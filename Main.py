import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Conveniência da XV", layout="wide")

# Conectando à Planilha
conn = st.connection("gsheets", type=GSheetsConnection)

# Estilo Visual
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .product-card { background: #1e1e1e; padding: 15px; border-radius: 12px; border-left: 5px solid #FF8C00; margin-bottom: 10px; }
    h1, h2, h3 { color: #FF8C00 !important; }
    </style>
""", unsafe_allow_html=True)

# Lista de Produtos Real
PRODUTOS_XV = {
    "🥤 Refrigerantes": ["Coca lata", "Guaraná lata", "Sprite lata", "Fanta laranja", "Pepsi lata", "Água", "Coca 600ml", "Coca 2L", "Conquista Guaraná"],
    "🍺 Cervejas": ["Brahma", "Skol", "Amstel", "Heineken LN", "Budweiser", "Beats Azul", "Spaten", "Lokal lata"],
    "🥃 Destilados": ["Dom Scott", "Red Label", "Jack Daniels", "Askov 900ml", "Smirnoff", "Velho Barreiro", "Combo Smirnoff"],
    "⚡ Energéticos": ["Monster Trad.", "Monster Melancia", "Red Bull", "Furioso 2L", "Magnetto 2L"],
    "🍓 Frutas & Gelo": ["Gelo Potável", "Gelo Coco", "Gelo Maçã", "Morango", "Melancia", "Limão", "Abacaxi"],
    "🧹 Limpeza & Copos": ["Copo 700ml", "Copo 50ml", "Papel Higiênico", "Detergente", "Saco lixo 60L", "Canudo"],
    "🍫 Doces & Tabacaria": ["Ouro Branco", "Sonho de Valsa", "Fini Beijos", "Halls", "Trident", "Carvão", "Seda Zomo"]
}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Conveniência da XV 🚀")
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        admins = {"Feli": "priceca1", "Pri": "priceca1", "Gordinho": "priceca1"}
        colabs = {"Felipe": "conveniênciadaxv1", "Gustavo": "conveniênciadaxv1"}
        
        if user in admins and admins[user] == password:
            st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "admin", user
            st.rerun()
        elif user in colabs and colabs[user] == password:
            st.session_state.logged_in, st.session_state.role, st.session_state.user = True, "colab", user
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
else:
    opcoes = ["📝 Fazer Balanço"]
    if st.session_state.role == "admin":
        opcoes.append("📊 Visão do Dono")
    
    aba = st.sidebar.radio("Navegação", opcoes)
    if st.sidebar.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()

    if aba == "📝 Fazer Balanço":
        st.header(f"Balanço por: {st.session_state.user}")
        cat = st.selectbox("Escolha a Categoria", list(PRODUTOS_XV.keys()))
        
        with st.form("form_balanco"):
            lista_dados = []
            for p in PRODUTOS_XV[cat]:
                st.markdown(f"<div class='product-card'><b>{p}</b></div>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                ini = c1.number_input("Início", key=f"i_{p}", min_value=0)
                ent = c2.number_input("Entrada", key=f"e_{p}", min_value=0)
                fin = c3.number_input("Final", key=f"f_{p}", min_value=0)
                consumo = (ini + ent) - fin
                lista_dados.append({"Data": datetime.now().strftime("%d/%m/%Y"), "Funcionario": st.session_state.user, "Produto": p, "Consumo": consumo})
            
            if st.form_submit_button("SALVAR NO GOOGLE"):
                df_novo = pd.DataFrame(lista_dados)
                existente = conn.read()
                updated_df = pd.concat([existente, df_novo], ignore_index=True)
                conn.update(data=updated_df)
                st.success("Salvo com sucesso!")
                st.balloons()

    elif aba == "📊 Visão do Dono":
        st.header("Gráficos de Vendas")
        df = conn.read()
        if not df.empty:
            fig = px.bar(df, x="Produto", y="Consumo", color="Produto", title="Consumo por Produto")
            st.plotly_chart(fig, use_container_width=True)
            st.write("### Histórico da Planilha")
            st.dataframe(df)
