import streamlit as st

with st.form("my_form"):
    valor_de_tabela = st.number_input("Valor de Tabela")
    custo_do_produto = st.number_input("Custo do Produto")
    submitted = st.form_submit_button("Submit")
comissao_representante = 0.03 * valor_de_tabela
comissao_gerente = 0.0027 * valor_de_tabela
pis_cofins = 0.0365 * valor_de_tabela
icms = 0.18 * valor_de_tabela
ir_cssl = 0.0306 * valor_de_tabela
royalites = 0.07 * valor_de_tabela
frete_proprio = 0.06 * valor_de_tabela
frete_terceiros = 0.12 * valor_de_tabela
antecipacao = 0.1 * valor_de_tabela

st.write("comissão representante:", comissao_representante)
st.write("comissão gerente:", comissao_gerente)
st.write("PIS/COFINS:", pis_cofins)
st.write("ICMS:", icms)
st.write("IR/CSLL:", ir_cssl)
st.write("Royalites Lider:", royalites)
st.write("Frete Próprio:", frete_proprio)
st.write("Frete Terceiros:", frete_terceiros)
st.write("Antecipação:", antecipacao)
despesas_variaveis = comissao_representante + comissao_gerente + pis_cofins + icms + ir_cssl + royalites + frete_proprio + frete_terceiros + antecipacao + custo_do_produto

st.write("Despesas Variáveis:", despesas_variaveis)
st.write("Margem de Contribuição:", valor_de_tabela - despesas_variaveis)
st.write("Margem de Contribuição %:", (valor_de_tabela - despesas_variaveis) / valor_de_tabela * 100)