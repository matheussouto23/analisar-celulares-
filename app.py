import tkinter as tk
from tkinter import messagebox, StringVar, Listbox, ttk
import pandas as pd

# Função para avaliar se o celular é bom ou ruim
def avaliar_celular(row):
    media = (row['Desempenho'] + row['Câmera'] + row['Bateria'] + row['Tela'] + row['Armazenamento']) / 5
    return "Bom" if media >= 4 else "Ruim"

# Função para buscar e exibir os dados do celular
def buscar_celular(event=None):
    modelo = entry_modelo.get()
    try:
        # Carregar dados do CSV
        df = pd.read_csv('data/celulares.csv')

        # Verificar se o celular está na lista
        celular = df[df['Modelo'].str.contains(modelo, case=False)].copy()

        if celular.empty:
            messagebox.showinfo("Resultado", "Celular não encontrado.")
        else:
            # Avaliar o celular
            celular['Avaliação'] = celular.apply(avaliar_celular, axis=1)
            exibir_resultados(celular.iloc[0])
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")

# Função para exibir resultados em uma nova janela
def exibir_resultados(info):
    # Criar uma nova janela
    resultado_window = tk.Toplevel(root)
    resultado_window.title("Resultado da Avaliação")
    resultado_window.geometry("350x400")  # Tamanho da janela
    resultado_window.config(bg="#f0f0f0")

    # Cabeçalho
    tk.Label(resultado_window, text="Avaliação do Celular", bg="#f0f0f0", font=("Arial", 16, "bold")).pack(pady=10)

    # Labels para mostrar os resultados
    tk.Label(resultado_window, text="Modelo:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    tk.Label(resultado_window, text=info['Modelo'], bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=5)

    tk.Label(resultado_window, text="Desempenho:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    tk.Label(resultado_window, text=info['Desempenho'], bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=5)

    tk.Label(resultado_window, text="Câmera:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    tk.Label(resultado_window, text=info['Câmera'], bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=5)

    tk.Label(resultado_window, text="Bateria:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    tk.Label(resultado_window, text=info['Bateria'], bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=5)

    tk.Label(resultado_window, text="Tela:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    tk.Label(resultado_window, text=info['Tela'], bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=5)

    tk.Label(resultado_window, text="Armazenamento:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    tk.Label(resultado_window, text=info['Armazenamento'], bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=5)

    tk.Label(resultado_window, text="Preço:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    tk.Label(resultado_window, text=f"R$ {info['Preço']}", bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=5)

    tk.Label(resultado_window, text="Avaliação:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
    tk.Label(resultado_window, text=info['Avaliação'], bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=5)

# Função para atualizar as sugestões de autocompletar
def atualizar_sugestoes(*args):
    modelo = entry_modelo.get()
    if modelo:
        sugestoes = df[df['Modelo'].str.contains(modelo, case=False)]['Modelo'].tolist()
        listbox.delete(0, tk.END)  # Limpa as sugestões anteriores
        for sugestao in sugestoes:
            listbox.insert(tk.END, sugestao)  # Adiciona novas sugestões

# Criar a janela principal
root = tk.Tk()
root.title("Avaliação de Celulares")
root.geometry("400x400")  # Tamanho da janela
root.config(bg="#f0f0f0")  # Cor de fundo

# Carregar dados do CSV uma vez
df = pd.read_csv('data/celulares.csv')

# Cabeçalho principal
header = tk.Label(root, text="Sistema de Avaliação de Celulares", bg="#4CAF50", fg="white", font=("Arial", 18, "bold"))
header.pack(fill=tk.X)

# Frame principal
frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
frame.pack(pady=20)

# Configurar widgets
label_modelo = tk.Label(frame, text="Digite o modelo do celular:", bg="#f0f0f0", font=("Arial", 12))
label_modelo.grid(row=0, column=0, pady=5)

entry_modelo = tk.Entry(frame, width=50, font=("Arial", 12), borderwidth=2, relief="groove")
entry_modelo.grid(row=0, column=1, pady=5)
entry_modelo.bind("<KeyRelease>", atualizar_sugestoes)  # Atualiza sugestões ao digitar

# Listbox para exibir sugestões
listbox = Listbox(frame, width=50, font=("Arial", 12), height=5)
listbox.grid(row=1, columnspan=2, pady=5)

# Configurar ação ao clicar em uma sugestão
def on_select(event):
    selected = listbox.curselection()
    if selected:
        entry_modelo.delete(0, tk.END)  # Limpa o campo de entrada
        entry_modelo.insert(0, listbox.get(selected))  # Insere a sugestão selecionada
        listbox.delete(0, tk.END)  # Limpa as sugestões

listbox.bind("<<ListboxSelect>>", on_select)

button_buscar = tk.Button(frame, text="Buscar Celular", command=buscar_celular, bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
button_buscar.grid(row=2, columnspan=2, pady=20)

# Iniciar o loop da interface gráfica
root.mainloop()
