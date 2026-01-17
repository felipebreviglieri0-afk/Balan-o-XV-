import streamlit as st
import pandas as pd
from datetime import datetime

# Estilo Visual "The Bestie" com cores da Conveniência da XV
st.set_page_config(page_title="Balanço XV", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    .product-card { background: #1e1e1e; padding: 15px; border-radius: 12px; border-left: 5px solid #00CED1; margin-bottom: 10px; }
    h1, h2 { color: #FF8C00 !important; }
    </style>
""", unsafe_allow_html=True)

# Lista completa extraída das suas fotos
PRODUTOS_XV = {
    "🥤 Refrigerantes": ["Coca Lata", "Guaraná Lata", "Sprite Lata", "Fanta Laranja", "Pepsi Lata", "Água", "Coca 2L", "Conquista Guaraná"],
    "🍺 Cervejas": ["Brahma", "Skol", "Amstel", "Heineken LN", "Budweiser", "Beats Azul", "Spaten", "Lokal Lata"],
    "🥃 Destilados": ["Dom Scott", "Red Label", "Jack Daniels", "Askov 900ml", "Smirnoff", "Velho Barreiro", "Combo Smirnoff"],
    "⚡ Energéticos": ["Monster Trad.", "Monster Melancia", "Red Bull", "Furioso 2L", "Magnetto 2L"],
    "🧹 Limpeza e Descartáveis": ["Papel Higiênico", "Detergente", "Copo 700ml", "Copo 50ml", "Saco Lixo 60L", "Canudo"],
    "🍓 Frutas e Gelo": ["Gelo Coco", "Gelo Maçã", "Gelo Potável", "Morango", "Melancia", "Limão", "Abacaxi"],
    "🍫 Doces e Outros": ["Ouro Branco", "Sonho de Valsa", "Fini Beijos", "Halls", "Trident", "Carvão", "Seda Zomo"]
}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Conveniência da XV 🚀")
    user = st.text_input("Usuário")
    if st.button("Entrar"):
        if user in ["Feli", "Pri", "Gordinho", "Felipe", "Gustavo"]:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.rerun()
else:
    st.sidebar.title(f"Olá, {st.session_state.user}!")
    aba = st.sidebar.radio("Navegação", ["📝 Fazer Balanço", "📊 Histórico"])

    if aba == "📝 Fazer Balanço":
        cat = st.selectbox("Escolha a Categoria", list(PRODUTOS_XV.keys()))
        
        with st.form("form_balanco"):
            dados_para_salvar = []
            for p in PRODUTOS_XV[cat]:
                st.markdown(f"<div class='product-card'><b>{p}</b></div>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                ini = c1.number_input(f"Início ({p})", min_value=0, key=f"i_{p}")
                ent = c2.number_input(f"Entrada ({p})", min_value=0, key=f"e_{p}")
                fin = c3.number_input(f"Final ({p})", min_value=0, key=f"f_{p}")
                dados_para_salvar.append({"Data": datetime.now().strftime("%d/%m/%Y"), "Produto": p, "Consumo": (ini+ent)-fin})
            
            if st.form_submit_button("Finalizar e Enviar para Planilha"):
                st.success("Balanço registrado com sucesso! (Conecte o Sheets nos Secrets para gravar permanentemente)")
                st.balloons()
