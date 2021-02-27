from tkinter import *
import tkinter as tk
from tkinter import filedialog
import pygame
from tinytag import TinyTag 

class Application (Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        pygame.mixer.init()
        global paused
        #button functions/definitions
        def play():
            paused = FALSE
            pygame.mixer.music.load("")
            pygame.mixer.music.play(loops=0)
            
        def pause():
            paused = TRUE
            pygame.mixer.music.pause()
        
        def skip():
            return

        def prev():
            return
        
        def stop():
            pygame.mixer.music.stop()

        def add_song():
            #get song file directory
            song_file = filedialog.askopenfilename(initialdir='Music/', title='Select a song', filetypes=(("mp3 Files", "*.mp3"), ("WAV Files", "*.wav"), ("FLAC Files", "*.flac")))
            #get song file metadata
            tag = TinyTag.get(song_file)
            #get song file metadata title
            song = tag.title
            #add song to playlist
            self.playlist_box.insert(END, song)
            
        #button images
        self.play_btn_img = PhotoImage(file='imgs/play_img.png')
        self.pause_btn_img = PhotoImage(file='imgs/pause_img.png')
        self.skip_btn_img = PhotoImage(file='imgs/skip_img.png')
        self.prev_btn_img = PhotoImage(file='imgs/prev_img.png')
        self.stop_btn_img = PhotoImage(file='imgs/stop_img.png')

        #initialize playlist area items
        self.playlist_box = Listbox(self, bg="white", fg="black", width=65, height=20)
        self.playlist = Menu(self)
        master.config(menu=self.playlist)

        #Add song playlist
        self.add_song_playlist = Menu(self.playlist)
        self.playlist.add_cascade(label="Add Songs", menu=self.add_song_playlist)
        self.add_song_playlist.add_command(label="Add song to playlist", command=lambda:add_song())

        #initialize buttons
        self.buttons_frame = Frame(self)
        self.play_btn = Button(self.buttons_frame, image=self.play_btn_img, borderwidth=0, command=lambda:play())
        self.pause_btn = Button(self.buttons_frame, image=self.pause_btn_img, borderwidth=0)
        self.skip_btn = Button(self.buttons_frame, image=self.skip_btn_img, borderwidth=0)
        self.prev_btn = Button(self.buttons_frame, image=self.prev_btn_img, borderwidth=0)
        self.stop_btn = Button(self.buttons_frame, image=self.stop_btn_img, borderwidth=0, command=lambda:stop())

        #UI item placements
        self.buttons_frame.grid(row=1, column = 3)
        self.play_btn.grid(row=1, column=2, padx=10)
        self.pause_btn.grid(row=1, column=3, padx=10)
        self.skip_btn.grid(row=1, column=4, padx=10)
        self.prev_btn.grid(row=1, column=1, padx=10)
        self.stop_btn.grid(row=1, column=5, padx=10)
        self.playlist_box.grid(row=2,column=3)
        self.pack()

root = tk.Tk()
root.title("Music Player")
app = Application(root)
#root.geometry("500x400")
root.mainloop()