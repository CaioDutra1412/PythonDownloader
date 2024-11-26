import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp as ydl
import os
from urllib.parse import urlparse

# Função para validar URL
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Função para atualizar a barra de progresso
def hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        if total_bytes > 0:
            progresso = int(downloaded_bytes / total_bytes * 100)
            progress_bar['value'] = progresso
            janela.update_idletasks()
        status_label.config(text=f"Baixando: {progresso}% concluído")
    elif d['status'] == 'finished':
        progress_bar['value'] = 100
        status_label.config(text="Download concluído!")

# Função para fazer o download
def baixar():
    link = link_entry.get()
    salvar_em = salvar_entry.get()
    formato = format_var.get()

    # Validações de entrada
    if not is_valid_url(link):
        status_label.config(text="Erro: Insira um link válido!")
        return

    if not salvar_em.strip():
        status_label.config(text="Erro: Selecione um local para salvar o arquivo!")
        return

    try:
        # Configurações do yt-dlp
        ydl_opts = {
            'outtmpl': os.path.join(salvar_em, '%(title)s.%(ext)s'),
            'progress_hooks': [hook],  # Vincular a barra de progresso
        }

        if formato == "Áudio":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',  # Configura o formato de saída como MP3
                    'preferredquality': '192',  # Qualidade do áudio (pode ajustar para 128, 256, etc.)
                }]
            })
        else:
            ydl_opts.update({'format': 'best'})  # Configuração para vídeo

        # Configurar FFmpeg se necessário
        ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"  # Atualize o caminho para o FFmpeg no seu sistema
        if os.path.exists(ffmpeg_path):
            ydl_opts['ffmpeg_location'] = ffmpeg_path

        status_label.config(text="Iniciando o download...")
        progress_bar['value'] = 0

        # Baixar usando yt-dlp
        with ydl.YoutubeDL(ydl_opts) as ydl_instance:
            ydl_instance.download([link])

        messagebox.showinfo("Sucesso", "Download concluído com sucesso!")

    except ydl.DownloadError:
        status_label.config(text="Erro: Verifique o link ou sua conexão!")
    except FileNotFoundError:
        status_label.config(text="Erro: FFmpeg não encontrado!")
    except Exception as e:
        status_label.config(text=f"Erro desconhecido: {str(e)}")

# Função para abrir a janela de seleção de pasta
def escolher_local():
    pasta = filedialog.askdirectory(title="Escolha onde salvar o arquivo")
    if pasta:
        salvar_entry.delete(0, tk.END)
        salvar_entry.insert(0, pasta)

# Criar a interface gráfica
janela = tk.Tk()
janela.title("YouTube Downloader")
janela.geometry("450x355")
janela.resizable(False, False)

# Widgets da interface
tk.Label(janela, text="Link do YouTube:", font=("Arial", 10)).pack(pady=5)
link_entry = tk.Entry(janela, width=60)
link_entry.pack(pady=5)

tk.Label(janela, text="Salvar em:", font=("Arial", 10)).pack(pady=5)
salvar_entry = tk.Entry(janela, width=60)
salvar_entry.pack(pady=5)

escolher_button = tk.Button(janela, text="Escolher Local", command=escolher_local)
escolher_button.pack(pady=5)

tk.Label(janela, text="Formato:", font=("Arial", 10)).pack(pady=5)
format_var = tk.StringVar(value="Vídeo")  # Padrão
tk.OptionMenu(janela, format_var, "Vídeo", "Áudio").pack(pady=5)

baixar_button = tk.Button(janela, text="Baixar", command=baixar, bg="#4CAF50", fg="white", font=("Arial", 10))
baixar_button.pack(pady=20)

progress_bar = ttk.Progressbar(janela, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=5)

status_label = tk.Label(janela, text="", font=("Arial", 10), fg="red")
status_label.pack(pady=5)

# Rodar a interface gráfica
janela.mainloop()
