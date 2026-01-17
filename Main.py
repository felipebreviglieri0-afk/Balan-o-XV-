import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Conveniência da XV", layout="wide")

# Conexão com a Planilha
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SISTEMA DE LOGIN COM SENHA ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Conveniência da XV - Acesso Restrito 🔐")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        # Definição de acessos
        admins = {"Feli": "priceca1", "Pri": "priceca1", "Gordinho": "priceca1"}
        colabs = {"Felipe": "conveniênciadaxv1", "Gustavo": "conveniênciadaxv1"}
        
        if user in admins and admins[user] == password:
            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.session_state.user = user
            st.rerun()
        elif user in colabs and colabs[user] == password:
            st.session_state.logged_in = True
            st.session_state.role = "colab"
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
else:
    # Menu Lateral
    opcoes = ["📝 Fazer Balanço"]
    if st.session_state.role == "admin":
        opcoes.append("📊 Gráficos e Relatórios")
    
    aba = st.sidebar.radio("Navegação", opcoes)
    if st.sidebar.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()

    # --- ABA DE BALANÇO ---
    if aba == "📝 Fazer Balanço":
        st.header(f"Balanço por: {st.session_state.user}")
        # (Aqui entra a lógica de produtos que já criamos antes...)
        st.info("Selecione a categoria no menu para começar o lançamento.")

    # --- ABA DE GRÁFICOS (SOMENTE ADMIN) ---
    elif aba == "📊 Gráficos e Relatórios":
        st.header("Análise de Vendas e Consumo")
        try:
            df = conn.read()
            if not df.empty:
                # Gráfico de Consumo por Produto
                fig = px.bar(df, x="Produto", y="Consumo", color="Produto", title="Produtos mais vendidos (Consumo)")
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Dados Brutos da Planilha")
                st.write(df)
            else:
                st.warning("Ainda não existem dados salvos na planilha.")
        except:
            st.error("Erro ao carregar gráficos. Verifique a conexão com o Google Sheets.")
