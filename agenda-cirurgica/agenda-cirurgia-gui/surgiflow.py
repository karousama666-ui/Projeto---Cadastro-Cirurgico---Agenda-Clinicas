import customtkinter as ctk
from tkinter import ttk
import sqlite3
import os

from PIL import Image
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.geometry("1200x700")

# =========================
# CAMINHO DOS ARQUIVOS
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CAMINHO_LOGO = os.path.join(
    BASE_DIR,
    "logo_surgiflow.png"
)

# ===========================
# FRAME LOGIN
# ===========================

frame_login = ctk.CTkFrame(app)

frame_login.pack(
    fill="both",
    expand=True
)

ctk.CTkLabel(
    frame_login,
    text="LOGIN",
    font=("Segoe UI", 30, "bold")
).pack(
    pady=100
)


# ===========================
# FRAME DO DASHBOARD
# ===========================

frame_dashboard = ctk.CTkFrame(
    app,
    fg_color="#F8F7FF"
)

# ======================
# AREA PRINCIPAL
# ======================

sidebar = ctk.CTkFrame(
    frame_dashboard,
    width=70,
    corner_radius=0,
    fg_color="#EDE9FE"
)

sidebar.pack(
    side="left",
    fill="y"
)

logo_sidebar = ctk.CTkImage(
    light_image=Image.open(CAMINHO_LOGO),
    dark_image=Image.open(CAMINHO_LOGO),
    size=(100,100)
)


logo_label = ctk.CTkLabel(
    sidebar,
    image=logo_sidebar,
    text=""
)

logo_label.pack(
    pady=(25,10)
)


conteudo_principal = ctk.CTkFrame(
    frame_dashboard,
    fg_color="#F8F7FF"
)

conteudo_principal.pack(
    side="right",
    fill="both",
    expand=True
)

# ===========================
# CONTAINER DO DASHBOARD
# ===========================

dashboard_container = ctk.CTkFrame(
    frame_dashboard,
    fg_color="transparent"
)

dashboard_container.pack(
    fill="both",
    expand=True
)

# ===========================
# SIDEBAR
# ===========================

sidebar = ctk.CTkFrame(
    dashboard_container,
    width=240,
    corner_radius=0,
    fg_color="#7154CE"
)

sidebar.pack(
    side="left",
    fill="y"
)



# ===========================
# ÁREA DE CONTEÚDO
# ===========================

conteudo = ctk.CTkFrame(
    dashboard_container,
    fg_color="#F8F7FF",
    corner_radius=0
)

conteudo.pack(
    side="left",
    fill="both",
    expand=True
)

conteudo_principal = ctk.CTkFrame(
    conteudo,
    fg_color="transparent"
)

conteudo_principal.pack(
    fill="both",
    expand=True,
    padx=40,
    pady=30
)

# ===========================
# TOPBAR
# ===========================

topbar = ctk.CTkFrame(
    conteudo_principal,
    fg_color="transparent"
)

topbar.pack(
    fill="x",
    pady=(0,15)
)


# lado esquerdo

titulo_top = ctk.CTkLabel(
    topbar,
    text="SurgiFlow",
    font=(
        "Segoe UI",
        24,
        "bold"
    ),
    text_color="#2D2438"
)

titulo_top.pack(
    side="left"
)


# lado direito

usuario_area = ctk.CTkFrame(
    topbar,
    fg_color="transparent"
)

usuario_area.pack(
    side="right"
)


label_usuario = ctk.CTkLabel(
    usuario_area,
    text="👤 Administrador",
    font=(
        "Segoe UI",
        14
    )
)

label_usuario.pack(
    side="left",
    padx=15
)


botao_notificacao = ctk.CTkButton(
    usuario_area,
    text="🔔 0",
    width=80,
    height=35,
    fg_color="#7154CE",
    hover_color="#5B3FA8"
)

botao_notificacao.pack(
    side="left"
)

titulo_dashboard = ctk.CTkLabel(
    conteudo_principal,
    text="📊 Dashboard",
    font=(
        "Segoe UI",
        34,
        "bold"
    ),
    text_color="#2D2438"
)

titulo_dashboard.pack(
    anchor="w"
)

subtitulo_dashboard = ctk.CTkLabel(
    conteudo_principal,
    text="Resumo das cirurgias e indicadores do dia",
    font=(
        "Segoe UI",
        15
    ),
    text_color="#6B7280"
)

subtitulo_dashboard.pack(
    anchor="w",
    pady=(0,30)
)


# BANCO DE DADOS

import os

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


BANCO = os.path.join(
    BASE_DIR,
    "cirurgias.db"
)

# FUNÇÃO CRIAR CARDS

def criar_card(parent, titulo, valor, cor):
    sombra = ctk.CTkFrame(
        parent,
        width=190,
        height=130,
        fg_color="#E9E4FF",
        corner_radius=22
    )

    sombra.pack(
        side="left",
        padx=15,
        pady=10
    )

    card = ctk.CTkFrame(
        sombra,
        width=180,
        height=120,
        fg_color=cor,
        corner_radius=20
    )

    card.pack_propagate(False)
    card.pack(expand=True, fill="both", padx=5, pady=5)

    ctk.CTkLabel(
        card,
        text=titulo,
        font=(
            "Segoe UI",
            15,
            "bold"
        ),
        text_color="white"
    ).pack(
        pady=(18, 5)
    )

    numero = ctk.CTkLabel(
        card,
        text=str(valor),
        font=(
            "Segoe UI",
            38,
            "bold"
        ),
        text_color="white"
    )

    numero.pack()

    return card, numero

# FUNÇÃO CARREGAR INDICADORES

def carregar_indicadores():

    conexao = sqlite3.connect(
        BANCO
    )

    cursor = conexao.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM cirurgias"
    )

    total = cursor.fetchone()[0]


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM cirurgias
        WHERE status='Agendada'
        """
    )

    agendadas = cursor.fetchone()[0]


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM cirurgias
        WHERE status='Confirmada'
        """
    )

    confirmadas = cursor.fetchone()[0]


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM cirurgias
        WHERE status='Cancelada'
        """
    )

    canceladas = cursor.fetchone()[0]


    conexao.close()


    return (
        total,
        agendadas,
        confirmadas,
        canceladas
    )

# FUNÇÃO CARREGAR CIRURGIAS

def carregar_cirurgias():

    conexao = sqlite3.connect(
        BANCO
    )

    cursor = conexao.cursor()


    cursor.execute(
        """
        SELECT 
        paciente,
        medico,
        hospital,
        data,
        status

        FROM cirurgias
        ORDER BY data
        """
    )


    dados = cursor.fetchall()


    conexao.close()


    return dados

# FUNÇÃO VERIFICAR LOGIN

def verificar_login():

    global usuario_logado
    global nivel_logado


    usuario = entry_usuario.get()
    senha = entry_senha.get()


    # seu banco continua igual...


    if resultado:

        usuario_logado = usuario
        nivel_logado = resultado[0]


        frame_login.pack_forget()


        frame_dashboard.pack(
            fill="both",
            expand=True
        )



    else:

        messagebox.showerror(
            "Erro",
            "Usuário ou senha inválidos"
        )

# FRAME CARDS

frame_cards = ctk.CTkFrame(
    conteudo_principal,
    fg_color="transparent"
)

frame_cards.pack(
    anchor="w"
)

cards = ctk.CTkFrame(
    frame_cards,
    fg_color="transparent"
)

cards.pack(
    anchor="w"
)

card_total, lbl_total = criar_card(
    cards,
    "🩺 Cirurgias",
    0,
    "#5B3FD6"
)

card_total.pack(
    side="left",
    padx=(0,20)
)


card_agendada, lbl_agendada = criar_card(
    cards,
    "📅 Agendadas",
    0,
    "#F59E0B"
)

card_agendada.pack(
    side="left",
    padx=20
)


card_confirmada, lbl_confirmada = criar_card(
    cards,
    "✅ Confirmadas",
    0,
    "#22C55E"
)

card_confirmada.pack(
    side="left",
    padx=20
)


card_cancelada, lbl_cancelada = criar_card(
    cards,
    "❌ Canceladas",
    0,
    "#EF4444"
)

card_cancelada.pack(
    side="left",
    padx=(20,0)
)

# FUNÇÃO ATUALIZAR CARDS

def atualizar_cards():

    total, agendadas, confirmadas, canceladas = carregar_indicadores()


    lbl_total.configure(
        text=total
    )

    lbl_agendada.configure(
        text=agendadas
    )

    lbl_confirmada.configure(
        text=confirmadas
    )

    lbl_cancelada.configure(
        text=canceladas
    )

# FUNÇÃO MOSTRAR DASHBOARD

def mostrar_dashboard():

    limpar_conteudo()

    titulo = ctk.CTkLabel(
        conteudo_principal,
        text="📊 Dashboard",
        font=("Segoe UI",30,"bold")
    )

    titulo.pack(
        anchor="w",
        pady=20
    )

    atualizar_cards()

# FUNÇÃO PARA ABRIR O DASHBOARD

def abrir_dashboard():

    atualizar_cards()

    frame_login.pack_forget()

    frame_dashboard.pack(
        fill="both",
        expand=True
    )

# FUNÇÃO MOSTRAR AGENDA

def mostrar_agenda():

    limpar_conteudo()


    titulo = ctk.CTkLabel(
        conteudo_principal,
        text="📅 Agenda Cirúrgica",
        font=(
            "Segoe UI",
            30,
            "bold"
        )
    )

    titulo.pack(
        anchor="w",
        pady=20
    )


    botao_novo = ctk.CTkButton(
        conteudo_principal,
        text="+ Nova Cirurgia",
        fg_color="#7154CE"
    )

    botao_novo.pack(
        anchor="e",
        pady=10
    )


    tabela = ttk.Treeview(
        conteudo_principal,
        columns=(
            "paciente",
            "medico",
            "hospital",
            "data",
            "status"
        ),
        show="headings"
    )


    tabela.heading(
        "paciente",
        text="Paciente"
    )

    tabela.heading(
        "medico",
        text="Médico"
    )

    tabela.heading(
        "hospital",
        text="Hospital"
    )

    tabela.heading(
        "data",
        text="Data"
    )

    tabela.heading(
        "status",
        text="Status"
    )


    tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )


    for cirurgia in carregar_cirurgias():

        tabela.insert(
            "",
            "end",
            values=cirurgia
        )

# ===========================
# BOTÕES SIDEBAR
# ===========================


def criar_botao_menu(texto, comando):

    botao = ctk.CTkButton(
        sidebar,
        text=texto,
        width=170,
        height=40,
        corner_radius=10,
        fg_color="#FFFFFF",
        text_color="#2D2438",
        hover_color="#DDD6FE",
        command=comando
    )

    botao.pack(
        pady=8,
        padx=15
    )


criar_botao_menu(
    "📊 Dashboard",
    mostrar_dashboard
)


criar_botao_menu(
    "📅 Agenda",
    mostrar_agenda
)


criar_botao_menu(
    "🗓 Calendário",
    lambda: print("Calendário")
)


criar_botao_menu(
    "👥 Usuários",
    lambda: print("Usuários")
)


criar_botao_menu(
    "📄 Relatórios",
    lambda: print("Relatórios")
)

# ===========================
# LOGO
# ===========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CAMINHO_LOGO = os.path.join(
    BASE_DIR,
    "logo_surgiflow.png"
)

logo = ctk.CTkImage(
    light_image=Image.open(CAMINHO_LOGO),
    dark_image=Image.open(CAMINHO_LOGO),
    size=(250,250)
)

ctk.CTkLabel(
    frame_login,
    image=logo,
    text=""
).pack(
    pady=(30,10)
)

ctk.CTkLabel(
    frame_login,
    text="Bem-vindo",
    font=("Segoe UI",30,"bold")
).pack()

ctk.CTkLabel(
    frame_login,
    text="Faça login para continuar",
    font=("Segoe UI",14),
    text_color="#777777"
).pack(
    pady=(0,30)
)

entrada_usuario = ctk.CTkEntry(
    frame_login,
    width=320,
    height=42,
    placeholder_text="Usuário"
)

entrada_usuario.pack(
    pady=10
)

entrada_senha = ctk.CTkEntry(
    frame_login,
    width=320,
    height=42,
    show="•",
    placeholder_text="Senha"
)

entrada_senha.pack(
    pady=10
)

botao_login = ctk.CTkButton(
    frame_login,
    text="Entrar",
    width=320,
    height=45,
    command=abrir_dashboard
)

botao_login.pack(
    pady=30
)

frame_login.pack(
    fill="both",
    expand=True
)


app.mainloop()