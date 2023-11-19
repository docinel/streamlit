import streamlit as st
import datetime
import pandas as pd

st.set_page_config(page_title="Cálculo de Custos, layout=center", page_icon="📈")
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

Custo_do_Produto = df[df['CODIGO'] == codigo]['CUSTOS'].values[0]
Valor_de_Tabela = df[df['CODIGO'] == codigo]['VALOR_TABELA'].values[0]
st.sidebar.write('Custo do Produto:', df[df['CODIGO'] == codigo]['CUSTOS'].values[0])
st.sidebar.write('Valor de Tabela:', df[df['CODIGO'] == codigo]['VALOR_TABELA'].values[0])
st.sidebar.write('ID do Produto:', df[df['CODIGO'] == codigo]['ID'].values[0])
st.sidebar.write('Descrição do Produto:', df[df['CODIGO'] == codigo]['PRODUTO'].values[0])

# CRIAR UM FORM PARA O PRECO DE VENDA E MATERIA PRIMA
with st.form("preco", clear_on_submit=False):
    preco_venda = st.number_input("Preço de Venda")
    materia_prima = st.number_input("Materia Prima")
    submit = st.form_submit_button("Calcular")

# CRIAR AS VARIAVEIS NÃO MUTÁVEIS
COMISSAO_REPR = 0.03
COMISSAO_GER = 0.0027
PIS_COFINS = 0.0365
IR_CSSL = 0.0306

with st.form("my_form", clear_on_submit=False):
    st.write("Inside the form")
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
        st.write(" :green[ALERTA] MARGEM DE CONTRIBUICAO ACIMA DE 30% " + " :rocket: " * 10)
    else:
        st.write(":red[ALERTA] \n MARGEM DE CONTRIBUICAO ABAIXO DE 30% " + " :disappointed: " * 10)
        st.write("FAVOR VERIFICAR O QUE PODE SER FEITO PARA AMENIZAR A PERDA")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Calcular")
resultado = st.button(":green[RESULTADO]")
if resultado:
    st.write("Custo do Produto:", f':green[R$ {Custo_do_Produto:.2f}]'.replace('.', ','))
    st.write("Despezas variáveis:", f'R$ {despesas_variaveis:.2f}'.replace('.', ','))
    st.write("Margem de Contribuição:", f'R$ {preco_venda - despesas_variaveis:.2f}'.replace('.', ','))
    st.write("Margem de Contribuição %:", f'{margem:.2f}%'.replace('.', ','))
    st.write("------")
    st.write("Frete Próprio:", f'R$ {frtp:.2f}'.replace('.', ','))
    st.write("Frete Terceiros:", f'R$ {frete_terceiros:.2f}'.replace('.', ','))
    st.write("Comissão Gerente:", f'R$ {cger:.2f}'.replace('.', ','))
    st.write("Comissão Representante:", f'R$ {crepr:.2f}'.replace('.', ','))
    st.write("Royalites Lider:", f'R$ {royalites:.2f}'.replace('.', ','))
    st.write("------")
    st.write("ICMS:", f'R$ {ic:.2f}'.replace('.', ','))
    st.write("PIS/COFINS:", f'R$ {pis:.2f}'.replace('.', ','))
    st.write("IR/CSLL:", f'R$ {ir:.2f}'.replace('.', ','))
    st.write("Prazo:", f'R$ {prazo:.2f}'.replace('.', ','))
