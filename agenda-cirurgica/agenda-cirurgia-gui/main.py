import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

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

# Título

titulo = tk.Label(janela, text="Cadastro Cirúrgico", font=("Arial", 16))
titulo.pack(pady=10)    

# Campo Paciente

tk.Label(janela, text="Paciente:").pack()

entrada_paciente = tk.Entry(janela, width=40)
entrada_paciente.pack()

# Campo Médico

tk.Label(janela, text="Médico:").pack()

entrada_medico = tk.Entry(janela, width=40)
entrada_medico.pack()

# Campo Hospital

tk.Label(janela, text="Hospital:").pack()

entrada_hospital = tk.Entry(janela, width=40)
entrada_hospital.pack()

# Campo Convênio

tk.Label(janela, text="Convênio:").pack()

entrada_convenio = tk.Entry(janela, width=40)
entrada_convenio.pack()

# Campo Data da Cirurgia

tk.Label(janela, text="Data da Cirurgia:").pack()

entrada_data = tk.Entry(janela, width=40)
entrada_data.pack()

# Campo Horário da Cirurgia

tk.Label(janela, text="Horário da Cirurgia:").pack()

entrada_horario = tk.Entry(janela, width=40)
entrada_horario.pack()

# Campo Procedimento

tk.Label(janela, text="Procedimento:").pack()

entrada_procedimento = tk.Entry(janela, width=40)
entrada_procedimento.pack()

# Campo de Busca

tk.Label(janela, text="Buscar por Paciente:").pack()

entrada_busca = tk.Entry(janela, width=40)
entrada_busca.pack()

def cadastrar():
    paciente = entrada_paciente.get()
    medico = entrada_medico.get()
    hospital = entrada_hospital.get()
    convenio = entrada_convenio.get()
    data = entrada_data.get()
    horario = entrada_horario.get()
    procedimento = entrada_procedimento.get()

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
    print("Índice de Edição: ", indice_edicao)
    
    if indice_edicao is not None:
        cirurgias[indice_edicao] = cirurgia
        indice_edicao = None
    else:
        cirurgias.append(cirurgia)

    salvar_dados()
    atualizar_tabela()

    entrada_paciente.delete(0, tk.END)
    entrada_medico.delete(0, tk.END)
    entrada_hospital.delete(0, tk.END)
    entrada_convenio.delete(0, tk.END)
    entrada_data.delete(0, tk.END)
    entrada_horario.delete(0, tk.END)
    entrada_procedimento.delete(0, tk.END)

    from tkinter import messagebox
    messagebox.showinfo("Sucesso", "Cirurgia cadastrada com sucesso!")

    print(cirurgias)

def carregar_dados():

    global cirurgias

    try:

        with open ("cirurgias.json", "r", encoding="utf-8") as arquivo:

            cirurgias = json.load(arquivo)

    except FileNotFoundError:

        cirurgias = []

cirurgias = []
carregar_dados()

def excluir_cirurgia():
    
    item_selecionado = tabela.selection()

    if not item_selecionado:
        print("Nenhuma cirurgia selecionada para exclusão.")
        return
    
    valores = tabela.item(item_selecionado [0], "values")
    
    for cirurgia in cirurgias:
        if (cirurgia["paciente"] == valores[0]):
            cirurgias.remove(cirurgia)
            break
    
    salvar_dados()
    atualizar_tabela()

    messagebox.showinfo("Sucesso", "Cirurgia excluída com sucesso!")

def editar_cirurgia():
    item_selecionado = tabela.selection()

    if not item_selecionado:
        print("Nenhuma cirurgia selecionada para edição.")
        return
    
    valores = tabela.item(item_selecionado[0], "values")


    global indice_edicao
    indice_edicao = tabela.index(item_selecionado[0])
    print("Editando índice: ", indice_edicao)

    entrada_paciente.delete(0, tk.END)
    entrada_paciente.insert(0, valores[0])  
    entrada_medico.delete(0, tk.END)
    entrada_medico.insert(0, valores[1])
    entrada_hospital.delete(0, tk.END)
    entrada_hospital.insert(0, valores[2])
    entrada_convenio.delete(0, tk.END)
    entrada_convenio.insert(0, valores[3])
    entrada_data.delete(0, tk.END)
    entrada_data.insert(0, valores[4])
    entrada_horario.delete(0, tk.END)
    entrada_horario.insert(0, valores[5])
    entrada_procedimento.delete(0, tk.END)
    entrada_procedimento.insert(0, valores[6])

def buscar_paciente():
    termo_busca = entrada_busca.get().lower()

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

    
    
    

botao_cadastrar = tk.Button(janela, text="Cadastrar", command=cadastrar)
botao_cadastrar.pack(pady=10)   

botao_excluir = tk.Button(janela, text="Excluir Cirurgia",
                          command=excluir_cirurgia)
botao_excluir.pack(pady=5)

botao_editar = tk.Button(janela, text="Editar Cirurgia",
                         command=editar_cirurgia)
botao_editar.pack(pady=5)

botao_buscar = tk.Button(janela, text="Buscar", command=buscar_paciente)
botao_buscar.pack(pady=5)

tabela = ttk.Treeview(janela, columns=("Paciente", "Médico", "Hospital", "Convênio", "Data", "Horário", "Procedimento"), show="headings")
tabela.heading("Paciente", text="Paciente")
tabela.heading("Médico", text="Médico")
tabela.heading("Hospital", text="Hospital")
tabela.heading("Convênio", text="Convênio")
tabela.heading("Data", text="Data")
tabela.heading("Horário", text="Horário")  
tabela.heading("Procedimento", text="Procedimento")

tabela.pack(pady=10)
print("Tabela criada")

def atualizar_tabela():

    for item in tabela.get_children():
        tabela.delete(item)

    for cirurgia in cirurgias:
        tabela.insert("", "end", values=(
            cirurgia["paciente"],
            cirurgia["medico"],
            cirurgia["hospital"],
            cirurgia["convenio"],
            cirurgia["data"],
            cirurgia["horario"],
            cirurgia["procedimento"]
        ))
atualizar_tabela()



janela.mainloop()

