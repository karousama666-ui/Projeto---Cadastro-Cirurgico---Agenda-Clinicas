import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import messagebox
import json
from datetime import datetime
from tkcalendar import DateEntry
import matplotlib.pyplot as plt

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

janela = tk.Tk()
janela.title("Agenda Cirúrgica")
janela.geometry("1920x1080")

notebook = ttk.Notebook(janela)

aba_cadastro = tk.Frame(notebook)
aba_agenda = tk.Frame(notebook)
aba_relatorios = tk.Frame(notebook)

notebook.add(
    aba_cadastro,
    text="Cadastro"
)

notebook.add(
    aba_agenda,
    text="Agenda"
)

notebook.add(
    aba_relatorios,
    text="Relatórios"
)

notebook.pack(
    expand=True,
    fill="both"
)

titulo_relatorios = tk.Label(
    aba_relatorios,
    text="Relatórios",
    font=("Arial", 16)
)

titulo_relatorios.pack(pady=10)

label_total = tk.Label(
    aba_relatorios,
    text="Total de Cirurgias: 0",
    font=("Arial", 12)
)

label_total.pack(pady=10)

label_hospital = tk.Label(
    aba_relatorios,
    text="Hospital mais utilizado: -",
    font=("Arial", 12)
)

label_hospital.pack(pady=5)

label_convenio = tk.Label(
    aba_relatorios,
    text="Convênio mais utilizado: -",
    font=("Arial", 12)
)

label_convenio.pack(pady=5)

label_medico = tk.Label(
    aba_relatorios,
    text="Médico com mais cirurgias: -",
    font=("Arial", 12)
)

label_medico.pack(pady=5)



# Título

titulo = tk.Label(aba_cadastro, text="Cadastro Cirúrgico", font=("Arial", 16))
titulo.pack(pady=10)    

# Campo Paciente

tk.Label(aba_cadastro, text="Paciente:").pack()

entrada_paciente = tk.Entry(aba_cadastro, width=40)
entrada_paciente.pack()

# Campo Médico

tk.Label(aba_cadastro, text="Médico:").pack()

entrada_medico = tk.Entry(aba_cadastro, width=40)
entrada_medico.pack()

# Campo Hospital

tk.Label(aba_cadastro, text="Hospital:").pack()

entrada_hospital = tk.Entry(aba_cadastro, width=40)
entrada_hospital.pack()

# Campo Convênio

tk.Label(aba_cadastro, text="Convênio:").pack()

entrada_convenio = tk.Entry(aba_cadastro, width=40)
entrada_convenio.pack()

# Campo Data da Cirurgia

tk.Label(aba_cadastro, text="Data da Cirurgia:").pack()

entrada_data = DateEntry(
    aba_cadastro,
    width=20,
    date_pattern="dd/mm/yyyy"
)

entrada_data.pack()

# Campo Horário da Cirurgia

tk.Label(aba_cadastro, text="Horário da Cirurgia:").pack()

entrada_horario = tk.Entry(aba_cadastro, width=40)
entrada_horario.pack()

# Campo Procedimento

tk.Label(aba_cadastro, text="Procedimento:").pack()

entrada_procedimento = tk.Entry(aba_cadastro, width=40)
entrada_procedimento.pack()

# Agenda

titulo_agenda = tk.Label(
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
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return
    
    # Validação de data no formato YYYY-MM-DD

    try:
        datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Erro", "Data inválida! Use o formato DD/MM/YYYY.")
        return
    
    # Horário no formato HH:MM

    try:
        datetime.strptime(horario, "%H:%M")
    except ValueError:
        messagebox.showerror("Erro", "Horário inválido! Use o formato HH:MM.")
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
        "procedimento": procedimento
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

    conexao = sqlite3.connect("cirurgias.db")
    cursor = conexao.cursor()

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

    # Atualiza os labels
    label_total.config(
        text=f"Total de Cirurgias: {total}"
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

    # Widgets

tk.Label(janela, text="Buscar por Paciente:").pack()

entrada_busca = tk.Entry(aba_agenda, width=40)
entrada_busca.pack()

entrada_busca.bind(
    "<KeyRelease>",
    buscar_em_tempo_real
)
    

botao_cadastrar = tk.Button(aba_cadastro, text="Cadastrar", command=cadastrar)
botao_cadastrar.pack(pady=10)   

botao_excluir = tk.Button(aba_agenda, text="Excluir Cirurgia",
                          command=excluir_cirurgia)
botao_excluir.pack(pady=5)

botao_editar = tk.Button(aba_agenda, text="Editar Cirurgia",
                         command=editar_cirurgia)
botao_editar.pack(pady=5)

botao_buscar = tk.Button(aba_agenda, text="Buscar", command=buscar_paciente)
botao_buscar.pack(pady=5)

botao_mostrar_todos = tk.Button(aba_agenda, text="Mostrar Todos", command=mostrar_todos)
botao_mostrar_todos.pack(pady=5)

tabela = ttk.Treeview(aba_agenda, columns=("ID", "Paciente", "Médico", "Hospital", "Convênio", "Data", "Horário", "Procedimento"), show="headings")
tabela.heading("ID", text="ID")
tabela.heading("Paciente", text="Paciente")
tabela.heading("Médico", text="Médico")
tabela.heading("Hospital", text="Hospital")
tabela.heading("Convênio", text="Convênio")
tabela.heading("Data", text="Data")
tabela.heading("Horário", text="Horário")  
tabela.heading("Procedimento", text="Procedimento")

scrollbar = ttk.Scrollbar(aba_agenda, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=scrollbar.set)

tabela.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def carregar_cirurgias_do_banco():
    conexao = sqlite3.connect("cirurgias.db")
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id, paciente, medico, hospital, convenio, data, horario, procedimento FROM cirurgias"""
    )
    registros = cursor.fetchall()
    conexao.close()

    return registros

def atualizar_tabela():

    for item in tabela.get_children():
        tabela.delete(item)

    registros = carregar_cirurgias_do_banco()

    for registro in registros:
        tabela.insert("", "end", values=(
            registro[0],  # ID
            registro[1],  # paciente
            registro[2],  # medico
            registro[3],  # hospital
            registro[4],  # convenio
            registro[5],  # data
            registro[6],  # horario 
            registro[7]   # procedimento
        
        ))


def criar_banco():

    import os
    print("Banco sendo criado em:")
    print(os.path.abspath("cirurgias.db"))



    conexao = sqlite3.connect("cirurgias.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cirurgias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente TEXT,
            medico TEXT,
            hospital TEXT,
            convenio TEXT,
            data TEXT,
            horario TEXT,
            procedimento TEXT
        )
    """)
    conexao.commit()
    conexao.close()

criar_banco()
atualizar_tabela()

def salvar_cirurgia_no_banco(cirurgia):
    conexao = sqlite3.connect("cirurgias.db")
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO cirurgias (paciente, medico, hospital, convenio, data, horario, procedimento)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        cirurgia["paciente"],
        cirurgia["medico"],
        cirurgia["hospital"],
        cirurgia["convenio"],
        cirurgia["data"],
        cirurgia["horario"],
        cirurgia["procedimento"]
    ))
    conexao.commit()
    conexao.close()

def excluir_cirurgia_banco(id_cirurgia):

    conexao = sqlite3.connect("cirurgias.db")

    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM cirurgias WHERE id = ?",
        (id_cirurgia,)
    )

    conexao.commit()

    conexao.close()

def atualizar_cirurgia_banco(cirurgia, paciente_original):

    conexao = sqlite3.connect("cirurgias.db")
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
        paciente_original
    ))

    conexao.commit()
    conexao.close()

def listar_cirurgias_banco():
    conexao = sqlite3.connect("cirurgias.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM cirurgias")

    registros = cursor.fetchall()

    print("\nRegistros no Banco de Dados:")

    for registro in registros:
        print(registro)

    conexao.close()



criar_banco()
atualizar_tabela()
atualizar_relatorios()

janela.mainloop()

