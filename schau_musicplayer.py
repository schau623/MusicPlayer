
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import pygame
from tinytag import TinyTag 
import time
from mutagen.mp3 import MP3
from mutagen import File
import tkinter.ttk as ttk
import pickle
import os
from PIL import Image, ImageTk
import io

class Application (Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        pygame.mixer.init()
        self.prev_rewind = 0
        if os.path.exists('songs.pickle'):
            self.playlist = pickle.load(open('songs.pickle', 'rb'))
        else:
            self.playlist=[]
        """IMAGE INITIALIZATION"""
        self.pause_btn_img = PhotoImage(file='imgs/play_img.png')
        self.play_btn_img = PhotoImage(file='imgs/pause_img.png')
        self.skip_btn_img = PhotoImage(file='imgs/skip_img.png')
        self.prev_btn_img = PhotoImage(file='imgs/prev_img.png')
        self.stop_btn_img = PhotoImage(file='imgs/stop_img.png')
        self.loop_btn_img = PhotoImage(file='imgs/loop_img.png')
        self.loop_on_btn_img = PhotoImage(file='imgs/loop_on_img.png')
        self.cover_img = PhotoImage(file='imgs/placeholder_cover.png')
        self.cover_img2 = PhotoImage(file='imgs/001.png')
        self.cover_img = self.cover_img.subsample(x=2, y=2)

        self.current = 0
        self.paused = True
        self.played = False
        self.loop_flag = 0
        self.create_frames()
        self.create_controls()
        self.create_playlist_display()
        self.create_menu()
        self.enumerate_songs()
        self.master.bind('<space>', self.pause)
        pygame.mixer.music.set_volume(0.1)
    def create_frames(self):
        #create_frames
        """FRAME INITIALIZATION"""
        #initialization
        self.controls_frame = Frame(self)
        self.playlist_frame = LabelFrame(self, text=f'Playlist - {str(len(self.playlist))} Songs',
           font=15, bd=0)
        self.playlist_frame.config(width=190,height=400)
        self.song_slider_frame = Frame(self)
        self.display_frame = LabelFrame(self, bd=0)
        
        #frame grid placements
        self.controls_frame.grid(row=2, column=0, padx=10)
        self.playlist_frame.config(width=190, height=400)
        self.playlist_frame.grid(row=0,column=1, rowspan=3, pady=5)
        self.song_slider_frame.grid(row=1, column=0)
        self.display_frame.grid(row=0, column=0)
    def create_controls(self):
        """CONTROL INITIALIZATION"""
        #initialize buttons
        #self.play_btn = Button(self.controls_frame, image=self.play_btn_img, borderwidth=0, command=lambda:play())
        self.pause_btn = Button(self.controls_frame, image=self.pause_btn_img, borderwidth=0, command=lambda:self.pause())
        self.skip_btn = Button(self.controls_frame, image=self.skip_btn_img, borderwidth=0, command=lambda:self.skip())
        self.prev_btn = Button(self.controls_frame, image=self.prev_btn_img, borderwidth=0, command=lambda:self.prev())
        self.stop_btn = Button(self.controls_frame, image=self.stop_btn_img, borderwidth=0, command=lambda:self.stop())
        self.loop_btn = Button(self.controls_frame, image=self.loop_btn_img,borderwidth=0, command=self.loop_activate)
        self.volume_slider = ttk.Scale(self.controls_frame, from_=0,to_=1, orient=HORIZONTAL,
            value=0.1, command=self.volume, length=100)
        #initialize song position slider
        self.slider_label = Label(self.song_slider_frame, text='', width=5)
        self.length_bar = Label(self.song_slider_frame, width=5, text='')
        #Song position slider
        self.position_slider = ttk.Scale(self.song_slider_frame, from_=0, to_=100, 
            orient=HORIZONTAL, value=0, command=self.position_slide, length=250)
        
        """CONTROL GRID PLACEMENTS"""
        #slider grid placements
        self.slider_label.grid(row=0,column=1)
        self.length_bar.grid(row=0, column=3)
        self.position_slider.grid(row=0, column=2, pady=0)
        #button grid placements
        self.pause_btn.grid(row=1, column=2, padx=10)
        self.skip_btn.grid(row=1, column=3, padx=10)
        self.prev_btn.grid(row=1, column=1, padx=10)
        self.stop_btn.grid(row=1, column=4, padx=10)
        self.loop_btn.grid(row=1, column=0, padx=10)
        self.volume_slider.grid(row=1, column=5)

    def create_playlist_display(self):
        """PLAYLIST INITIALIZATION"""
        self.scrollbar = tk.Scrollbar(self.playlist_frame, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')
        self.playlist_box = Listbox(self.playlist_frame, bg="white", fg="black", 
            selectbackground="dodger blue", selectforeground="white",
             selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set)
        self.playlist_box.config(height=22, width=30)
        self.playlist_box.bind('<Double-1>', self.play)

        self.scrollbar.config(command=self.playlist_box.yview)
        self.playlist_box.grid(row=0,column=0, rowspan=5)

        """DISPLAY INITIALIZATION"""
        self.canvas = Label(self.display_frame, image=self.cover_img)
        self.canvas.grid(row=0,column=0)
        self.track_bar = Label(self.display_frame, font=15, text='')
        self.track_bar.config(width=30,height=1)
        self.track_bar.grid(row=1,column=0,pady=10)

    def create_menu(self):
        """MENU INITIALIZATION"""
        #menu bar
        self.menu_ = Menu(self)
        self.master.config(menu=self.menu_)
        self.file_menu = Menu(self.menu_, tearoff=0)
        self.menu_.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Add Song(s) to Playlist", command=lambda:self.add_song())
        self.file_menu.add_command(label="Remove Selected Song from Playlist", command=lambda:self.remove_song())
        self.file_menu.add_command(label="Clear Playlist", command=lambda:self.clear_playlist())
        
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)
        self.grid(row=0,column=0)
        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0,weight=1)

    #button/menu functions
    def play(self, event=None):
        self.position_slider.config(value=0)
        if event is not None:
            self.current = self.playlist_box.curselection()[0]
            for i in range(len(self.playlist)):
                self.playlist_box.itemconfigure(i, bg="white")
        pygame.mixer.music.load(self.playlist[self.current])
        
        #display cover art of song
        song_file = TinyTag.get(self.playlist[self.current], image=True)
        artwork = song_file.get_image()
        pi = Image.open(io.BytesIO(artwork))
        max_size = (250, 250)
        pi.thumbnail(max_size)
        img = ImageTk.PhotoImage(pi)
        self.canvas.config(image = img)
        self.canvas.image = img

        self.paused = False
        self.played = True
        self.pause_btn.config(image=self.play_btn_img)
        self.playlist_box.activate(self.current) 
        self.playlist_box.itemconfigure(self.current, bg='sky blue')
        self.track_bar.config(text=self.playlist_box.get(ACTIVE))
        pygame.mixer.music.play(loops=0)
        self.play_time()

    def pause(self, event=None):
        if not self.paused:
            self.paused = True
            pygame.mixer.music.pause()
            self.pause_btn.config(image=self.pause_btn_img)
        else:
            if self.played == False:
                self.play()
            self.paused = False
            pygame.mixer.music.unpause()
            self.pause_btn.config(image=self.play_btn_img)
        
    def prev(self, event=None):
        #if song has been playing for more than 3 seconds, return to start of song
        if self.position_slider.get() > 3:
            self.position_slider.config(value=0)
            pygame.mixer.music.rewind()

        #play previous song in playlist
        elif len(self.playlist) > 1:
            self.master.focus_set()
            if self.current > 0:
                self.current -= 1
            else:
                self.current = 0
            self.playlist_box.itemconfigure(self.current + 1, bg='white')
            self.play()

    #only activated once current song as finished playing; autoplay feature
    def next_song(self):
        self.master.focus_set()
        if self.current == len(self.playlist)-1:
            self.playlist_box.itemconfigure(self.current, bg='white')
            if self.loop_flag == -1:
                self.current = 0
                self.play()
            else:
                self.stop()
        else:
            self.current += 1
            self.playlist_box.itemconfigure(self.current-1, bg='white')
            self.play()
            
    def skip(self):
        self.master.focus_set()
        #if current song is last in playlist, return to top of playlist
        if self.current == len(self.playlist)-1:
            self.playlist_box.itemconfigure(self.current, bg='white')
            self.current = 0
            self.play()
        else:
            self.current += 1
            self.playlist_box.itemconfigure(self.current-1, bg='white')
            self.play()
    
    def stop(self):
        #clear all text and cover image
        self.canvas.config(image = self.cover_img)
        self.canvas.image = self.cover_img
        self.slider_label.config(text='')
        self.length_bar.config(text='')
        self.position_slider.config(value=0)
        self.track_bar.config(text='')

        self.paused = True
        self.played = False
        pygame.mixer.music.stop()
        self.pause_btn.config(image=self.pause_btn_img)
        self.playlist_box.itemconfigure(self.current, bg='white')
        self.playlist_box.selection_clear(ACTIVE)

    def loop_activate(self):
        if self.loop_flag == 0:
            self.loop_flag = -1
            self.loop_btn.config(image=self.loop_on_btn_img)
        else:
            self.loop_flag = 0
            self.loop_btn.config(image=self.loop_btn_img)

    def add_song(self):
        #get song file directory
        file = filedialog.askopenfilenames(initialdir='Music/', title='Select a song', filetypes=(("mp3 Files", "*.mp3"), ("wav Files", "*.wav")))
        song_tuple = self.master.splitlist(file)
        song_list = list(song_tuple)
        #iterate through song list and add songs to playlist
        for song in song_list:
            self.playlist.append(song)
            tag = TinyTag.get(song)
            song_title = tag.title
            self.playlist_box.insert(END, song_title)
        if len(self.playlist) == 1:
            self.playlist_frame.config(text=f'Playlist - {str(len(self.playlist))} Song')
        else:
            self.playlist_frame.config(text=f'Playlist - {str(len(self.playlist))} Songs')
        #write songs to pickle
        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.playlist, f)
    
    #when app is opened, relist all pickled songs
    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            tag = TinyTag.get(song)
            song_title = tag.title
            self.playlist_box.insert(index, os.path.basename(song_title))

    def remove_song(self):
        song = self.playlist_box.curselection()
        if(self.current == song[0]): #if removed song is currently playing, stop
            self.stop()
        self.playlist.remove(self.playlist[int(song[0])])
        self.playlist_box.delete(song)
    
        if len(self.playlist) == 1:
            self.playlist_frame.config(text=f'Playlist - {str(len(self.playlist))} Song')
        else:
            self.playlist_frame.config(text=f'Playlist - {str(len(self.playlist))} Songs')
        #Rewrite pickle file
        emptylist = []
        with open('songs.pickle', 'wb') as o:
            pickle.dump(emptylist, o)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.playlist, f)
        

    def clear_playlist(self):
        self.playlist_box.delete(0, END)
        for i in range (len(self.playlist)):
            self.playlist.pop()
        self.stop()
        #Rewrite pickle file
        emptylist = []
        with open('songs.pickle', 'wb') as o:
            pickle.dump(emptylist, o)
        self.track_bar.config(text='')
        self.playlist_frame.config(text=f'Playlist - 0 Songs')

    #song position time function
    def play_time(self):
        if self.paused == False:
            #get current time/song position
            current_time = pygame.mixer.music.get_pos()/1000
            converted_time = time.strftime('%M:%S', time.gmtime(current_time))
            #get song length
            current_song = self.playlist_box.curselection()
            song_mut = MP3(self.playlist[self.current])
            self.song_length = song_mut.info.length
            converted_song_length = time.strftime('%M:%S',time.gmtime(self.song_length))
            self.length_bar.config(text=converted_song_length)
            current_time+=1

            #Update slider while song plays
            #end of song
            if int(self.position_slider.get())==int(self.song_length):
                self.slider_label.config(text=converted_song_length)
                self.next_song()

            elif self.paused:
                pass
            elif int(self.position_slider.get()==int(current_time)):
                self.slider_position=int(self.song_length)
                self.position_slider.config(to=self.slider_position, value=int(current_time))
            else: #update slider to current position in song
                slider_position = int(self.song_length)
                self.position_slider.config(to=slider_position, value=int(self.position_slider.get()))
                converted_time = time.strftime('%M:%S', time.gmtime(int(self.position_slider.get())))
                self.slider_label.config(text=converted_time)

                next_time = int(self.position_slider.get())+1
                self.position_slider.config(value=next_time)
                
        self.slider_label.after(1000, self.play_time)

    def position_slide(self, x):
        song = self.playlist_box.curselection()
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play(loops=0, start=int(self.position_slider.get()))

    def volume(self, x):
        pygame.mixer.music.set_volume(self.volume_slider.get())
        current_volume = pygame.mixer.music.get_volume()
        current_volume = current_volume*100
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Music Player")
    app = Application(root)
    root.geometry('700x400')
    root.mainloop()