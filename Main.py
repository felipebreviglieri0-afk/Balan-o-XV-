import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import plotly.express as px

# Configurações de Página
st.set_page_config(page_title="Conveniência da XV", layout="wide")

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILIZAÇÃO CUSTOMIZADA ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    [data-testid="stMetricValue"] { color: #00CED1 !important; }
    .product-card { background: #1e1e1e; padding: 15px; border-radius: 12px; border-left: 5px solid #FF8C00; margin-bottom: 10px; }
    h1, h2, h3 { color: #FF8C00 !important; }
    .stButton>button { width: 100%; border-radius: 20px; background: linear-gradient(45deg, #FF8C00, #00CED1); color: white; border: none; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS DE PRODUTOS (EXTRAÍDO DAS SUAS FOTOS) ---
PRODUTOS_XV = {
    "🥤 Refrigerantes": ["Coca lata", "Guaraná lata", "Sprite lata", "Fanta laranja", "Pepsi lata", "Água c/ gás", "Água s/ gás", "Coca 600ml", "Coca 2L", "Conquista Guaraná", "Conquista Cola", "Conquista Laranja"],
    "🍺 Cervejas & Long Neck": ["Brahma", "Skol", "Amstel", "Original", "Itaipava", "Petra", "Heineken LN", "Spaten LN", "Corona LN", "Budweiser LN", "Beats Azul", "Beats Vermelha", "Lokal lata"],
    "🥃 Destilados & Doses": ["Dom Scott", "Red Label", "Jack Daniels", "Passport", "Ballantines", "White Horse", "Askov 900ml", "Smirnoff", "Absolut", "Velho Barreiro", "Cachaça 51", "Campari"],
    "⚡ Energéticos": ["Monster Trad.", "Monster Melancia", "Monster Manga", "Red Bull", "Furioso 2L", "Magnetto 2L"],
    "🍓 Frutas & Gelo": ["Gelo Potável", "Gelo Coco", "Gelo Maçã", "Gelo Maracujá", "Morango", "Melancia", "Limão", "Laranja", "Abacaxi"],
    "🧹 Limpeza & Copos": ["Copo 700ml", "Copo 50ml", "Papel Higiênico", "Detergente", "Saco lixo 60L", "Saco lixo 200L", "Canudo", "Guardanapo"],
    "🍫 Doces & Tabacaria": ["Ouro Branco", "Sonho de Valsa", "Prestigio", "Chokito", "Fini Beijos", "Halls", "Trident", "Carvão", "Seda Zomo", "Isqueiro Bic"]
}

# --- SISTEMA DE LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Conveniência da XV - Login 🔐")
    with st.container():
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password") # AGORA COM CAMPO DE SENHA
        
        if st.button("Acessar Sistema"):
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
                st.error("Usuário ou senha incorretos. Tente novamente.")

# --- APP APÓS LOGIN ---
else:
    st.sidebar.title(f"Olá, {st.session_state.user}!")
    
    menu_opcoes = ["📝 Fazer Balanço"]
    if st.session_state.role == "admin":
        menu_opcoes.append("📊 Visão do Dono (Gráficos)")
    
    aba = st.sidebar.radio("Selecione uma opção:", menu_opcoes)
    
    if st.sidebar.button("Sair / Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- ABA: FAZER BALANÇO ---
    if aba == "📝 Fazer Balanço":
        st.header("Lançamento de Estoque")
        categoria = st.selectbox("Escolha a Categoria", list(PRODUTOS_XV.keys()))
        
        with st.form("balanco_xv"):
            lista_para_salvar = []
            st.subheader(f"Itens de {categoria}")
            
            for p in PRODUTOS_XV[categoria]:
                st.markdown(f"<div class='product-card'><b>{p}</b></div>", unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns([1,1,1,1])
                ini = c1.number_input("Início", key=f"i_{p}", min_value=0, step=1)
                ent = c2.number_input("Entrada", key=f"e_{p}", min_value=0, step=1)
                fin = c3.number_input("Final", key=f"f_{p}", min_value=0, step=1)
                consumo = (ini + ent) - fin
                c4.metric("Consumo", consumo)
                
                lista_para_salvar.append({
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Funcionario": st.session_state.user,
                    "Categoria": categoria,
                    "Produto": p,
                    "Inicial": ini,
                    "Entrada": ent,
                    "Final": fin,
                    "Consumo": consumo
                })
            
            enviar = st.form_submit_button("FINALIZAR E SALVAR NO GOOGLE")
            
            if enviar:
                try:
                    df_novo = pd.DataFrame(lista_para_salvar)
                    existente = conn.read()
                    updated_df = pd.concat([existente, df_novo], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("Balanço salvo com sucesso na planilha!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro ao salvar: Verifique os Secrets do Streamlit.")

    # --- ABA: GRÁFICOS (ADMIN) ---
    elif aba == "📊 Visão do Dono (Gráficos)":
        st.header("Análise de Consumo Semanal")
        try:
            df_dash = conn.read()
            if not df_dash.empty:
                # Gráfico de Consumo
                fig = px.bar(df_dash, x="Produto", y="Consumo", color="Categoria", title="Consumo por Produto")
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Histórico Completo")
                st.dataframe(df_dash)
            else:
                st.info("Ainda não há dados na planilha para gerar gráficos.")
        except:
            st.error("Não foi possível carregar os dados. Verifique a planilha.")
                
