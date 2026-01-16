import streamlit as st
import pandas as pd

# Configuração Visual Estilo "The Bestie"
st.set_page_config(page_title="Conveniência da XV", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .stButton>button { border-radius: 20px; background: linear-gradient(45deg, #FF8C00, #00CED1); color: white; border: none; font-weight: bold; }
    .card { background-color: #1e1e1e; padding: 20px; border-radius: 15px; border-left: 5px solid #00CED1; }
    </style>
""", unsafe_allow_html=True)

# 1. Gerenciamento de Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.image("https://i.imgur.com/vH6Z4Uf.png", width=200) # Coloque seu logo aqui
    st.title("Conveniência da XV 🚀")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        admins = {"Feli": "priceca1", "Pri": "priceca1", "Gordinho": "priceca1"}
        colabs = {"Felipe": "conveniênciadaxv1", "Gustavo": "conveniênciadaxv1"}
        
        if user in admins and admins[user] == password:
            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.rerun()
        elif user in colabs and colabs[user] == password:
            st.session_state.logged_in = True
            st.session_state.role = "colab"
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")

# 2. App após Login
else:
    st.sidebar.title(f"Bem-vindo, {st.session_state.role}!")
    menu = st.sidebar.radio("Navegação", ["Fazer Balanço", "Relatórios", "Gerenciar Produtos"])

    if menu == "Fazer Balanço":
        cat = st.selectbox("Escolha a Categoria", ["🥤 Refrigerantes", "🍺 Cervejas", "🥃 Destilados", "🧹 Limpeza & Embalagens", "🍫 Doces & Tabacaria"])
        
        st.write(f"### Lançamento: {cat}")
        # Exemplo de linha de produto
        with st.container():
            col1, col2, col3, col4 = st.columns([2,1,1,1])
            col1.write("**Coca Lata**")
            ini = col2.number_input("Inicial", key="coca_ini", step=1)
            ent = col3.number_input("Entrada", key="coca_ent", step=1)
            fin = col4.number_input("Final", key="coca_fin", step=1)
            
            consumo = (ini + ent) - fin
            st.success(f"Consumo Total: {consumo}")
        
        if st.button("Salvar Balanço da Semana"):
            st.balloons()
            st.success("Balanço salvo com sucesso!")

    if menu == "Relatórios":
        if st.session_state.role == "admin":
            st.title("📊 Desempenho Semanal")
            st.write("Gráficos de produtos mais vendidos aparecerão aqui.")
        else:
            st.error("Acesso negado.")
