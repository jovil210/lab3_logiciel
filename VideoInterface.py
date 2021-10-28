

import time,  os, queue, threading, tkinter as tk
from tkinter import ttk, filedialog as fd
import Playback as pb



STATES = {
    "stop": 0,
    "play": 1,
    "pause": 2
}

global video_state
video_state = STATES["stop"]


class GUI:
    
    def __init__(self, master):
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

        video_state = STATES["play"]
        
        self.queue = queue.Queue()
        video_thread = ThreadedTask(self.queue)
        video_thread.filename = filename
        video_thread.start()
        self.master.after(100, self.process_queue)
        
        

        

    def play_pause(self):
        global video_state
        if(video_state == STATES["play"]):
            pb.pause()
            video_state = STATES["pause"]
        elif(video_state == STATES["pause"]):
            pb.play()
            video_state = STATES["play"]
        else:
            pass

    def stop(self):
        global video_state
        pb.stop()
        video_state = STATES["stop"]      
        
    def restart(self):
        pb.restart()

    def accelerate(self):
        pb.accelerate()

    def process_queue(self):
        try:
            msg = self.queue.get_nowait()
            # Show result of the task if needed
        except queue.Empty:
            self.master.after(100, self.process_queue)

class ThreadedTask(threading.Thread):
    global video_state
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.filename = ""
        self.running= True

    def run(self):
        global video_state
        pb.start_video(self.filename)  # Simulate long running process
        while(video_state != STATES["stop"]):
            pass

root = tk.Tk()
main_ui = GUI(root)
root.mainloop()