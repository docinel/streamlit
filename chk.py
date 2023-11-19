import streamlit as st
import pandas as pd

st.write("Hello, *World!* :sunglasses:")

df = pd.read_excel(
    io='TB_CUSTOS.xlsx',
    engine='openpyxl',
    usecols='A:E',

)

st.sidebar.write("Hello, *World!* :sunglasses:")

codigo = st.sidebar.selectbox(
    'Selecione o Código',
    df['CODIGO'],
)
produto = st.sidebar.selectbox(
    'Selecione o Produto',
    df['PRODUTO'],
    index=1
)

st.sidebar.write('Custo do Produto:', df[df['CODIGO'] == codigo]['CUSTOS'].values[0])
st.sidebar.write('Valor de Tabela:', df[df['CODIGO'] == codigo]['VALOR_TABELA'].values[0])
st.sidebar.write('Descrição do Produto:', df[df['CODIGO'] == codigo]['PRODUTO'].values[0])
