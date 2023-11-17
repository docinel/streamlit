import streamlit as st
import datetime

agora = datetime.datetime.now()
agora_txt = agora.strftime("%H")

if 0 < int(agora_txt) < 12:
    st.write("Bom dia!")
elif 12 <= int(agora_txt) < 18:
    st.write("Boa tarde!")
else:
    st.write("Boa noite!")

st.write("Data:", agora.strftime("%d/%m/%Y"))

COMISSAO_REPR = 0.03
COMISSAO_GER = 0.0027
FRETE_TERCEIROS = 0.12
FRETE_PROPRIO = 0.06
icms = [0.18, 0.16]
PIS_COFINS = 0.0365
IR_CSSL = 0.0306
with st.form("my_form", clear_on_submit=False):
    st.write("Inside the form")
    preco_venda = st.number_input("Preço de Venda", step=1)
    preco_materia_prima = st.number_input("Preço de matéria prima", step=1)

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
        if st.checkbox("Frete Terceiro", value=True):
            FRETE_TERCEIROS = 0.12
        else:
            FRETE_TERCEIROS = 0 
    with col3:
        if st.checkbox("Royalites Lider", value=True):
            royalites = 0.07
        else:
            royalites = 0
    with col4:
        if st.checkbox("Pagto a Prazo", value=True):
            prazo = 0.1
        else:
            prazo = 0
    frtp = FRETE_PROPRIO * preco_venda
    frete_terceiros = FRETE_TERCEIROS * preco_venda
    cger = COMISSAO_GER * preco_venda
    crepr = COMISSAO_REPR * preco_venda
    ic = icms * preco_venda
    pis = PIS_COFINS * preco_venda
    cofins = PIS_COFINS * preco_venda
    ir = IR_CSSL * preco_venda
    royalites = royalites * preco_venda
    prazo = prazo * preco_venda
    margem = 0
    despesa_geral = frtp + frete_terceiros + cger + crepr + ic + pis + cofins + ir + preco_materia_prima + royalites + prazo
    margem = (preco_venda - despesa_geral) / preco_venda * 100
    if margem >= 30:
        st.write(" :green[ALERTA]  MARGEM DE CONTRIBUICAO ACIMA DE 30% " + " :rocket: "* 10)
    else:
        st.write(":red[ALERTA]  MARGEM DE CONTRIBUICAO ABAIXO DE 30% " + " :disappointed: "* 10)
        st.write("FAVOR VERIFICAR O QUE PODE SER FEITO PARA AMENIZAR A PERDA")
    
    st.write("------")

    st.write("Margem de Contribuição:", preco_venda - despesa_geral)
    st.write("Margem de Contribuição %:", margem)    
    st.write("Despezas variáveis:", despesa_geral)
    st.write("Frete Próprio:", frtp)
    st.write("Frete Terceiros:", frete_terceiros)
    st.write("Comissão Gerente:", cger)
    st.write("Comissão Representante:", crepr)
    st.write("ICMS:", ic)
    st.write("PIS/COFINS:", pis)
    st.write("IR/CSLL:", ir)
    st.write("Royalites Lider:", royalites)
    st.write("Prazo:", prazo)

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
