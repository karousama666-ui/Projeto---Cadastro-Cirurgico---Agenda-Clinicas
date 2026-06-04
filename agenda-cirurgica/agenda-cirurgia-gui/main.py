import tkinter as tk
janela = tk.Tk()
janela.title("Agenda Cirúrgica")
tk.Label(janela, text="Paciente").pack()

entrada_paciente = tk.Entry(janela)
entrada_paciente.pack()


janela.mainloop()

