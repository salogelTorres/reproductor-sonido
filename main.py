import tkinter as tk
from tkinter import filedialog
import pygame
import time

# Inicializa Pygame para el audio
pygame.mixer.init()

# Variables
audio_loaded = False
paused = False
current_pos = 0
start_time = 0
duration = 0

# Funciones
def cargar_audio():
    global audio_loaded, paused, duration, current_pos
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
    if file_path:
        pygame.mixer.music.load(file_path)
        play_pause_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.NORMAL)
        forward_button.config(state=tk.NORMAL)
        backward_button.config(state=tk.NORMAL)
        play_pause_button.config(text="Play")
        status_label.config(text="Audio cargado: " + file_path.split("/")[-1])
        audio_loaded = True
        paused = False
        current_pos = 0  # Reseteamos la posición
        duration = pygame.mixer.Sound(file_path).get_length()  # Obtenemos la duración total del archivo
        update_time_label()  # Actualizamos la etiqueta de tiempo

def play_pause_audio():
    global paused, current_pos, start_time
    if audio_loaded:
        if paused:
            pygame.mixer.music.unpause()
            play_pause_button.config(text="Pause")
            status_label.config(text="Reproduciendo...")
            start_time = time.time() - current_pos  # Ajusta el tiempo inicial después de la pausa
            paused = False
            update_time_label()  # Inicia la actualización del tiempo
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                play_pause_button.config(text="Play")
                current_pos = time.time() - start_time  # Guarda la posición actual
                status_label.config(text="Pausado")
                paused = True
            else:
                pygame.mixer.music.play(start=current_pos)
                play_pause_button.config(text="Pause")
                start_time = time.time() - current_pos  # Inicia el temporizador
                status_label.config(text="Reproduciendo...")
                paused = False
                update_time_label()  # Inicia la actualización del tiempo

def detener_audio():
    global paused, current_pos
    pygame.mixer.music.stop()
    play_pause_button.config(text="Play")
    status_label.config(text="Detenido")
    current_pos = 0
    paused = False
    update_time_label()  # Actualizamos el tiempo a 0

def avanzar_audio():
    global current_pos, start_time
    if audio_loaded and not paused:
        current_pos = min(duration, current_pos + 5)  # Avanza 5 segundos pero no más allá de la duración
        pygame.mixer.music.stop()
        pygame.mixer.music.play(start=current_pos)
        start_time = time.time() - current_pos
        status_label.config(text=f"Avanzado a {current_pos:.2f} segundos")
        update_time_label()

def retroceder_audio():
    global current_pos, start_time
    if audio_loaded and not paused:
        current_pos = max(0, current_pos - 5)  # Retrocede 5 segundos pero no menos de 0
        pygame.mixer.music.stop()
        pygame.mixer.music.play(start=current_pos)
        start_time = time.time() - current_pos
        status_label.config(text=f"Retrocedido a {current_pos:.2f} segundos")
        update_time_label()

def update_time_label():
    if audio_loaded and not paused:
        current_pos = time.time() - start_time  # Calcula el tiempo actual
        time_str = time_format(current_pos)
        total_str = time_format(duration)
        time_label.config(text=f"{time_str} / {total_str}")
        # Si la música sigue reproduciéndose, actualizamos cada 500 ms
        if pygame.mixer.music.get_busy():
            time_label.after(500, update_time_label)
        else:
            time_label.config(text=f"{time_format(duration)} / {total_str}")

def time_format(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

# Interfaz gráfica
root = tk.Tk()
root.title("Reproductor de Música")

# Botones en horizontal
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

cargar_button = tk.Button(buttons_frame, text="Cargar Audio", command=cargar_audio)
cargar_button.pack(side=tk.LEFT, padx=5)

play_pause_button = tk.Button(buttons_frame, text="Play", command=play_pause_audio, state=tk.DISABLED)
play_pause_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(buttons_frame, text="Stop", command=detener_audio, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=5)

forward_button = tk.Button(buttons_frame, text="Avanzar +5s", command=avanzar_audio, state=tk.DISABLED)
forward_button.pack(side=tk.LEFT, padx=5)

backward_button = tk.Button(buttons_frame, text="Retroceder -5s", command=retroceder_audio, state=tk.DISABLED)
backward_button.pack(side=tk.LEFT, padx=5)

# Etiqueta de tiempo actual / duración total
time_label = tk.Label(root, text="00:00 / 00:00")
time_label.pack(pady=10)

# Etiqueta de estado
status_label = tk.Label(root, text="No hay audio cargado")
status_label.pack(pady=10)

# Inicia la interfaz gráfica
root.mainloop()
