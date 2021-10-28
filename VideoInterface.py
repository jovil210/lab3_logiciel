
# Librairies externes
import time,  os, queue, threading, tkinter as tk
from tkinter import ttk, filedialog as fd
# Module fait en c++
import Playback


#Variable des états du vidéo
STATES = {
    "stop": 0,
    "play": 1,
    "pause": 2
}

#Variable global afin que les deux classes puissent voir l'état de la vidéo
global video_state
video_state = STATES["stop"]


class GUI:
    
    def __init__(self, master):
        #Initialisation de l'interface graphique
        self.master = master
        master.title("My video player")
        master.geometry("500x400")
        self.open_button = tk.Button(master,text='Select your video', command=self.select)
        self.open_button.pack(pady=20)
        self.play_pause_button = tk.Button(master,text='Play/Pause', command=self.play_pause)
        self.play_pause_button.pack(pady=20)
        self.stop_button = tk.Button(master,text='Stop', command=self.stop)
        self.stop_button.pack(pady=20)
        self.restart_button = tk.Button(master,text='Restart', command=self.restart)
        self.restart_button.pack(pady=20)
        self.accelerate_button = tk.Button(master,text='Accelerate', command=self.accelerate)
        self.accelerate_button.pack(pady=20)

    def select(self):
        
        global video_state
        # Sélection du fichier
        filetypes = (
            ('AVI files', '*.avi'),
            ('MP4 files', '*.mp4*'),
            ('Matroska files', '*.mkv*'),
            ('Windows Media Video files', '*.wmv*'),
            ('QuickTime files', '*.mov*'),
            ('WebM files', '*.webm'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Select a video',
            initialdir='/',
            filetypes=filetypes)

        #Démarrage de la vidéo
        video_state = STATES["play"]
        self.queue = queue.Queue()
        video_thread = ThreadedTask(self.queue)
        video_thread.filename = filename
        video_thread.start()
        self.master.after(100, self.process_queue)
        
        

        

    def play_pause(self):
        global video_state
        # Vérification de l'état afin de soit démarrer ou mettre en pause
        if(video_state == STATES["play"]):
            Playback.pause()
            video_state = STATES["pause"]
        elif(video_state == STATES["pause"]):
            Playback.play()
            video_state = STATES["play"]
        else:
            print("Please chose a video")    

    def stop(self):
        global video_state
        # Arret de la vidéo
        if(video_state != STATES["stop"]):
            Playback.stop()
            video_state = STATES["stop"]
        else:
            print("Please chose a video")      
        
    def restart(self):
        # Redémarrage de la vidéo
        if(video_state != STATES["stop"]):
            Playback.restart()
        else:
            print("Please chose a video")    

    def accelerate(self):
        #Accélération de la vidéo
        if(video_state != STATES["stop"]):
            Playback.accelerate()
        else:
            print("Please chose a video")    
    def process_queue(self):
        # Gestionnaire de processus
        try:
            msg = self.queue.get_nowait()
            # Show result of the task if needed
        except queue.Empty:
            self.master.after(100, self.process_queue)

class ThreadedTask(threading.Thread):
    global video_state
    def __init__(self, queue):
        #Initialisation d'un thread de vidéo
        super().__init__()
        self.queue = queue
        self.filename = ""
        self.running= True

    def run(self):
        # Démarrage du thread de la vidéo
        global video_state
        Playback.start_video(self.filename)  # Simulate long running process
        while(video_state != STATES["stop"]):
            pass
        
if(__name__ == "__main__"):
    root = tk.Tk()
    main_ui = GUI(root)
    root.mainloop()