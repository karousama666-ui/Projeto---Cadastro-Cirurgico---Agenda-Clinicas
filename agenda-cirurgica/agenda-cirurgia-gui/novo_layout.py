import customtkinter as ctk
import sqlite3
import os


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

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


BANCO = os.path.join(
    BASE_DIR,
    "cirurgias.db"
)

print(
    "BANCO USADO:",
    BANCO
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
    fg_color=ROXO
)

sidebar.pack(
    side="left",
    fill="y"
)


# LOGO TEXTO

titulo = ctk.CTkLabel(
    sidebar,
    text="🩺\nSurgiFlow",
    font=(
        "Segoe UI",
        28,
        "bold"
    ),
    text_color="white"
)

titulo.pack(
    pady=40
)

subtitulo = ctk.CTkLabel(
    sidebar,
    text="Gestão\nCirúrgica",
    font=(
        "Segoe UI",
        14
    ),
    text_color=LILAS
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
        fg_color="#E9D5FF",
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



# abre dashboard inicial

mostrar_dashboard()



# =========================
# START
# =========================

app.mainloop()