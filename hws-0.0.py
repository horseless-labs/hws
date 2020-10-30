# Change this later to only import the widgets needed from tkinter
from tkinter import *
from tkinter import ttk

import candidate_scraper_gui as csg
import downloader_gui as dg

import time
import threading
import random
import queue

class ThreadManager:
    def __init__(self, master):
        self.master = master
        self.queue = queue.LifoQueue()
        self.dp_thread = threading.Thread(target=self.download_panel)
        self.dp_thread.start()

    def download_panel(self):
        gui = dg.DownloaderGUI(self.master, self.queue)
        self.queue.put("download_panel running")

    def check_per_second(self):
        pass

root = Tk()
tm = ThreadManager(root)
root.mainloop()
