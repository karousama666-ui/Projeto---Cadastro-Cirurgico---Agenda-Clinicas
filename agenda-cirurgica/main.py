import json
import csv
from datetime import datetime


def salvar_dados():

    with open("cirurgias.json", "w", encoding="utf-8") as arquivo:
        
        json.dump(
            cirurgias,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

def carregar_dados():

    global cirurgias

    try:

        with open ("cirurgias.json", "r", encoding="utf-8") as arquivo:

            cirurgias = json.load(arquivo)

    except FileNotFoundError:

        cirurgias = []

cirurgias = []
carregar_dados()

def cadastrar_cirurgia():
    paciente = input("Nome do paciente: ")
    medico = input("Médico: ")
    hospital = input("Hospital: ")
    convenio = input("Convênio: ")
    
    while True:
        data = input("Data da cirurgia: (dd/mm/aaaa): ")

        if validar_data(data):
            break
        print("Data Inválida. Tente Novamente.")

    while True:
        horario = input("Horário da cirurgia: (HH:MM): ")

        if validar_horario(horario):
            break
        print("Horário Inválido. Tente Novamente.")

    procedimento = input("Procedimento: ")

    cirurgia = {
        "paciente" : paciente,
        "medico" : medico,
        "hospital" : hospital,
        "convenio" : convenio,
        "data" : data,
        "horario" : horario,
        "procedimento" : procedimento
    
    }

    cirurgias.append(cirurgia)
    print(cirurgias)
    salvar_dados()


    print("\nCirurgia Cadastrada!")
    print(cirurgia)




    print("\nResumo:")
    print("Paciente Cadastrado:", paciente)
    print("Médico:", medico)
    print("Hospital:", hospital)
    print("Convênio:", convenio)
    print("Data da cirurgia:", data)
    print("Horário da cirurgia:", horario)
    print("Procedimento:", procedimento)
    
def listar_cirurgias():

    print("\n====CIRURGIAS CADASTRADAS===")

    for cirurgia in cirurgias:
        
        print("\nPaciente:", cirurgia["paciente"])
        print("Médico:", cirurgia["medico"])
        print("Hospital:", cirurgia["hospital"])
        print("Convênio:", cirurgia["convenio"])
        print("Data da cirurgia:", cirurgia["data"])
        print("Horário da cirurgia:", cirurgia["horario"])
        print("Procedimento", cirurgia["procedimento"])

def buscar_cirurgia():
    
    paciente_busca = input("Digite o nome do paciente: ")
    
    encontrou = False

    for cirurgia in cirurgias:

        if paciente_busca.lower() in cirurgia["paciente"].lower():
            
            encontrou = True
            
        print("\nCirurgia encontrada!")
    
        print ("Paciente:", cirurgia["paciente"])
        print("Médico:", cirurgia["medico"])
        print("Hospital:", cirurgia["hospital"])
        print("Convênio:", cirurgia["convenio"])
        print("Data da cirurgia:", cirurgia["data"])
        print("Horário da cirurgia:", cirurgia["horario"])
        print("Procedimento", cirurgia["procedimento"])

    if not encontrou:
        print("Paciente não encontrado.")                  

def excluir_cirurgia():

    paciente_busca = input("Digite o nome do paciente para excluir: ")

    encontrou = False

    for cirurgia in cirurgias:

        if paciente_busca.lower() in cirurgia["paciente"].lower():
            
            cirurgias.remove(cirurgia)
            salvar_dados()

            encontrou = True

            print("\nCirurgia removida com sucesso!")
            break

    if not encontrou:
        print("\nPaciente não encontrado.")

def editar_cirurgia():

    paciente_busca = input("Digite o nome do paciente: ")

    encontrou = False

    for cirurgia in cirurgias:

        if paciente_busca.lower() in cirurgia["paciente"].lower():

            encontrou = True

            print("\nCirurgia encontrada!")

            print("Paciente:", cirurgia["paciente"])
            print("Data atual:", cirurgia["data"])
            print("Horário atual:", cirurgia ["horario"])

            nova_data = input("Nova data: ")
            novo_horario = input("Novo horário: ")
            salvar_dados()

            print("\nCirurgia atualizada com sucesso!")

            break
    
    if not encontrou:
        print("\nPaciente não encontrado.")

def buscar_por_data():

    data_busca = input("Digita a data (dd/mm/aaa): ")
    encontrou = False

    for cirurgia in cirurgias:

        if cirurgia["data"] == data_busca:
            encontrou = True

            print("\n--------------------------------------")
            print("Paciente: ", cirurgia["paciente"])
            print("Médico: ", cirurgia["medico"])
            print("Hospital: ", cirurgia["hospital"])
            print("Convênio: ", cirurgia["convenio"])
            print("Horário: ", cirurgia["horario"])
            print("Procedimento: ", cirurgia["procedimento"])

    if not encontrou:
        print("\nNenhuma cirurgia foi encontrada para esta data.")

def validar_data(data):

    try:

        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validar_horario(horario):

    try:
        datetime.strptime(horario, "%H:%M")
        return True
    except ValueError:
        return False

def resumo_agenda():
    print("\n==== RESUMO DA AGENDA ====")

    total = len(cirurgias)
    print("Total de cirurgias:", total)

    hospitais = {}

    for cirurgia in cirurgias:
        hospital = cirurgia["hospital"]

        if hospital in hospitais:
            hospitais[hospital] +=1

        else:
            hospitais[hospital] = 1

            print("\nCirurgias por hospital:")
            for hospital, quantidade in hospitais.items():
                print(f"{hospital}: {quantidade}")

def exportar_csv():
    with open(
        "relatorio_cirurgias.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:
        
        escritor = csv.writer(arquivo)

        escritor.writerow([
            "Paciente",
            "Médico",
            "Hospital"
            "Convênio"
            "Data",
            "Horário",
            "Procedimento",
        ])

        for cirurgia in cirurgias:

            escritor.writerow([
                cirurgia["paciente"],
                cirurgia["medico"],
                cirurgia["hospital"],
                cirurgia["convenio"],
                cirurgia["data"],
                cirurgia["horario"],
                cirurgia["procedimento"]
            ])

    print("\nRelatório exportado com sucesso!")

def buscar_por_convenio():
    convenio_busca = input("Digite o convênio: ")
    encontrou = False
    for cirurgia in cirurgias:
        
        if convenio_busca.lower() in cirurgia.get("convenio", "").lower():
            encontrou = True

            print("\n--------------------------------------")
            print("Paciente:", cirurgia["paciente"])
            print("Médico:", cirurgia["medico"])
            print("Hospital:", cirurgia["hospital"])
            print("Convênio:", cirurgia["convenio"])
            print("Data:", cirurgia["data"])
            print("Horário", cirurgia["horario"])
            print("Procedimento:", cirurgia["procedimento"])
        
    if not encontrou:
        print("\nNenhuma cirurgia encontrada para este convênio!")
    


while True:

    print("\n==== AGENDA CIRÚRGICA ====")

    print("1 - Cadastrar Cirurgia")
    print("2 - Listar Cirurgias")
    print("3 - Buscar Cirurgias")
    print("4 - Excluir Cirurgia")
    print("5 - Editar Cirurgia")
    print("6 - Buscar por Data")
    print("7 - Resumo da Agenda")
    print("8 - Exportar Relatório")
    print("9 - Buscar por Convênio")
    print("10 - Sair")


    opcao = input("Escolha uma opção: ")


    if opcao == "1":
        cadastrar_cirurgia()
    elif opcao == "2":
        listar_cirurgias()
    elif opcao == "3":
        buscar_cirurgia()
    elif opcao == "4":
        excluir_cirurgia()
    elif opcao == "5":
        editar_cirurgia()
    elif opcao == "6":
         buscar_por_data()
    elif opcao == "7":
        resumo_agenda()
    elif opcao == "8":
        exportar_csv()
    elif opcao == "9":
        buscar_por_convenio()
    elif opcao == "10":
        print("Encerrando o sistema...")
        break