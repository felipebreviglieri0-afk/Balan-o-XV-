        import streamlit as st

# Estilo Visual "The Bestie"
st.set_page_config(page_title="Conveniência da XV", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: white; }
    [data-testid="stMetricValue"] { color: #00CED1 !important; }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stIFrame"] { background-color: #1e1e1e; }
    .product-card { background: #1e1e1e; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #FF8C00; }
    </style>
""", unsafe_allow_html=True)

# 1. Banco de Dados Inicial (Se você não editar, ele usa esse)
if 'produtos' not in st.session_state:
    st.session_state.produtos = {
        "🥤 Refrigerantes": ["Coca Lata", "Guaraná Lata", "Sprite Lata", "Coca 2L", "Coca 600ml", "Água 500ml", "Conquista Guaraná"],
        "🍺 Cervejas": ["Brahma Lata", "Skol Lata", "Heineken LN", "Budweiser", "Amstel", "Spaten", "Beats Azul"],
        "🧹 Limpeza/Embalagens": ["Detergente", "Papel Higiênico", "Copo 700ml", "Copo 50ml", "Saco Lixo 60L"],
        "🥃 Destilados": ["Red Label", "Jack Daniels", "Askov Tradicional", "Velho Barreiro", "Combo Smirnoff"],
        "🍫 Doces/Gelo": ["Ouro Branco", "Sonho de Valsa", "Gelo Coco", "Gelo Maçã", "Fini Beijos"]
    }

# 2. Sistema de Login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Conveniência da XV - Login 🚀")
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
        else: st.error("Erro no login")
else:
    # Menu Lateral
    menu = st.sidebar.radio("Menu", ["📝 Fazer Balanço", "⚙️ Gerenciar Itens", "📊 Relatórios"])
    if st.sidebar.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()

    # --- ABA: GERENCIAR ITENS (Somente Admin) ---
    if menu == "⚙️ Gerenciar Itens":
        if st.session_state.role == "admin":
            st.header("Gerenciar Produtos")
            cat_sel = st.selectbox("Escolha a Categoria para editar", list(st.session_state.produtos.keys()))
            novo_prod = st.text_input("Nome do novo produto")
            if st.button("Adicionar Produto"):
                st.session_state.produtos[cat_sel].append(novo_prod)
                st.success(f"{novo_prod} adicionado!")
            
            st.write("---")
            st.write("Produtos Atuais (Clique para remover):")
            for p in st.session_state.produtos[cat_sel]:
                if st.button(f"Remover {p}", key=f"rem_{p}"):
                    st.session_state.produtos[cat_sel].remove(p)
                    st.rerun()
        else:
            st.error("Acesso Negado. Apenas Admins podem alterar produtos.")

    # --- ABA: FAZER BALANÇO ---
    elif menu == "📝 Fazer Balanço":
        st.header(f"Balanço por: {st.session_state.user}")
        categoria = st.selectbox("Selecione a Categoria", list(st.session_state.produtos.keys()))
        
        for p in st.session_state.produtos[categoria]:
            with st.container():
                st.markdown(f"<div class='product-card'><b>{p}</b></div>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                ini = c1.number_input("Início", key=f"i_{p}", min_value=0)
                ent = c2.number_input("Entrada", key=f"e_{p}", min_value=0)
                fin = c3.number_input("Final", key=f"f_{p}", min_value=0)
                st.info(f"Consumo: {(ini + ent) - fin}")
        
        if st.button("Finalizar e Salvar"):
            st.balloons()
            st.success("Balanço salvo com sucesso!")

    elif menu == "📊 Relatórios":
        st.title("Em breve: Gráficos automáticos!")

