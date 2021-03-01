from tkinter import *
import tkinter as tk
from tkinter import filedialog
import pygame
from tinytag import TinyTag 
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


class Application (Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        pygame.mixer.init()

        global paused 
        paused = False
        playlist = []
        pygame.mixer.music.set_volume(0.1)
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
            #self.position_bar.config(text='')
            self.length_bar.config(text='')
            self.slider_label.config(text='')
            self.position_slider.config(value=0)
            next_song = self.playlist_box.curselection()
            next_song = next_song[0]+1
            pygame.mixer.music.load(playlist[next_song])
            pygame.mixer.music.play(loops=0)
            self.playlist_box.selection_clear(0, END)
            self.playlist_box.activate(next_song)
            self.playlist_box.selection_set(next_song, last=None)

        def prev():
            #self.position_bar.config(text='')
            self.length_bar.config(text='')
            self.slider_label.config(text='')
            self.position_slider.config(value=0)
            prev_song = self.playlist_box.curselection()
            prev_song = prev_song[0]-1
            pygame.mixer.music.load(playlist[prev_song])
            pygame.mixer.music.play(loops=0)
            self.playlist_box.selection_clear(0, END)
            self.playlist_box.activate(prev_song)
            self.playlist_box.selection_set(prev_song, last=None)
        
        def stop():
            self.slider_label.config(text='')
            self.length_bar.config(text='')
            self.position_slider.config(value=0)
            global paused
            paused = True
            pygame.mixer.music.stop()
            self.playlist_box.selection_clear(ACTIVE)
            #self.position_bar.config(text='')

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
            playlist.remove(ANCHOR)
            pygame.mixer.music.stop()

        def clear_playlist():
            self.playlist_box.delete(0, END)
            for i in range (len(playlist)):
                playlist.pop()
            pygame.mixer.music.stop()

        #song position time function
        def play_time():
            global paused
            if paused == False:
                #get current time/song position
                current_time = pygame.mixer.music.get_pos()/1000
                converted_time = time.strftime('%M:%S', time.gmtime(current_time))
                #self.position_bar.config(text=converted_time)
                #update time
                #self.position_bar.after(1000, play_time)
                

                #get song length
                current_song = self.playlist_box.curselection()
                song_mut = MP3(playlist[int(current_song[0])])
                global song_length
                song_length = song_mut.info.length
                converted_song_length = time.strftime('%M:%S',time.gmtime(song_length))
                self.length_bar.config(text=converted_song_length)
                #self.length_bar.after(1000, play_time)
                current_time+=1

                if int(self.position_slider.get())==int(song_length):
                    self.slider_label.config(text=converted_song_length)
                
                elif paused:
                    pass
                
                elif int(self.position_slider.get()==int(current_time)):
                    self.slider_position=int(song_length)
                    self.position_slider.config(to=self.slider_position, value=int(current_time))
                
                else: #update slider to current position in song
                    slider_position = int(song_length)
                    self.position_slider.config(to=slider_position, value=int(self.position_slider.get()))
                    converted_time = time.strftime('%H:%M:%S', time.gmtime(int(self.position_slider.get())))
                    self.slider_label.config(text=converted_time)

                    next_time = int(self.position_slider.get())+1
                    self.position_slider.config(value=next_time)
                    
            self.slider_label.after(1000, play_time)

        def position_slide(x):
            song = self.playlist_box.curselection()
            pygame.mixer.music.load(playlist[int(song[0])])
            pygame.mixer.music.play(loops=0, start=int(self.position_slider.get()))

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
        self.position_frame = Frame(self)
        #self.position_bar = Label(self.position_frame, width=10, text='', bd=1, relief=GROOVE)
        self.length_bar = Label(self.position_frame, width=10, text='', bd=1, relief=GROOVE)
        #Song position slider
        self.position_slider = ttk.Scale(self.position_frame, from_=0, to_=100, orient=HORIZONTAL, value=0, command=position_slide, length=360)
        self.slider_label = Label(self.position_frame, text='', width=10, bd=1, relief=GROOVE)
        
        #UI item placements
        self.grid(row=0,column=0)
        master.columnconfigure(0,weight=1)
        master.rowconfigure(0,weight=1)
        #buttons
        self.buttons_frame.grid(row=0, column = 3)
        self.position_frame.grid(row=1, column=3, pady=10)
        self.play_btn.grid(row=1, column=2, padx=10)
        self.pause_btn.grid(row=1, column=3, padx=10)
        self.skip_btn.grid(row=1, column=4, padx=10)
        self.prev_btn.grid(row=1, column=1, padx=10)
        self.stop_btn.grid(row=1, column=5, padx=10)
        #playlist box
        self.playlist_box.grid(row=3,column=3)
        #song pos slider
        self.slider_label.grid(row=1,column=2)
        self.length_bar.grid(row=1, column=4)
        self.position_slider.grid(row=1, column=3)
        
        #self.pack()
root = tk.Tk()
root.title("Music Player")
app = Application(root)
root.geometry("600x500")
root.mainloop()