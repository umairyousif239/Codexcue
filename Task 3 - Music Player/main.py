# Description: A simple music player using pygame and tkinter
import tkinter
import customtkinter
import pygame
from PIL import Image, ImageTk
from threading import *
import time
import math

# Set appearance mode and default color theme
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

# Main window
root = customtkinter.CTk()
root.title("Music Player")
root.geometry("400x480")
root.resizable(False, False)
pygame.mixer.init()

# Variables
list_of_songs = ['music/Borderline.mp3', 'music/Sanctuary.mp3', 'music/SLOW DANCING IN THE DARK.mp3']
list_of_covers = ['img/Borderline.jpg', 'img/Sanctuary.jpg', 'img/SLOW DANCING IN THE DARK.jpg']
n = 0
is_paused = False

# Album cover
song_name_label = tkinter.Label(root, bg='#222222', fg='white')
song_name_label.place(relx=0.5, rely=0.63, anchor=tkinter.CENTER)

# Functions
def get_album_cover(song_name, n):
    current_song = n
    image1 = Image.open(list_of_covers[current_song])
    image2 = image1.resize((250, 250))
    load = ImageTk.PhotoImage(image2)
    label1 = tkinter.Label(root, image=load)
    label1.image = load
    label1.place(relx=.19, rely=.06)

    stripped_string = song_name[6:-5]
    song_name_label.configure(text=stripped_string)

def progress():
    a = pygame.mixer.Sound(f'{list_of_songs[n]}')
    song_len = a.get_length() * 3
    for _ in range(0, math.ceil(song_len)):
        time.sleep(.3)
        progressbar.set(pygame.mixer.music.get_pos() / 1000000)

def threading():
    t1 = Thread(target=progress)
    t1.start()

def play_music():
    global is_paused
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
        play_button.configure(text="Pause")
    else:
        threading()
        global n
        current_song = n
        song_name = list_of_songs[current_song]
        pygame.mixer.music.load(song_name)
        pygame.mixer.music.play(loops=0)
        pygame.mixer.music.set_volume(.5)
        get_album_cover(song_name, n)
        root.after(1000, check_song_end)
        play_button.configure(text="Pause")

def pause_music():
    global is_paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        is_paused = True
        play_button.configure(text="Play")

def play_pause_music():
    if is_paused:
        play_music()
    else:
        pause_music()

def check_song_end():
    if not pygame.mixer.music.get_busy() and not is_paused:
        skip_forward()
    else:
        root.after(1000, check_song_end)

def skip_forward():
    global n, is_paused
    n += 1
    if n >= len(list_of_songs):
        n = 0
    is_paused = False
    play_music()

def go_back():
    global n, is_paused
    n -= 1
    if n < 0:
        n = len(list_of_songs) - 1
    is_paused = False
    play_music()

def volume_control(val):
    pygame.mixer.music.set_volume(slider.get())

# Buttons
play_button = customtkinter.CTkButton(master=root, text='Play', command=play_pause_music)
play_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

skip_button = customtkinter.CTkButton(master=root, text='>', command=skip_forward, width=2)
skip_button.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

back_button = customtkinter.CTkButton(master=root, text='<', command=go_back, width=2)
back_button.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

slider = customtkinter.CTkSlider(master=root, from_=0, to=1, command=volume_control, width=210)
slider.place(relx=0.5, rely=0.78, anchor=tkinter.CENTER)

progressbar = customtkinter.CTkProgressBar(master=root, progress_color='#32a85a', width=250)
progressbar.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

# Initial play
play_music()

# Main loop
root.mainloop()
