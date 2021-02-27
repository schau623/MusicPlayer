from tkinter import *
import tkinter as tk
import pygame

class Application (Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        pygame.mixer.init()
        global paused
        #button functions/definitions
        def play(song):
            paused = FALSE
            pygame.mixer.music.load("")
            pygame.mixer.music.play(loops=0)
            
        def pause():
            paused = TRUE
            pygame.mixer.music.pause()

        #initialize buttons
        self.play_button = Button(self, pady=20, padx=20 ,text ="Play")
        self.pause_button = Button(self, pady=20, padx=20, text="Pause")
    
        #button grid placements
        self.play_button.grid(row=1, column=2)    
        self.pause_button.grid(row=1, column=1)  
        self.pack()
root = tk.Tk()
root.title("Music Player")
app = Application(root)
root.geometry("500x400")
root.mainloop()