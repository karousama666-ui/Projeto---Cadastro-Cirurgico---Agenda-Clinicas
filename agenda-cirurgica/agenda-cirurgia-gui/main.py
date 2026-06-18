import sqlite3
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
import json
from datetime import datetime
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from openpyxl import Workbook
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
from PIL import Image, ImageTk


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BANCO = os.path.join(
    BASE_DIR,
    "cirurgias.db"
)

cirurgias = []
indice_edicao = None

def salvar_dados():

    with open("cirurgias.json", "w", encoding="utf-8") as arquivo:
        
        json.dump(
            cirurgias,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def gerar_grafico_status():

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM cirurgias
        GROUP BY status
    """)

    dados = cursor.fetchall()

    conexao.close()

    labels = []
    valores = []

    for status, quantidade in dados:

        labels.append(status)

        valores.append(quantidade)

    figura = Figure(
        figsize=(5,4),
        dpi=100
    )

    grafico = figura.add_subplot(111)

    grafico.pie(
        valores,
        labels=labels,
        autopct="%1.1f%%"
    )

    grafico.set_title(
        "Cirurgias por Status"
    )

    for widget in frame_grafico_status.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(
        figura,
        master=frame_grafico_status
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )

def abrir_login():

    global janela_login
    global entry_usuario
    global entry_senha

    janela_login = tk.Toplevel(janela)

    janela_login.title("Login")
    janela_login.geometry("300x200")
    janela_login.grab_set()

    ttk.Label(
        janela_login,
        text="Usuário"
    ).pack()

    entry_usuario = ttk.Entry(
        janela_login
    )

    entry_usuario.pack()

    ttk.Label(
        janela_login,
        text="Senha"
    ).pack()

    entry_senha = ttk.Entry(
        janela_login,
        show="*"
    )

    entry_senha.pack()

    ttk.Button(
        janela_login,
        text="Entrar",
        command=verificar_login,
        bootstyle="success"
    ).pack(pady=15)

    def entrar():

        usuario = entry_usuario.get()

        senha = entry_senha.get()

        if validar_login(
            usuario,
            senha
        ):

            janela_login.destroy()

            abrir_sistema()

        else:

            messagebox.showerror(
                "Erro",
                "Usuário ou senha inválidos"
            )

    ttk.Button(
        janela_login,
        text="Entrar",
        command=entrar
    ).pack(pady=15)

    janela_login.mainloop()
    

janela = ttk.Window(
    themename="lumen"
)

caminho_logo = os.path.join(
    BASE_DIR,
    "logo_surgiflow.png"
)

imagem = Image.open(
    caminho_logo
)

imagem = imagem.resize(
    (900, 180)
)

logo = ImageTk.PhotoImage(
    imagem
)


style = ttk.Style()

style.configure(
    "TButton",
    font=("Segoe UI", 10),
    padding=10
)


janela.withdraw()

janela.title("Agenda Cirúrgica")
janela.state("zoomed")

header = ttk.Frame(
    janela,
    padding=15
)

header.pack(
    fill="x",
    pady=5
)

logo_label = ttk.Label(
    header,
    image=logo
)

logo_label.pack()

notebook = ttk.Notebook(janela)

# ABA CADASTRO

aba_cadastro = ttk.Frame(notebook)

notebook.add(
    aba_cadastro,
    text="📋 Cadastro"
)

frame_cadastro = ttk.LabelFrame(
    aba_cadastro,
    text="Cadastro de Cirurgia"
)

frame_cadastro.pack(
    padx=20,
    pady=20,
    fill="x"
)

conteudo_cadastro = ttk.Frame(
    frame_cadastro
)

conteudo_cadastro.pack(
    padx=20,
    pady=20
)

# ABA AGENDA

aba_agenda = ttk.Frame(notebook)

notebook.add(
    aba_agenda,
    text="🏥 Agenda"
)

# ABA RELATÓRIOS

aba_relatorios = ttk.Frame(notebook)

notebook.add(
    aba_relatorios,
    text="📊 Relatórios"
)

# ABA USUÁRIOS

aba_usuarios = ttk.Frame(notebook)

notebook.add(
    aba_usuarios,
    text="👥 Usuários"
)

frame_usuarios = ttk.LabelFrame(
    aba_usuarios,
    text="Gerenciamento de Usuários"
)

frame_usuarios.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

frame_cadastro_usuario = ttk.LabelFrame(
    frame_usuarios,
    text="Cadastro de Usuário"
)

frame_cadastro_usuario.pack(
    fill="x",
    padx=10,
    pady=10
)

ttk.Label(
    frame_cadastro_usuario,
    text="Usuário"
).pack()

entry_usuario_novo = ttk.Entry(
    frame_cadastro_usuario,
    width=40
)

entry_usuario_novo.pack(
    pady=5
)

ttk.Label(
    frame_cadastro_usuario,
    text="Senha"
).pack()

entry_senha_nova = ttk.Entry(
    frame_cadastro_usuario,
    width=40
)

entry_senha_nova.pack(
    pady=5
)

ttk.Label(
    frame_cadastro_usuario,
    text="Nível"
).pack()

combo_nivel_novo = ttk.Combobox(
    frame_cadastro_usuario,
    values=[
        "administrador",
        "usuario"
    ],
    state="readonly"
)

combo_nivel_novo.pack(
    pady=5
)

ttk.Button(
    frame_cadastro_usuario,
    text="Cadastrar Usuário"
).pack(
    pady=10
)


frame_lista_usuarios = ttk.LabelFrame(
    frame_usuarios,
    text="Usuários Cadastrados"
)

frame_lista_usuarios.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

tabela_usuarios = ttk.Treeview(
    frame_lista_usuarios,
    columns=(
        "ID",
        "Usuario",
        "Nivel"
    ),
    show="headings"
)

tabela_usuarios.heading(
    "ID",
    text="ID"
)

tabela_usuarios.heading(
    "Usuario",
    text="Usuário"
)

tabela_usuarios.heading(
    "Nivel",
    text="Nível"
)

tabela_usuarios.pack(
    fill="both",
    expand=True,
    pady=10
)

frame_botoes_usuario = ttk.Frame(
    frame_lista_usuarios
)

frame_botoes_usuario.pack(
    pady=10
)




notebook.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

style.configure(
    "TNotebook.Tab",
    font=("Segoe UI", 11),
    padding=[15, 8]
)

titulo_relatorios = ttk.Label(
    aba_relatorios,
    text="Relatórios",
    font=("Arial", 16)
)

titulo_relatorios.pack(pady=10)

label_total = ttk.Label(
    aba_relatorios,
    text="Total de Cirurgias: 0",
    font=("Arial", 12)
)

label_total.pack(pady=10)

label_hospital = ttk.Label(
    aba_relatorios,
    text="Hospital mais utilizado: -",
    font=("Arial", 12)
)

label_hospital.pack(pady=5)

label_convenio = ttk.Label(
    aba_relatorios,
    text="Convênio mais utilizado: -",
    font=("Arial", 12)
)

label_convenio.pack(pady=5)

label_medico = ttk.Label(
    aba_relatorios,
    text="Médico com mais cirurgias: -",
    font=("Arial", 12)
)

label_medico.pack(pady=5)

label_agendadas = ttk.Label(
    aba_relatorios,
    text="Agendadas: 0"
)

label_agendadas.pack(pady=5)

label_confirmadas = ttk.Label(
    aba_relatorios,
    text="Confirmadas: 0"
)

label_confirmadas.pack(pady=5)

label_realizadas = ttk.Label(
    aba_relatorios,
    text="Realizadas: 0"
)

label_realizadas.pack(pady=5)

label_canceladas = ttk.Label(
    aba_relatorios,
    text="Canceladas: 0"
)

label_canceladas.pack(pady=5)

# COLOCA AQUI

frame_grafico_status = tk.Frame(
    aba_relatorios
)

frame_grafico_status.pack(
    fill="both",
    expand=True,
    pady=20
)



# Título

titulo = ttk.Label(aba_cadastro, text="Cadastro Cirúrgico", font=("Arial", 16))
titulo.pack(pady=10)    

# Campo Paciente

ttk.Label(frame_cadastro, text="Paciente:").pack()

entrada_paciente = tk.Entry(frame_cadastro, width=40)
entrada_paciente.pack()

# Campo Médico

ttk.Label(frame_cadastro, text="Médico:").pack()

entrada_medico = tk.Entry(frame_cadastro, width=40)
entrada_medico.pack()

# Campo Hospital

ttk.Label(frame_cadastro, text="Hospital:").pack()

entrada_hospital = tk.Entry(frame_cadastro, width=40)
entrada_hospital.pack()

# Campo Convênio

ttk.Label(frame_cadastro, text="Convênio:").pack()

entrada_convenio = tk.Entry(frame_cadastro, width=40)
entrada_convenio.pack()

# Campo Data da Cirurgia

ttk.Label(frame_cadastro, text="Data da Cirurgia:").pack()

entrada_data = DateEntry(
    frame_cadastro,
    width=20,
    date_pattern="dd/mm/yyyy"
)

entrada_data.pack()

# Campo Horário da Cirurgia

ttk.Label(frame_cadastro, text="Horário da Cirurgia:").pack()

entrada_horario = tk.Entry(frame_cadastro, width=40)
entrada_horario.pack()

# Campo Procedimento

ttk.Label(frame_cadastro, text="Procedimento:").pack()

entrada_procedimento = tk.Entry(frame_cadastro, width=40)
entrada_procedimento.pack()

# NOVO CAMPO STATUS

ttk.Label(frame_cadastro, text="Status:").pack()

combo_status = ttk.Combobox(
    frame_cadastro,
    values=[
        "Agendada",
        "Confirmada",
        "Realizada",
        "Cancelada"
    ],
    state="readonly",
    width=37
)

combo_status.pack()

combo_status.set("Agendada")

# Agenda

titulo_agenda = ttk.Label(
    aba_agenda,
    text="Agenda de Cirurgias",
    font=("Arial", 16)
)

titulo_agenda.pack(pady=10)

def cadastrar():

    paciente = entrada_paciente.get()
    medico = entrada_medico.get()
    hospital = entrada_hospital.get()
    convenio = entrada_convenio.get()
    data = entrada_data.get()
    horario = entrada_horario.get()
    procedimento = entrada_procedimento.get()
    status = combo_status.get()

    print("Status:", status)

    # Campos obrigatórios

    if (
        not paciente or
        not medico or
        not hospital or
        not convenio or
        not data or
        not horario or
        not procedimento
    ):
        messagebox.showerror(
            "Erro",
            "Todos os campos devem ser preenchidos!"
        )
        return

    # Validação da data



    try:

        resultado = datetime.strptime(
            data,
            "%d/%m/%Y"
        )

        print("Data Válida:", resultado)


    except ValueError:

        messagebox.showerror(
            "Erro",
            "Data inválida.\nUse DD/MM/AAAA."
        )

        return

    # Validação do horário

    try:
        datetime.strptime(
            horario,
            "%H:%M"
        )

    except ValueError:

        messagebox.showerror(
            "Erro",
            "Horário inválido.\nUse HH:MM."
        )

        return

    print("Cadastro Realizado:")
    print(f"Paciente: {paciente}")
    print(f"Médico: {medico}")
    print(f"Hospital: {hospital}")
    print(f"Convênio: {convenio}")
    print(f"Data da Cirurgia: {data}")
    print(f"Horário da Cirurgia: {horario}")
    print(f"Procedimento: {procedimento}")

    cirurgia = {
        "paciente": paciente,
        "medico": medico,
        "hospital": hospital,
        "convenio": convenio,
        "data": data,
        "horario": horario,
        "procedimento": procedimento,
        "status": status
    }

    global indice_edicao

    if indice_edicao is not None:

        atualizar_cirurgia_banco(
            cirurgia,
            id_cirurgia
        )

        indice_edicao = None

    else:

        salvar_cirurgia_no_banco(cirurgia)

    listar_cirurgias_banco()
    atualizar_tabela()
    atualizar_relatorios()

    entrada_paciente.delete(0, tk.END)
    entrada_medico.delete(0, tk.END)
    entrada_hospital.delete(0, tk.END)
    entrada_convenio.delete(0, tk.END)
    entrada_data.delete(0, tk.END)
    entrada_horario.delete(0, tk.END)
    entrada_procedimento.delete(0, tk.END)

    messagebox.showinfo(
        "Sucesso",
        "Cirurgia cadastrada com sucesso!"
    )

    print(cirurgias)

def carregar_dados():

    global cirurgias

    try:

        with open ("cirurgias.json", "r", encoding="utf-8") as arquivo:

            cirurgias = json.load(arquivo)

    except FileNotFoundError:

        cirurgias = []

cirurgias = []
# carregar_dados()

def excluir_cirurgia():
    
    item_selecionado = tabela.selection()

    if not item_selecionado:
        print("Nenhuma cirurgia selecionada para exclusão.")
        return
    
    resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir a cirurgia do paciente?")

    if not resposta:
        return
    
    valores = tabela.item(item_selecionado [0], "values")

    id_cirurgia = valores[0]
    print("Valores:", valores)
    print("ID capturado:", id_cirurgia)

    excluir_cirurgia_banco(id_cirurgia)
    
    
    for cirurgia in cirurgias:
        if (cirurgia["paciente"] == valores[0]):
            cirurgias.remove(cirurgia)
            break
    
    # salvar_dados()
    atualizar_tabela()
    atualizar_relatorios()


    messagebox.showinfo("Sucesso", "Cirurgia excluída com sucesso!")

def editar_cirurgia():
    item_selecionado = tabela.selection()

    if not item_selecionado:
        print("Nenhuma cirurgia selecionada para edição.")
        return
    
    valores = tabela.item(item_selecionado[0], "values")

    global id_cirurgia
    id_cirurgia = valores[0]



    global indice_edicao
    indice_edicao = tabela.index(item_selecionado[0])
    print("Editando índice: ", indice_edicao)

    entrada_paciente.delete(0, tk.END)
    entrada_paciente.insert(0, valores[1])  
    entrada_medico.delete(0, tk.END)
    entrada_medico.insert(0, valores[2])
    entrada_hospital.delete(0, tk.END)
    entrada_hospital.insert(0, valores[3])
    entrada_convenio.delete(0, tk.END)
    entrada_convenio.insert(0, valores[4])
    entrada_data.delete(0, tk.END)
    entrada_data.insert(0, valores[5])
    entrada_horario.delete(0, tk.END)
    entrada_horario.insert(0, valores[6])
    entrada_procedimento.delete(0, tk.END)
    entrada_procedimento.insert(0, valores[7])

def buscar_paciente():
    nome_busca = entrada_busca.get().lower()

    for item in tabela.get_children():
        tabela.delete(item)

    for cirurgia in cirurgias:
        if nome_busca in cirurgia["paciente"].lower():
            tabela.insert("", "end", values=(
                cirurgia["paciente"],
                cirurgia["medico"],
                cirurgia["hospital"],
                cirurgia["convenio"],
                cirurgia["data"],
                cirurgia["horario"],
                cirurgia["procedimento"]
            ))

def mostrar_todos():
    atualizar_tabela()
    entrada_busca.delete(0, tk.END)    
    
def buscar_em_tempo_real(event=None):
    nome_busca = entrada_busca.get().lower()
    for item in tabela.get_children():
        tabela.delete(item)
        
    for cirurgia in cirurgias:
        if nome_busca == "" or nome_busca in cirurgia["paciente"].lower():
                tabela.insert("", "end", values=(
                    cirurgia["paciente"],
                    cirurgia["medico"],
                    cirurgia["hospital"],
                    cirurgia["convenio"],
                    cirurgia["data"],
                    cirurgia["horario"],
                    cirurgia["procedimento"]
                ))

def atualizar_relatorios():

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM cirurgias
    WHERE status = 'Agendada'
    """)
    agendadas = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM cirurgias
    WHERE status = 'Confirmada'
    """)
    confirmadas = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM cirurgias
    WHERE status = 'Realizada'
    """)
    realizadas = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM cirurgias
    WHERE status = 'Cancelada'
    """)
    canceladas = cursor.fetchone()[0]

    # Total de cirurgias
    cursor.execute("SELECT COUNT(*) FROM cirurgias")
    total = cursor.fetchone()[0]

    # Hospital mais utilizado
    cursor.execute("""
        SELECT hospital, COUNT(*)
        FROM cirurgias
        GROUP BY hospital
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    hospital = cursor.fetchone()

    # Convênio mais utilizado
    cursor.execute("""
        SELECT convenio, COUNT(*)
        FROM cirurgias
        GROUP BY convenio
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    convenio = cursor.fetchone()

    # Médico com mais cirurgias
    cursor.execute("""
        SELECT medico, COUNT(*)
        FROM cirurgias
        GROUP BY medico
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    medico = cursor.fetchone()

    label_total.config(
        text=f"Total de Cirurgias: {total}"
    )

    label_agendadas.config(
        text=f"Agendadas: {agendadas}"
    )

    label_confirmadas.config(
        text=f"Confirmadas: {confirmadas}"
    )

    label_realizadas.config(
        text=f"Realizadas: {realizadas}"
    )

    label_canceladas.config(
        text=f"Canceladas: {canceladas}"
    )

    if hospital:
        label_hospital.config(
            text=f"Hospital mais utilizado: {hospital[0]}"
        )

    if convenio:
        label_convenio.config(
            text=f"Convênio mais utilizado: {convenio[0]}"
        )

    if medico:
        label_medico.config(
            text=f"Médico com mais cirurgias: {medico[0]}"
        )

    conexao.close()

gerar_grafico_status()


from datetime import datetime, timedelta

def verificar_cirurgias_proximas():

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT paciente, data
        FROM cirurgias
    """)

    registros = cursor.fetchall()

    conexao.close()

    hoje = datetime.now()

    avisos = []

    for paciente, data in registros:

        try:

            data_cirurgia = datetime.strptime(
                data,
                "%d/%m/%Y"
            )

            diferenca = (
                data_cirurgia - hoje
            ).days

            if 0 <= diferenca <= 7:

                avisos.append(
                    f"{paciente} - {data}"
                )

        except:
            pass

    return avisos


def exportar_excel():

    wb = Workbook()
    ws = wb.active

    ws.title = "Cirurgias"

    ws.append([
        "ID",
        "Paciente",
        "Médico",
        "Hospital",
        "Convênio",
        "Data",
        "Horário",
        "Procedimento"
    ])

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, paciente, medico, hospital,
               convenio, data, horario, procedimento
        FROM cirurgias
    """)

    registros = cursor.fetchall()

    for registro in registros:
        ws.append(registro)

    conexao.close()

    wb.save("relatorio_cirurgias.xlsx")

    messagebox.showinfo(
        "Sucesso",
        "Relatório Excel gerado com sucesso!"
    )

def gerar_grafico_hospitais():

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT hospital, COUNT(*)
        FROM cirurgias
        GROUP BY hospital
        ORDER BY COUNT(*) DESC
    """)

    dados = cursor.fetchall()

    conexao.close()

    hospitais = []
    quantidades = []

    for hospital, quantidade in dados:
        hospitais.append(hospital)
        quantidades.append(quantidade)

    figura = Figure(figsize=(6, 4), dpi=100)

    grafico = figura.add_subplot(111)

    grafico.bar(hospitais, quantidades)

    grafico.set_title("Cirurgias por Hospital")
    grafico.set_xlabel("Hospital")
    grafico.set_ylabel("Quantidade")

    for widget in frame_grafico.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(
        figura,
        master=frame_grafico
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )


def alterar_status():

    item_selecionado = tabela.selection()

    if not item_selecionado:
        messagebox.showwarning(
            "Aviso",
            "Selecione uma cirurgia."
        )
        return

    valores = tabela.item(
        item_selecionado[0],
        "values"
    )

    id_cirurgia = valores[0]

    janela_status = tk.Toplevel(janela)

    janela_status.title("Alterar Status")
    janela_status.geometry("300x200")

    ttk.Label(
        janela_status,
        text="Novo Status:"
    ).pack(pady=10)

    status_var = tk.StringVar()

    combo_status = ttk.Combobox(
        janela_status,
        textvariable=status_var,
        values=[
            "Agendada",
            "Confirmada",
            "Realizada",
            "Cancelada"
        ]
    )

    combo_status.pack(pady=10)

    ttk.Button(
        janela_status,
        text="Salvar",
        command=lambda: salvar_novo_status(
            id_cirurgia,
            status_var.get(),
            janela_status
    )
).pack(pady=10)


    # Widgets

entrada_busca = tk.Entry(aba_agenda, width=40)
entrada_busca.pack()

entrada_busca.bind(
    "<KeyRelease>",
    buscar_em_tempo_real
)
    
from tkinter import messagebox

def abrir_filtros():

    janela_filtros = tk.Toplevel(janela)

    janela_filtros.title("Filtros")

    janela_filtros.geometry("350x400")

    agendada_var = tk.BooleanVar(value=True)
    confirmada_var = tk.BooleanVar(value=True)
    realizada_var = tk.BooleanVar(value=True)
    cancelada_var = tk.BooleanVar(value=True)

    tk.Checkbutton(
        janela_filtros,
        text="Agendada",
        variable=agendada_var
    ).pack(anchor="w", padx=20, pady=5)

    tk.Checkbutton(
        janela_filtros,
        text="Confirmada",
        variable=confirmada_var
    ).pack(anchor="w", padx=20, pady=5)

    tk.Checkbutton(
        janela_filtros,
        text="Realizada",
        variable=realizada_var
    ).pack(anchor="w", padx=20, pady=5)

    tk.Checkbutton(
        janela_filtros,
        text="Cancelada",
        variable=cancelada_var
    ).pack(anchor="w", padx=20, pady=5)

    ttk.Label(
        janela_filtros,
        text="Médico"
    ).pack(pady=(10,0))

    combo_medico = ttk.Combobox(
        janela_filtros
    )

    combo_medico.pack(pady=5)

    ttk.Label(
        janela_filtros,
        text="Hospital"
    ).pack(pady=(10,0))

    combo_hospital = ttk.Combobox(
        janela_filtros
    )

    combo_hospital.pack(pady=5)

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
    SELECT DISTINCT medico
    FROM cirurgias
    ORDER BY medico
    """)

    medicos = [
        linha[0]
        for linha in cursor.fetchall()
    ]

    cursor.execute("""
    SELECT DISTINCT hospital
    FROM cirurgias
    ORDER BY hospital
    """)

    hospitais = [
        linha[0]
        for linha in cursor.fetchall()
    ]

    conexao.close()

    combo_medico["values"] = [
        "Todos"
    ] + medicos

    combo_hospital["values"] = [
        "Todos"
    ] + hospitais

    combo_medico.set("Todos")

    combo_hospital.set("Todos")

    ttk.Button(
        janela_filtros,
        text="Aplicar",
        command=lambda: aplicar_filtros(
            agendada_var.get(),
            confirmada_var.get(),
            realizada_var.get(),
            cancelada_var.get(),
            combo_medico.get(),
            combo_hospital.get()
    )
).pack(pady=15)
    
    ttk.Button(
        janela_filtros,
        text="Limpar Filtros",
        command=lambda: atualizar_tabela()
).pack(pady=5)




def aplicar_filtros(
    agendada,
    confirmada,
    realizada,
    cancelada,
    medico,
    hospital
):

    for item in tabela.get_children():
        tabela.delete(item)

    registros = carregar_cirurgias_do_banco()

    for registro in registros:

        status = registro[8]

        if status == "Agendada" and not agendada:
            continue

        if status == "Confirmada" and not confirmada:
            continue

        if status == "Realizada" and not realizada:
            continue

        if status == "Cancelada" and not cancelada:
            continue

        if medico != "Todos":

            if registro[2] != medico:
                continue

        if hospital != "Todos":

            if registro[3] != hospital:
                continue

        tabela.insert(
            "",
            "end",
            values=registro
        )
    

def abrir_edicao(event):

    item = tabela.selection()

    if not item:
        return

    valores = tabela.item(
        item[0],
        "values"
    )

    janela_edicao = tk.Toplevel(janela)

    janela_edicao.focus_force()

    janela_edicao.title("Editar Cirurgia")

    janela_edicao.geometry("500x700")

    ttk.Label(
        janela_edicao,
        text="Paciente"
    ).pack()

    entry_paciente = tk.Entry(
        janela_edicao,
        width=40
    )

    entry_paciente.pack()

    entry_paciente.focus_set()

    print("STATE:", entry_paciente["state"])

    entry_paciente.insert(
        0,
        valores[1]
    )

    ttk.Label(
        janela_edicao,
        text="Médico"
    ).pack()

    entry_medico = tk.Entry(
        janela_edicao,
        width=40
    )

    entry_medico.pack()

    entry_medico.insert(
        0,
        valores[2]
    )

    ttk.Label(
        janela_edicao,
        text="Hospital"
    ).pack()

    entry_hospital = tk.Entry(
        janela_edicao,
        width=40
    )

    entry_hospital.pack()

    entry_hospital.insert(
        0,
        valores[3]
    )

    ttk.Label(
        janela_edicao,
        text="Convênio"
    ).pack()

    entry_convenio = tk.Entry(
        janela_edicao,
        width=40
    )

    entry_convenio.pack()

    entry_convenio.insert(
        0,
        valores[4]
    )

    ttk.Label(
        janela_edicao,
        text="Data"
    ).pack()

    entry_data = tk.Entry(
        janela_edicao,
        width=40
    )

    entry_data.pack()

    entry_data.insert(
        0,
        valores[5]
    )

    ttk.Label(
        janela_edicao,
        text="Horário"
    ).pack()

    entry_horario = tk.Entry(
        janela_edicao,
        width=40
    )

    entry_horario.pack()

    entry_horario.insert(
        0,
        valores[6]
    )

    ttk.Label(
        janela_edicao,
        text="Procedimento"
    ).pack()

    entry_procedimento = tk.Entry(
        janela_edicao,
        width=40
    )

    entry_procedimento.pack()

    entry_procedimento.insert(
        0,
        valores[7]
    )

    ttk.Label(
        janela_edicao,
        text="Status"
    ).pack()

    combo_status = ttk.Combobox(
        janela_edicao,
        values=[
            "Agendada",
            "Confirmada",
            "Realizada",
            "Cancelada"
        ]
    )

    combo_status.pack()

    combo_status.set(
        valores[8]
    )

    id_cirurgia = valores[0]

    def salvar_alteracoes():

        try:
            datetime.strptime(
                entry_data.get(),
                "%d/%m/%Y"
            )

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Data Inválida"
            )

            return
        
        try:
            datetime.strptime(
                entry_horario.get(),
                "%H:%M"
            )

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Horário inválido"
            )

            return

        conexao = sqlite3.connect(BANCO)

        cursor = conexao.cursor()

    

        cursor.execute("""
        UPDATE cirurgias
        SET
            paciente = ?,
            medico = ?,
            hospital = ?,
            convenio = ?,
            data = ?,
            horario = ?,
            procedimento = ?,
            status = ?
        WHERE id = ?
        """, (

            entry_paciente.get(),
            entry_medico.get(),
            entry_hospital.get(),
            entry_convenio.get(),
            entry_data.get(),
            entry_horario.get(),
            entry_procedimento.get(),
            combo_status.get(),
            id_cirurgia

        ))

        conexao.commit()

        conexao.close()

        atualizar_tabela()

        atualizar_relatorios()

        janela_edicao.destroy()

    ttk.Button(
        janela_edicao,
        text="Salvar Alterações",
        command=salvar_alteracoes
    ).pack(pady=20)


def salvar_usuario(usuario, senha, nivel):

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO usuarios (
        usuario,
        senha,
        nivel
    )
    VALUES (?, ?, ?)
    """, (

        usuario,
        senha,
        nivel

    ))

    conexao.commit()
    carregar_usuarios()

    conexao.close()

def abrir_cadastro_usuario():

    janela_usuario = tk.Toplevel(janela)

    janela_usuario.title("Cadastrar Usuário")

    janela_usuario.geometry("350x300")

    ttk.Label(
        janela_usuario,
        text="Usuário"
    ).pack(pady=5)

    entry_usuario = tk.Entry(
        janela_usuario
    )

    entry_usuario.pack()

    ttk.Label(
        janela_usuario,
        text="Senha"
    ).pack(pady=5)

    entry_senha = tk.Entry(
        janela_usuario
    )

    entry_senha.pack()

    ttk.Label(
        janela_usuario,
        text="Nível"
    ).pack(pady=5)

    combo_nivel = ttk.Combobox(
        janela_usuario,
        values=[
            "administrador",
            "usuario"
        ],
        state="readonly"
    )

    combo_nivel.pack()

    combo_nivel.set("usuario")

def cadastrar_usuario():

    salvar_usuario(

        entry_usuario.get(),

        entry_senha.get(),

        combo_nivel.get()

    )

    carregar_usuarios()

    messagebox.showinfo(
        "Sucesso",
        "Usuário cadastrado!"
    )

    janela_usuario.destroy()

def abrir_usuarios():

    global tabela_usuarios

    janela_usuarios = tk.Toplevel(janela)

    janela_usuarios.title("Usuários Cadastrados")

    janela_usuarios.geometry("500x350")

    tabela_usuarios = ttk.Treeview(
        janela_usuarios,
        columns=(
            "ID",
            "Usuário",
            "Nível"
        ),
        show="headings"
    )

    tabela_usuarios.heading(
        "ID",
        text="ID"
    )

    tabela_usuarios.heading(
        "Usuário",
        text="Usuário"
    )

    tabela_usuarios.heading(
        "Nível",
        text="Nível"
    )

    tabela_usuarios.pack(
        fill="both",
        expand=True,
        pady=10
    )

    carregar_usuarios()

    ttk.Button(
        janela_usuarios,
        text="Editar Usuário",
        command=editar_usuario,
        bootstyle="info"
    ).pack(pady=5)

    ttk.Button(
        janela_usuarios,
        text="Excluir Usuário",
        command=excluir_usuario,
        bootstyle="danger"
    ).pack(pady=5)

def carregar_usuarios():

    for item in tabela_usuarios.get_children():

        tabela_usuarios.delete(item)

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
    SELECT id, usuario, nivel
    FROM usuarios
    """)

    usuarios = cursor.fetchall()

    conexao.close()

    for usuario in usuarios:

        tabela_usuarios.insert(
            "",
            "end",
            values=(

                usuario[0],
                usuario[1],
                usuario[2]

            )
        )

def excluir_usuario():

    item = tabela_usuarios.selection()

    if not item:

        messagebox.showwarning(
            "Aviso",
            "Selecione um usuário."
        )

        return

    valores = tabela_usuarios.item(
        item[0],
        "values"
    )

    id_usuario = valores[0]

    usuario = valores[1]

    if usuario == "admin":

        messagebox.showerror(
            "Erro",
            "O usuário admin não pode ser excluído."
        )

        return

    resposta = messagebox.askyesno(
        "Confirmar",
        f"Excluir usuário {usuario}?"
    )

    if not resposta:

        return

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
    DELETE FROM usuarios
    WHERE id = ?
    """, (

        id_usuario,

    ))

    conexao.commit()

    conexao.close()

    tabela_usuarios.delete(item[0])

    messagebox.showinfo(
        "Sucesso",
        "Usuário excluído."
    )

def editar_usuario():

    item = tabela_usuarios.selection()

    if not item:

        messagebox.showwarning(
            "Aviso",
            "Selecione um usuário."
        )

        return

    valores = tabela_usuarios.item(
        item[0],
        "values"
    )

    id_usuario = valores[0]

    usuario = valores[1]

    janela_editar = tk.Toplevel(janela)

    janela_editar.title("Editar Usuário")

    janela_editar.geometry("400x400")

    ttk.Label(
        janela_editar,
        text=f"Usuário: {usuario}"
    ).pack(pady=10)

    ttk.Label(
        janela_editar,
        text="Nova Senha"
    ).pack()

    entry_senha = tk.Entry(
        janela_editar
    )

    entry_senha.pack()

    ttk.Label(
        janela_editar,
        text="Nível"
    ).pack()

    combo_nivel = ttk.Combobox(
        janela_editar,
        values=[
            "administrador",
            "usuario"
        ],
        state="readonly"
    )

    combo_nivel.pack()

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
    SELECT nivel
    FROM usuarios
    WHERE id = ?
    """, (

        id_usuario,

    ))

    resultado = cursor.fetchone()

    conexao.close()

    if resultado and resultado[0]:

        combo_nivel.set(
            resultado[0]
    )

    else:

        combo_nivel.set(
            "usuario"
    )
        

    def salvar():

        conexao = sqlite3.connect(BANCO)

        cursor = conexao.cursor()

        cursor.execute("""
        UPDATE usuarios
        SET
            senha = ?,
            nivel = ?
        WHERE id = ?
        """, (

            entry_senha.get(),
            combo_nivel.get(),
            id_usuario

        ))

        conexao.commit()

        conexao.close()

        messagebox.showinfo(
            "Sucesso",
            "Usuário atualizado."
        )

        janela_editar.destroy()

    ttk.Button(
        janela_editar,
        text="Salvar",
        command=salvar
    ).pack(pady=20)

ttk.Button(
    frame_botoes_usuario,
    text="Editar Usuário",
    command=editar_usuario,
    bootstyle="info"
).pack(
    side="left",
    padx=5
)

ttk.Button(
    frame_botoes_usuario,
    text="Excluir Usuário",
    command=excluir_usuario,
    bootstyle="danger"
).pack(
    side="left",
    padx=5
)

def verificar_login():

    global usuario_logado
    global nivel_logado

    usuario = entry_usuario.get()

    senha = entry_senha.get()

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
    SELECT nivel
    FROM usuarios
    WHERE usuario = ?
    AND senha = ?
    """, (

        usuario,
        senha

    ))

    resultado = cursor.fetchone()

    conexao.close()

    if resultado:

        usuario_logado = usuario

        nivel_logado = resultado[0]

        label_usuario.config(
            text=f"Usuário: {usuario_logado} ({nivel_logado})"
        )

        aplicar_permissoes()

        janela_login.destroy()

        janela.deiconify()

    else:

        messagebox.showerror(
            "Erro",
            "Usuário ou senha inválidos."
        )

def aplicar_permissoes():

    if nivel_logado == "usuario":

        botao_usuario.config(
            state="disabled"
        )

        botao_usuarios.config(
            state="disabled"
        )

    else:

        botao_usuario.config(
            state="normal"
        )

        botao_usuarios.config(
            state="normal"
        )

def sair():

    janela.destroy()


def trocar_usuario():

    janela.withdraw()

    abrir_login()

frame_sessao = ttk.Frame(
    janela
)

frame_sessao.pack(
    pady=10
)

botao_trocar_usuario = ttk.Button(
    frame_sessao,
    text="Trocar Usuário",
    command=trocar_usuario,
    bootstyle="warning"
)

botao_trocar_usuario.pack(
    side="left",
    padx=5
)

botao_sair = ttk.Button(
    frame_sessao,
    text="Sair",
    command=sair,
    bootstyle="danger"
)

botao_sair.pack(
    side="left",
    padx=5
)
    


# ABA CADASTRO

botao_cadastrar = ttk.Button(
    frame_cadastro,
    text="Cadastrar",
    command=cadastrar,
    bootstyle="success"
)

botao_cadastrar.pack(pady=10)

# ABA AGENDA

frame_acoes = ttk.Frame(
    aba_agenda
)

frame_acoes.pack(
    pady=10
)

botao_excluir = ttk.Button(
    frame_acoes,
    text="Excluir Cirurgia",
    command=excluir_cirurgia,
    bootstyle="danger"
)

botao_excluir.pack(
    side="left",
    padx=5
)

botao_editar = ttk.Button(
    frame_acoes,
    text="Editar Cirurgia",
    command=editar_cirurgia,
    bootstyle="info"
)

botao_editar.pack(
    side="left",
    padx=5
)

botao_buscar = ttk.Button(
    frame_acoes,
    text="Buscar",
    command=buscar_paciente,
    bootstyle="secondary"
)

botao_buscar.pack(
    side="left",
    padx=5
)



botao_filtros = ttk.Button(
    frame_acoes,
    text="Filtros",
    command=abrir_filtros,
    bootstyle="info"
)

botao_filtros.pack(
    side="left",
    padx=5
)

botao_mostrar = ttk.Button(
    frame_acoes,
    text="Mostrar Todos",
    command=mostrar_todos,
    bootstyle="success"
)

botao_mostrar.pack(
    side="left",
    padx=5
)

botao_status = ttk.Button(
    frame_acoes,
    text="Alterar Status",
    command=alterar_status,
    bootstyle="primary"
)

botao_status.pack(
    side="left",
    padx=5
)

botao_excel = ttk.Button(
    frame_acoes,
    text="Exportar Excel",
    command=exportar_excel,
    bootstyle="warning"
)

botao_excel.pack(
    side="left",
    padx=5
)

label_usuario = ttk.Label(
    janela,
    text=""
)

label_usuario.pack(pady=5)

botao_trocar_usuario = ttk.Button(
    janela,
    text="Trocar Usuário",
    command=trocar_usuario,
    bootstyle="dark"
)

# RODAPÉ

frame_sessao = ttk.Frame(
    janela
)

frame_sessao.pack(
    pady=10
)

botao_trocar_usuario = ttk.Button(
    frame_sessao,
    text="Trocar Usuário",
    command=trocar_usuario,
    bootstyle="warning"
)

botao_sair = ttk.Button(
    frame_sessao,
    text="Sair",
    command=sair,
    bootstyle="danger"
)

botao_sair.pack(
    side="left",
    padx=5
)

# BOTÃO GRÁFICO

botao_grafico = ttk.Button(
    aba_relatorios,
    text="Gráfico por Hospital",
    command=gerar_grafico_hospitais
)

botao_grafico.pack(pady=10)



tabela = ttk.Treeview(
    aba_agenda,
    columns=(
        "ID",
        "Paciente",
        "Médico",
        "Hospital",
        "Convênio",
        "Data",
        "Horário",
        "Procedimento",
        "Status"
    ),
    show="headings"
)
tabela.heading("ID", text="ID")
tabela.heading("Paciente", text="Paciente")
tabela.heading("Médico", text="Médico")
tabela.heading("Hospital", text="Hospital")
tabela.heading("Convênio", text="Convênio")
tabela.heading("Data", text="Data")
tabela.heading("Horário", text="Horário")  
tabela.heading("Procedimento", text="Procedimento")
tabela.heading("Status", text="Status")

tabela.tag_configure(
    "agendada",
    background="#FFF3CD"
)

tabela.tag_configure(
    "confirmada",
    background="#D1ECF1"
)

tabela.tag_configure(
    "realizada",
    background="#D4EDDA"
)

tabela.tag_configure(
    "cancelada",
    background="#F8D7DA"
)

tabela.bind(
    "<Double-1>",
    abrir_edicao
)

scrollbar = ttk.Scrollbar(aba_agenda, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=scrollbar.set)

tabela.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def carregar_cirurgias_do_banco():

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM cirurgias
    """)

    registros = cursor.fetchall()

    conexao.close()

    return registros

def atualizar_tabela():

    for item in tabela.get_children():
        tabela.delete(item)

    registros = carregar_cirurgias_do_banco()


    for r in registros:
        print(r)

    for registro in registros:

        status = registro[8]

        tag = ""

        if status == "Agendada":
           tag = "agendada"

        elif status == "Confirmada":
            tag = "confirmada"

        elif status == "Realizada":
            tag = "realizada"

        elif status == "Cancelada":
            tag = "cancelada"

        tabela.insert(
            "",
           "end",
           values=(
               registro[0],
               registro[1],
               registro[2],
               registro[3],
               registro[4],
               registro[5],
               registro[6],
               registro[7],
               registro[8]
        ),
        tags=(tag,)
    )

def criar_banco():

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    try:

        cursor.execute("""
        ALTER TABLE usuarios
        ADD COLUMN nivel TEXT
        """)

    except sqlite3.OperationalError:

        pass

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cirurgias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente TEXT,
            medico TEXT,
            hospital TEXT,
            convenio TEXT,
            data TEXT,
            horario TEXT,
            procedimento TEXT,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            senha TEXT,
            nivel TEXT
        )
    """)

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE usuario = ?
    """, ("admin",))

    usuario_admin = cursor.fetchone()

    if not usuario_admin:

        cursor.execute("""
            INSERT INTO usuarios (
                usuario,
                senha,
                nivel
            )
            VALUES (?, ?, ?)
        """, (

            "admin",
            "123",
            "administrador"

        ))

    cursor.execute("""
    UPDATE usuarios
    SET nivel = 'administrador'
    WHERE usuario = 'admin'
    """)

    conexao.commit()

    conexao.close()

def salvar_cirurgia_no_banco(cirurgia):
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute("""
    INSERT INTO cirurgias (
        paciente,
        medico,
        hospital,
        convenio,
        data,
        horario,
        procedimento,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    cirurgia["paciente"],
    cirurgia["medico"],
    cirurgia["hospital"],
    cirurgia["convenio"],
    cirurgia["data"],
    cirurgia["horario"],
    cirurgia["procedimento"],
    cirurgia["status"]
))
    conexao.commit()
    conexao.close()

def excluir_cirurgia_banco(id_cirurgia):

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM cirurgias WHERE id = ?",
        (id_cirurgia,)
    )

    conexao.commit()

    conexao.close()

def atualizar_cirurgia_banco(cirurgia, id_cirurgia):

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("""
    UPDATE cirurgias
    SET paciente = ?,
        medico = ?,
        hospital = ?,
        convenio = ?,
        data = ?,
        horario = ?,
        procedimento = ?
    WHERE id = ?
""", (
    cirurgia["paciente"],
    cirurgia["medico"],
    cirurgia["hospital"],
    cirurgia["convenio"],
    cirurgia["data"],
    cirurgia["horario"],
    cirurgia["procedimento"],
    id_cirurgia
))

    conexao.commit()
    conexao.close()

def listar_cirurgias_banco():
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM cirurgias")

    registros = cursor.fetchall()


    conexao.close()

def adicionar_coluna_status():

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()


    conexao.commit()
    conexao.close()

def verificar_colunas():

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("PRAGMA table_info(cirurgias)")

    colunas = cursor.fetchall()

    conexao.close()

def atualizar_status_banco(id_cirurgia, novo_status):

    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE cirurgias
        SET status = ?
        WHERE id = ?
    """, (
        novo_status,
        id_cirurgia
    ))

    conexao.commit()
    conexao.close()

def salvar_novo_status(
    id_cirurgia,
    novo_status,
    janela_status
):

    atualizar_status_banco(
        id_cirurgia,
        novo_status
    )

    atualizar_tabela()
    atualizar_relatorios()

    janela_status.destroy()

    messagebox.showinfo(
        "Sucesso",
        "Status atualizado com sucesso!"
    )

def validar_login(usuario, senha):

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
    SELECT *
    FROM usuarios
    WHERE usuario = ?
    AND senha = ?
    """, (usuario, senha))

    resultado = cursor.fetchone()

    conexao.close()

    return resultado


adicionar_coluna_status()
verificar_colunas()
adicionar_coluna_status()
verificar_colunas()
criar_banco()
atualizar_tabela()
atualizar_relatorios()

avisos = verificar_cirurgias_proximas()

if avisos:

    messagebox.showinfo(
        "Cirurgias Próximas",
        "\n".join(avisos)
    )


def validar_login(usuario, senha):

    conexao = sqlite3.connect(BANCO)

    cursor = conexao.cursor()

    cursor.execute("""
    SELECT *
    FROM usuarios
    WHERE usuario = ?
    AND senha = ?
    """, (

        usuario,
        senha

    ))

    resultado = cursor.fetchone()

    conexao.close()

    return resultado

print(
    validar_login(
        "admin",
        "123"
    )
)


def abrir_login():

    janela_login = tk.Toplevel()

    janela_login.protocol(
    "WM_DELETE_WINDOW",
    lambda: None
)

    janela_login.title("Login")

    janela_login.geometry("300x200")

    janela_login.grab_set()

    ttk.Label(
        janela_login,
        text="Usuário"
    ).pack(pady=5)

    entry_usuario = tk.Entry(
        janela_login
    )

    entry_usuario.pack()

    ttk.Label(
        janela_login,
        text="Senha"
    ).pack(pady=5)

    entry_senha = tk.Entry(
        janela_login,
        show="*"
    )

    entry_senha.pack()

    def fazer_login():

        usuario = entry_usuario.get()

        senha = entry_senha.get()

        resultado = validar_login(
            usuario,
            senha
        )

        if resultado:

            janela.deiconify()

            janela_login.destroy()

        else:

            messagebox.showerror(
                "Erro",
                "Usuário ou senha inválidos"
            )

    ttk.Button(
        janela_login,
        text="Entrar",
        command=fazer_login
    ).pack(pady=15)







janela.withdraw()

abrir_login()
carregar_usuarios()

janela.mainloop()

