import customtkinter as ctk
import sqlite3
import os

from PIL import Image
from tkinter import messagebox


# =========================
# CONFIGURAÇÃO VISUAL
# =========================

ctk.set_appearance_mode("light")

ctk.set_default_color_theme("blue")


# =========================
# JANELA PRINCIPAL
# =========================

app = ctk.CTk()

app.title(
    "SurgiFlow"
)

app.geometry(
    "1200x700"
)


# =========================
# CORES SURGIFLOW
# =========================

ROXO = "#3B1F70"
ROXO_CLARO = "#8B5CF6"
LILAS = "#DDD6FE"
FUNDO = "#F8F7FF"
TEXTO = "#24153F"

USUARIO_LOGADO = "Administrador"

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


BANCO = os.path.join(
    BASE_DIR,
    "cirurgias.db"
)

CAMINHO_LOGO = os.path.join(
    BASE_DIR,
    "logo_surgiflow.png"
)

logo_sidebar = ctk.CTkImage(
    light_image=Image.open(CAMINHO_LOGO),
    dark_image=Image.open(CAMINHO_LOGO),
    size=(150, 150)
)



app.configure(
    fg_color=FUNDO
)


# =========================
# SIDEBAR
# =========================

sidebar = ctk.CTkFrame(
    app,
    width=240,
    corner_radius=0,
    fg_color="#7154CE"
)

sidebar.pack(
    side="left",
    fill="y"
)


# LOGO TEXTO

logo = ctk.CTkLabel(
    sidebar,
    image=logo_sidebar,
    text=""
)

logo.pack(
    pady=(35, 10)
)

subtitulo = ctk.CTkLabel(
    sidebar,
    text="Gestão\nCirúrgica",
    font=(
        "Segoe UI",
        14
    ),
    text_color="#F8F7FC"
)

subtitulo.pack(
    pady=10
)


# =========================
# MENU
# =========================

def criar_botao(texto, comando):

    botao = ctk.CTkButton(
        sidebar,
        text=texto,
        width=190,
        height=40,
        corner_radius=10,
        fg_color="#D8CAEB",
        text_color=TEXTO,
        hover_color="#C084FC",
        command=comando
    )

    botao.pack(
        pady=8,
        padx=20
    )





# =========================
# ÁREA PRINCIPAL
# =========================

conteudo = ctk.CTkFrame(
    app,
    fg_color=FUNDO,
    corner_radius=0
)

conteudo.pack(
    side="left",
    fill="both",
    expand=True
)


# =========================
# FUNÇÕES DAS TELAS
# =========================


def limpar_tela():

    for widget in conteudo.winfo_children():
        widget.destroy()



def criar_card(
    pai,
    titulo,
    valor,
    cor
):

    card = ctk.CTkFrame(
        pai,
        width=220,
        height=150,
        corner_radius=20,
        fg_color=cor
    )

    card.pack(
        side="left",
        padx=20,
        pady=20
    )


    ctk.CTkLabel(
        card,
        text=titulo,
        font=(
            "Segoe UI",
            14,
            "bold"
        ),
        text_color="white"
    ).pack(
        pady=(30,5)
    )


    ctk.CTkLabel(
        card,
        text=valor,
        font=(
            "Segoe UI",
            38,
            "bold"
        ),
        text_color="white"
    ).pack()

def carregar_indicadores():

    conexao = sqlite3.connect(
        BANCO
    )

    cursor = conexao.cursor()


    # TOTAL

    cursor.execute(
        "SELECT COUNT(*) FROM cirurgias"
    )

    total = cursor.fetchone()[0]


    # AGENDADAS

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM cirurgias
        WHERE status = 'Agendada'
        """
    )

    agendadas = cursor.fetchone()[0]


    # CONFIRMADAS

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM cirurgias
        WHERE status = 'Confirmada'
        """
    )

    confirmadas = cursor.fetchone()[0]


    # CANCELADAS

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM cirurgias
        WHERE status = 'Cancelada'
        """
    )

    canceladas = cursor.fetchone()[0]


    conexao.close()


    print(
        "INDICADORES:",
        total,
        agendadas,
        confirmadas,
        canceladas
    )


    return (
        total,
        agendadas,
        confirmadas,
        canceladas
    )

def mostrar_dashboard():

    limpar_tela()

    total, agendadas, confirmadas, canceladas = carregar_indicadores()
 
    titulo = ctk.CTkLabel(
        conteudo,
        text="📊 Dashboard",
        font=(
            "Segoe UI",
            32,
            "bold"
        ),
        text_color=TEXTO
    )

    titulo.pack(
        anchor="w",
        padx=60,
        pady=(40,10)
    )

    ctk.CTkLabel(
        conteudo,
        text="Resumo das cirurgias e indicadores do dia",
        font=(
            "Segoe UI",
            14
        ),
        text_color="#6B7280"
    ).pack(
        anchor="w",
        padx=60
    )

    frame_cards = ctk.CTkFrame(
        conteudo,
        fg_color="transparent"
    )

    frame_cards.pack(
        pady=40
    )

    total, agendadas, confirmadas, canceladas = carregar_indicadores()

    criar_card(
        frame_cards,
        "🩺 Cirurgias",
        total,
        ROXO
    )


    criar_card(
        frame_cards,
        "📅 Agendadas",
        agendadas,
        "#F59E0B"
    )


    criar_card(
        frame_cards,
        "✅ Confirmadas",
        confirmadas,
        "#22C55E"
    )


    criar_card(
        frame_cards,
        "❌ Canceladas",
        canceladas,
        "#EF4444"
    )



def mostrar_agenda():

    limpar_tela()

    ctk.CTkLabel(
        conteudo,
        text="📅 Agenda Cirúrgica",
        font=(
            "Segoe UI",
            30,
            "bold"
        )
    ).pack(
        pady=60
    )



def mostrar_calendario():

    limpar_tela()

    ctk.CTkLabel(
        conteudo,
        text="🗓 Calendário",
        font=(
            "Segoe UI",
            30,
            "bold"
        )
    ).pack(
        pady=60
    )



def mostrar_usuarios():

    limpar_tela()

    ctk.CTkLabel(
        conteudo,
        text="👥 Usuários",
        font=(
            "Segoe UI",
            30,
            "bold"
        )
    ).pack(
        pady=60
    )



def mostrar_relatorios():

    limpar_tela()

    ctk.CTkLabel(
        conteudo,
        text="📄 Relatórios",
        font=(
            "Segoe UI",
            30,
            "bold"
        )
    ).pack(
        pady=60
    )


def sair_do_sistema():

    resposta = messagebox.askyesno(
        "Encerrar sessão",
        "Deseja realmente sair do SurgiFlow?"
    )

    if resposta:
        janela.destroy()


# =========================
# BOTÕES SIDEBAR
# =========================


criar_botao(
    "📊 Dashboard",
    mostrar_dashboard
)

criar_botao(
    "📅 Agenda",
    mostrar_agenda
)

criar_botao(
    "🗓 Calendário",
    mostrar_calendario
)

criar_botao(
    "👥 Usuários",
    mostrar_usuarios
)

criar_botao(
    "📄 Relatórios",
    mostrar_relatorios
)

# espaço

ctk.CTkLabel(
    sidebar,
    text="",
).pack(
    expand=True
)

# =========================
# RODAPÉ SIDEBAR
# =========================

rodape = ctk.CTkFrame(
    sidebar,
    fg_color="transparent"
)

rodape.pack(
    side="bottom",
    fill="x",
    padx=15,
    pady=20
)

#Linha

ctk.CTkFrame(
    rodape,
    height=2,
    fg_color="#7E69C6"
).pack(
    fill="x",
    pady=(0,15)
)

# USUÁRIO

usuario = ctk.CTkLabel(
    rodape,
    text="👤  " + USUARIO_LOGADO,
    font=(
        "Segoe UI",
        15,
        "bold"
    ),
    text_color="white"
)

usuario.pack(
    anchor="w"
)

# CARGO

cargo = ctk.CTkLabel(
    rodape,
    text="Administrador",
    font=(
        "Segoe UI",
        11
    ),
    text_color="#D8CCFF"
)

cargo.pack(
    anchor="w",
    pady=(0,12)
)

# BOTÃO NOTIFICAÇÃO

botao_notificacao = ctk.CTkButton(
    rodape,
    text="🔔  Notificações (2)",
    height=35,
    fg_color="transparent",
    hover_color="#7E69C6",
    anchor="w"
)

botao_notificacao.pack(
    fill="x",
    pady=2
)

# BOTÃO CONFIGURAÇÃO

botao_config = ctk.CTkButton(
    rodape,
    text="⚙ Configurações",
    height=35,
    fg_color="transparent",
    hover_color="#7E69C6",
    anchor="w"
)

botao_config.pack(
    fill="x",
    pady=2
)

# BOTÃO TROCAR USUÁRIO

botao_usuario = ctk.CTkButton(
    rodape,
    text="🔄 Trocar usuário",
    height=35,
    fg_color="transparent",
    hover_color="#7E69C6",
    anchor="w"
)

botao_usuario.pack(
    fill="x",
    pady=2
)

# BOTÃO BLOQUEAR

botao_bloquear = ctk.CTkButton(
    rodape,
    text="🔒 Bloquear",
    height=35,
    fg_color="transparent",
    hover_color="#7E69C6",
    anchor="w"
)

botao_bloquear.pack(
    fill="x",
    pady=2
)

# BOTÃO SAIR

botao_sair = ctk.CTkButton(
    rodape,
    text="🚪 Sair",
    fg_color="#D64550",
    hover_color="#B92F3A",
    text_color="white",
    height=38,
    command=sair_do_sistema
)

botao_sair.pack(
    fill="x",
    pady=(8,0)
)

# abre dashboard inicial

mostrar_dashboard()



# =========================
# START
# =========================

app.mainloop()