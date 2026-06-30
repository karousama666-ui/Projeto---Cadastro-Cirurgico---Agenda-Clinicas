import customtkinter as ctk
from PIL import Image
import sqlite3
import os

# ======================
# CONFIGURAÇÃO
# ======================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BANCO = os.path.join(
    BASE_DIR,
    "cirurgias.db"
)

CAMINHO_LOGO = os.path.join(
    BASE_DIR,
    "logo_surgiflow.png"
)

ROXO = "#6750C8"
FUNDO = "#A195EC"

# ======================
# JANELA
# ======================

app = ctk.CTk()

app.geometry("520x650")

app.title("SurgiFlow")

app.configure(fg_color=FUNDO)

app.resizable(False, False)

# ======================
# LOGO
# ======================

logo = ctk.CTkImage(
    light_image=Image.open(CAMINHO_LOGO),
    dark_image=Image.open(CAMINHO_LOGO),
    size=(250,250)
)

ctk.CTkLabel(
    app,
    image=logo,
    text=""
).pack(
    pady=(25,10)
)

# ======================
# TÍTULO
# ======================

ctk.CTkLabel(
    app,
    text="Bem-vindo",
    font=(
        "Segoe UI",
        30,
        "bold"
    )
).pack()

ctk.CTkLabel(
    app,
    text="Faça login para continuar",
    font=(
        "Segoe UI",
        14
    ),
    text_color="#FFFFFF"
).pack(
    pady=(0,30)
)

# ======================
# USUÁRIO
# ======================

usuario = ctk.CTkEntry(
    app,
    width=320,
    height=42,
    placeholder_text="Usuário"
)

usuario.pack(
    pady=10
)

# ======================
# SENHA
# ======================

senha = ctk.CTkEntry(
    app,
    width=320,
    height=42,
    show="•",
    placeholder_text="Senha"
)

senha.pack(
    pady=10
)

# ======================
# BOTÃO
# ======================

botao = ctk.CTkButton(
    app,
    text="Entrar",
    width=320,
    height=45,
    fg_color=ROXO,
    hover_color="#5840B7"
)

botao.pack(
    pady=30
)

app.mainloop()