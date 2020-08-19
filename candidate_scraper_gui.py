from tkinter import *
from tkinter import ttk

class CandidateScraperGUI(Frame):
    def __init__(self, master):
        self.master = master
        self.content = ttk.Frame(self.master)
        self.init_window()

    def init_window(self):
        self.master.title("Candidate Scraper Panel")
