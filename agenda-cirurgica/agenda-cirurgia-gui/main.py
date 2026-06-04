import tkinter as tk
import json

cirurgias = []
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
janela.geometry("600x400")

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
    
    
    
    cirurgias.append(cirurgia)
    salvar_dados()
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

botao_cadastrar = tk.Button(janela, text="Cadastrar", command=cadastrar)
botao_cadastrar.pack(pady=10)   


janela.mainloop()

