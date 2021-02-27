from tkinter import *
import tkinter as tk
import pygame

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

        #button images
        self.play_btn_img = PhotoImage(file='imgs/play_img.png')
        self.pause_btn_img = PhotoImage(file='imgs/pause_img.png')
        self.skip_btn_img = PhotoImage(file='imgs/skip_img.png')
        self.prev_btn_img = PhotoImage(file='imgs/prev_img.png')
        self.stop_btn_img = PhotoImage(file='imgs/stop_img.png')
        #initialize playlist box
        self.playlist_box = Listbox(self, bg="white", fg="black", width=65, height=20)
        
        #initialize buttons
        self.buttons_frame = Frame(self)
        self.play_btn = Button(image=self.play_btn_img, borderwidth=0, command=lambda:play())
        self.pause_btn = Button(image=self.pause_btn_img, borderwidth=0)
        self.skip_btn = Button(image=self.skip_btn_img, borderwidth=0)
        self.prev_btn = Button(image=self.prev_btn_img, borderwidth=0)
        self.stop_btn = Button(image=self.stop_btn_img, borderwidth=0, command=lambda:stop())
        #button grid placements

        self.play_btn.grid(row=1, column=2)
        self.pause_btn.grid(row=1, column=3)
        self.skip_btn.grid(row=1, column=4)
        self.prev_btn.grid(row=1, column=1)
        self.stop_btn.grid(row=1, column=5)
        self.playlist_box.grid(row=2,column=3)
        self.pack()
root = tk.Tk()
root.title("Music Player")
app = Application(root)
#root.geometry("500x400")
root.mainloop()