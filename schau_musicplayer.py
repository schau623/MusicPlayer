from tkinter import *
import tkinter as tk
from tkinter import filedialog
import pygame
from tinytag import TinyTag 
import time
from mutagen.mp3 import MP3


class Application (Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        pygame.mixer.init()

        global paused 
        paused = False
        playlist = []
        
        #button/menu functions
        def play():
            global paused
            paused = False
            pygame.mixer.music.stop()
            song = self.playlist_box.curselection()
            pygame.mixer.music.load(playlist[int(song[0])])
            pygame.mixer.music.play(loops=0)
            play_time()

        def pause(is_paused):
            global paused 
            paused = is_paused
            if paused:
                pygame.mixer.music.unpause()
                paused = False
            else:
                pygame.mixer.music.pause()
                paused = True
        
        def skip():
            next_song = self.playlist_box.curselection()
            next_song = next_song[0]+1
            pygame.mixer.music.load(playlist[next_song])
            pygame.mixer.music.play(loops=0)
            self.playlist_box.selection_clear(0, END)
            self.playlist_box.activate(next_song)
            self.playlist_box.selection_set(next_song, last=None)

        def prev():
            prev_song = self.playlist_box.curselection()
            prev_song = prev_song[0]-1
            pygame.mixer.music.load(playlist[prev_song])
            pygame.mixer.music.play(loops=0)
            self.playlist_box.selection_clear(0, END)
            self.playlist_box.activate(prev_song)
            self.playlist_box.selection_set(prev_song, last=None)
        
        def stop():
            global paused
            paused = True
            pygame.mixer.music.stop()
            self.playlist_box.selection_clear(ACTIVE)
            self.position_bar.config(text='')
            self.length_bar.config(text='')

        def add_song():
            #get song file directory
            file = filedialog.askopenfilenames(initialdir='Music/', title='Select a song', filetypes=(("mp3 Files", "*.mp3"), ("wav Files", "*.wav")))
            song_tuple = master.splitlist(file)
            song_list = list(song_tuple)
            #iterate through song list and add songs to playlist
            for song in song_list:
                playlist.append(song)
                tag = TinyTag.get(song)
                song_title = tag.title
                self.playlist_box.insert(END, song_title)

        def remove_song():
            self.playlist_box.delete(ANCHOR)
            pygame.mixer.music.stop()

        def clear_playlist():
            self.playlist_box.delete(0, END)
            pygame.mixer.music.stop()

        #position bar function
        def play_time():
            global paused
            if paused == False:
                current_time = pygame.mixer.music.get_pos()/1000
                converted_time = time.strftime('%H:%M:%S', time.gmtime(current_time))
                self.position_bar.config(text=converted_time)
                #update time
                self.position_bar.after(1000, play_time)
                current_song = self.playlist_box.curselection()
                song_mut = MP3(playlist[int(current_song[0])])
                song_length = song_mut.info.length
                converted_song_length = time.strftime('%H:%M:%S',time.gmtime(song_length))
                self.length_bar.config(text=converted_song_length)
                self.length_bar.after(1000, play_time)

        #button images
        self.play_btn_img = PhotoImage(file='imgs/play_img.png')
        self.pause_btn_img = PhotoImage(file='imgs/pause_img.png')
        self.skip_btn_img = PhotoImage(file='imgs/skip_img.png')
        self.prev_btn_img = PhotoImage(file='imgs/prev_img.png')
        self.stop_btn_img = PhotoImage(file='imgs/stop_img.png')

        #initialize playlist area and menu
        self.playlist_box = Listbox(self, bg="white", fg="black", width=65, height=20, selectbackground="dodger blue", selectforeground="white")
       
        #menu bar
        self.menu_ = Menu(self)
        master.config(menu=self.menu_)
        self.file_menu = Menu(self.menu_, tearoff=0)
        self.menu_.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Add Song(s) to Playlist", command=lambda:add_song())
        self.file_menu.add_command(label="Remove Selected Song from Playlist", command=lambda:remove_song())
        self.file_menu.add_command(label="Clear Playlist", command=lambda:clear_playlist())
        
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=master.quit)

        #initialize buttons
        self.buttons_frame = Frame(self)
        self.play_btn = Button(self.buttons_frame, image=self.play_btn_img, borderwidth=0, command=lambda:play())
        self.pause_btn = Button(self.buttons_frame, image=self.pause_btn_img, borderwidth=0, command=lambda:pause(paused))
        self.skip_btn = Button(self.buttons_frame, image=self.skip_btn_img, borderwidth=0, command=lambda:skip())
        self.prev_btn = Button(self.buttons_frame, image=self.prev_btn_img, borderwidth=0, command=lambda:prev())
        self.stop_btn = Button(self.buttons_frame, image=self.stop_btn_img, borderwidth=0, command=lambda:stop())

        #Song position bar
        self.position_bar = Label(self, width=10, text='', bd=1, relief=GROOVE)
        self.length_bar = Label(self, width=10, text='', bd=1, relief=GROOVE)
        #self.position_bar.pack(fill=X, side=BOTTOM, ipady=2)
        
        #UI item placements
        self.buttons_frame.grid(row=1, column = 3)
        self.play_btn.grid(row=1, column=2, padx=10)
        self.pause_btn.grid(row=1, column=3, padx=10)
        self.skip_btn.grid(row=1, column=4, padx=10)
        self.prev_btn.grid(row=1, column=1, padx=10)
        self.stop_btn.grid(row=1, column=5, padx=10)
        self.playlist_box.grid(row=3,column=3)
        self.position_bar.grid(row=2,column=2)
        self.length_bar.grid(row=2, column=4)
        
        self.pack()

root = tk.Tk()
root.title("Music Player")
app = Application(root)
root.geometry("700x400")
root.mainloop()