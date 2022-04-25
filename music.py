import os
import tkinter as tk
from tkinter import PhotoImage
from pygame import mixer
from videoTest import liveVideoTest

### Create the main windows that is music player
class Player(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        mixer.init()
        
        self.playlist = []
        self.current = 0
        self.paused = True
        self.played = False
        
        ### Call the createFrames function 
        self.createFrames()
        self.trackWidgets()
        self.controlWidgets()
        self.trackListWidgets()
        
    ### Function to create the frame inside the window
    def createFrames(self):
        ### First frame
        self.track = tk.LabelFrame(self, text='Song Track', font=("times new roman", "15", "bold"), bg="grey", fg="white", bd=5, relief=tk.GROOVE)
        self.track.configure(width=700, height=500)
        self.track.grid(row=0, column=0, padx=10)
        
        ### Second frame
        self.tracklist = tk.LabelFrame(self, text=f'Playlist', font=("times new roman", "13", "bold"), bg="grey", fg="white", bd=5, relief=tk.GROOVE)
        self.tracklist.configure(width=320, height=700)
        self.tracklist.grid(row=0, column=1, rowspan=3, pady=5)
        
        ### Third frame
        self.controls = tk.LabelFrame(self, font=("times new roman", "15", "bold"), bg="white", fg="white", bd=5, relief=tk.GROOVE)
        self.controls.configure(width=700, height=140)
        self.controls.grid(row=1, column=0, pady=20, padx=10)
    
    def trackWidgets(self):
        self.canvas = tk.Label(self.track, image=img)
        self.canvas.configure(width=700, height=530)
        self.canvas.grid(row=0, column=0)
        
        self.songTrack = tk.Label(self.track, font=("times new roman", "15", "bold"), bg='white', fg='dark blue')
        self.songTrack['text'] = 'Emotion Based Music Player'
        self.songTrack.configure(width=30, height=1)
        self.songTrack.grid(row=1, column=0)
    
    def controlWidgets(self):
        self.loadSongs = tk.Button(self.controls, bg='green', fg='white', font=("times new roman", "15", "bold"))
        self.loadSongs['text'] = "Detect Emotion"
        self.loadSongs['command'] = self.retrieveSongs
        self.loadSongs.grid(row=0, column=0, padx=10, pady=5)
        
        self.prev = tk.Button(self.controls, image=prev)
        self.prev['command'] = self.previousSongs
        self.prev.grid(row=0, column=1, padx=10, pady=5)
        
        self.pause = tk.Button(self.controls, image=pause)
        self.pause['command'] = self.pauseSongs
        self.pause.grid(row=0, column=2, padx=10, pady=5)
        
        self.next = tk.Button(self.controls, image=next_)
        self.next['command'] = self.nextSongs
        self.next.grid(row=0, column=3, padx=10, pady=5)
        
        self.volume = tk.DoubleVar()
        self.slider = tk.Scale(self.controls, from_=0, to=10, orient=tk.HORIZONTAL)
        self.slider['variable'] = self.volume
        self.slider.set(8)
        mixer.music.set_volume(0.8)
        self.slider['command'] = self.changeVolume
        self.slider.grid(row=0, column=4, padx=10, pady=5)
    
    def trackListWidgets(self):
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, rowspan=5, sticky='ns')
        
        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE, yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
        
        self.enumerateSongs()
        self.list.config(height=55, width=35)
        self.list.bind('<Double-1>', self.playSong)
        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)
    
    def enumerateSongs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))
    
    def retrieveSongs(self):
        self.songlist = []
        
        result = liveVideoTest()
        status = result[0]
        directory = result[1]
        
        for root_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    path = (root_ + '/' + file).replace('\\', '/')
                    self.songlist.append(path)

        self.playlist = self.songlist
        self.tracklist['text'] = f'{status} Song List - {str(len(self.playlist))}'
        self.list.delete(0, tk.END)
        self.enumerateSongs()
    
    def playSong(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg='white')
                
        mixer.music.load(self.playlist[self.current])
        self.pause['image'] = play
        self.paused = False
        self.played = True
        self.songTrack['anchor'] = 'w'
        self.songTrack['text'] = os.path.basename(self.playlist[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg='sky blue')
        mixer.music.play()  
    
    def pauseSongs(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = pause
        else:
            if self.played == False:
                self.playSong()
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = play
    
    def previousSongs(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
            
        self.list.itemconfigure(self.current+1, bg='white')
        self.playSong()
    
    def nextSongs(self):
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
            self.playSong()
        self.list.itemconfigure(self.current-1, bg='white')
        self.playSong()
    
    def changeVolume(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v/10)

root = tk.Tk()
root.geometry('1000x700')
root.wm_title('Emotion Based Music Player')
root.resizable(width=0, height=0)

img = PhotoImage(file='images/music.gif')
next_ = PhotoImage(file = 'images/next.gif')
prev = PhotoImage(file='images/previous.gif')
play = PhotoImage(file='images/play.gif')
pause = PhotoImage(file='images/pause.gif')

### Call the main window class
app = Player(master=root)
app.mainloop()