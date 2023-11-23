# streamlit_app.py

import hmac
import streamlit as st
import datetime
import pandas as pd


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Usuário", key="username")
            st.text_input("Senha", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Verifique a senha informada o usuário está correto."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 Usuário incorreto ou senha inválida. ")
    return False


if not check_password():
    st.stop()

# Main Streamlit app starts here
st.set_page_config(page_title="Cálculo de Custos", layout="centered", page_icon="📈")
st.header(":blue[CÁLCULO DE CUSTOS - PREMIUM E LÍDER]")
# DETERMINAR O HORARIO DA SAUDAÇÂO
agora = datetime.datetime.now()
agora_txt = agora.strftime("%H")

if 0 < int(agora_txt) < 12:
    st.write("Bom dia!")
elif 12 <= int(agora_txt) < 18:
    st.write("Boa tarde!")
else:
    st.write("Boa noite!")

st.write("Data:", agora.strftime("%d/%m/%Y"))

# SELECIONAR A PLANILHA DE CUSTOS
df = pd.read_excel(
    io='TB_CUSTOS.xlsx',
    engine='openpyxl',
    usecols='A:E',
)

# ABRIR O SIDEBAR PARA SELECIONAR O CODIGO
st.sidebar.subheader(":blue[CÁLCULO DE CUSTOS - PREMIUM E LÍDER]")

codigo = st.sidebar.selectbox(
    ':blue[Selecione o Código:]',
    df['CODIGO'],
)
if st.sidebar.button("RECARREGAR"):
    st.rerun()
st.sidebar.divider()
Custo_do_Produto = df[df['CODIGO'] == codigo]['CUSTOS'].values[0]
Valor_de_Tabela = df[df['CODIGO'] == codigo]['VALOR_TABELA'].values[0]
st.sidebar.write(f':blue[Custo do Produto: :green[R$ {df[df["CODIGO"] == codigo]["CUSTOS"].values[0]:.2f}]]'
                 .replace('.', ','))
st.sidebar.write(f':blue[Valor de Tabela: :green[R$ {df[df["CODIGO"] == codigo]["VALOR_TABELA"].values[0]:.2f}]]'
                 .replace('.', ','))
st.sidebar.write(f':blue[ID do Produto: :green[{df[df["CODIGO"] == codigo]["ID"].values[0]}]]')
st.sidebar.divider()
st.sidebar.write(':red[Descrição do Produto:]', df[df['CODIGO'] == codigo]['PRODUTO'].values[0])

# CRIAR UM FORM PARA O PRECO DE VENDA E MATERIA PRIMA
with st.form("preco", clear_on_submit=True):
    st.subheader(":green[PRATICAR PREÇO DE VENDA FORA DA TABELA:]", divider='grey')
    preco_venda = st.number_input("Preço de Venda")
    submit = st.form_submit_button("Calcular")

# CRIAR AS VARIAVEIS NÃO MUTÁVEIS
COMISSAO_REPR = 0.03
COMISSAO_GER = 0.0027
PIS_COFINS = 0.0365
IR_CSSL = 0.0306

with st.form("my_form", clear_on_submit=True):
    # st.write("CALCULAR PREÇO DE VENDA")
    if preco_venda == 0:
        preco_venda = Valor_de_Tabela

    icms = st.selectbox("ICMS", ["18", "16"])
    if icms == "18":
        icms = 0.18
    else:
        icms = 0.16

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.checkbox("Frete Própio", value=True):
            FRETE_PROPRIO = 0.06
        else:
            FRETE_PROPRIO = 0
    with col2:
        if st.checkbox("Frete Terceiro", value=False):
            FRETE_TERCEIROS = 0.12
        else:
            FRETE_TERCEIROS = 0

    with col3:
        if st.checkbox("Royalites Lider", value=False):
            royalites = 0.07
        else:
            royalites = 0

    with col4:
        if st.checkbox("Pagto a Prazo", value=True):
            prazo = 0.1
        else:
            prazo = 0

    if preco_venda == 0:
        frtp = FRETE_PROPRIO * Valor_de_Tabela
    else:
        frtp = FRETE_PROPRIO * preco_venda

    if preco_venda == 0:
        frete_terceiros = FRETE_TERCEIROS * Valor_de_Tabela
    else:
        frete_terceiros = FRETE_TERCEIROS * preco_venda

    if preco_venda == 0:
        cger = COMISSAO_GER * Valor_de_Tabela
        crepr = COMISSAO_REPR * Valor_de_Tabela
    else:
        cger = COMISSAO_GER * preco_venda
        crepr = COMISSAO_REPR * preco_venda

    if preco_venda == 0:
        ic = icms * Valor_de_Tabela
        ir = IR_CSSL * Valor_de_Tabela
        royalites = royalites * Valor_de_Tabela
        pis = PIS_COFINS * Valor_de_Tabela
    else:
        ic = icms * preco_venda
        ir = IR_CSSL * preco_venda
        royalites = royalites * preco_venda
        pis = PIS_COFINS * preco_venda

    if preco_venda == 0:
        prazo = prazo * Valor_de_Tabela
    else:
        prazo = prazo * preco_venda

    margem = 0
    despesas_variaveis = frtp + frete_terceiros + cger + crepr + ic + pis + ir + royalites + prazo + Custo_do_Produto
    margem = ((preco_venda - despesas_variaveis) / preco_venda * 100)

    if margem >= 30:
        st.subheader(" :green[MARGEM DE CONTRIBUICAO ACIMA DE 30%] " + ":rocket: " * 3)
    else:
        st.subheader(":red[MARGEM DE CONTRIBUIÇÃO ABAIXO DE 30%] " + " :disappointed: " * 3)
        st.write("FAVOR VERIFICAR O QUE PODE SER FEITO PARA AMENIZAR A PERDA")
    
    # Every form must have a submit button.
    submitted = st.form_submit_button("Calcular")
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Valor de Tabela:", f':green[R$ {Valor_de_Tabela:.2f}]'.replace('.', ','))
    with col2:
        st.write("Fora de tabela:", f':green[R$ {preco_venda:.2f}]'.replace('.', ','))
    with col3:
        des_apl = 100-((preco_venda/Valor_de_Tabela)*100)
        st.write("Desconto Aplicado:", f':green[{des_apl:.2f}%]'.replace('.', ','))
    st.divider()
    st.write("Custo do Produto:", f':green[R$ {Custo_do_Produto:.2f}]'.replace('.', ','))
    st.write("Despesas variáveis:", f':green[R$ {despesas_variaveis:.2f}]'.replace('.', ','))
    st.write("Margem de Contribuição:", f':green[R$ {preco_venda - despesas_variaveis:.2f}]'.replace('.', ','))
    st.write("Margem de Contribuição %:", f':green[{margem:.2f}%]'.replace('.', ','))
    st.write("------")
    st.write("Frete Próprio:", f':green[R$ {frtp:.2f}]'.replace('.', ','))
    st.write("Frete Terceiros:", f':green[R$ {frete_terceiros:.2f}]'.replace('.', ','))
    st.write("Comissão Gerente:", f':green[R$ {cger:.2f}]'.replace('.', ','))
    st.write("Comissão Representante:", f':green[R$ {crepr:.2f}]'.replace('.', ','))
    st.write("Royalites Lider:", f':green[R$ {royalites:.2f}]'.replace('.', ','))
    st.write("------")
    st.write("ICMS:", f':green[R$ {ic:.2f}]'.replace('.', ','))
    st.write("PIS/COFINS:", f':green[R$ {pis:.2f}]'.replace('.', ','))
    st.write("IR/CSLL:", f':green[R$ {ir:.2f}]'.replace('.', ','))
    st.write("Prazo:", f':green[R$ {prazo:.2f}]'.replace('.', ','))
