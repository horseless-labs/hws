from tkinter import *
from tkinter import ttk

from selenium import webdriver

import candidate_scraper as cs

class CandidateScraperGUI(Frame):
    def __init__(self, master, q):
        self.thread_queue = q
        self.master = master
        self.content = ttk.Frame(self.master)
        self.init_window()

        # The list of candidate neighbors to be passed to DownloaderGUI
        self.candidates = str()

    def init_window(self):
        self.master.title("Candidate Scraper Panel")
        self.content.grid(column=0, row=0)

        # COLUMN 0
        # Labels
        driver_label = ttk.Label(self.content, text="Web Driver Path:", justify=LEFT)
        driver_label.grid(column=0, row=0)

        query_label = ttk.Label(self.content, text="Query:", justify=LEFT)
        query_label.grid(column=0, row=1)

        max_layers_label = ttk.Label(self.content, text="Max Num. of Layers:", justify=LEFT)
        max_layers_label.grid(column=0, row=2)

        max_nodes_label = ttk.Label(self.content, text="Max Num. of Nodes:", justify=LEFT)
        max_nodes_label.grid(column=0, row=3)
        
        # Entry widgets
        self.driver = ttk.Entry(self.content, justify=LEFT)
        self.driver.insert(0, "../chromedriver")
        self.driver.grid(column=1, row=0, padx=10, pady=8)

        self.seed_term = ttk.Entry(self.content, justify=LEFT)
        self.seed_term.grid(column=1, row=1, padx=10, pady=8)

        self.max_layers = ttk.Entry(self.content, justify=LEFT)
        self.max_layers.insert(0, 2)
        self.max_layers.grid(column=1, row=2, padx=10, pady=8)

        self.max_nodes = ttk.Entry(self.content, justify=LEFT)
        self.max_nodes.insert(0, 1)
        self.max_nodes.grid(column=1, row=3, padx=10, pady=8)

        # COLUMN 1
        start_btn = Button(self.content, text="Start", width=15, command=self.start)
        start_btn.grid(column=2, row=0, padx=10, pady=8)

        pause_btn = Button(self.content, text="Pause", width=15)
        pause_btn.grid(column=2, row=1, padx=10, pady=8)

        cancel_btn = Button(self.content, text="Cancel", width=15)
        cancel_btn.grid(column=2, row=2, padx=10, pady=8)

    def get_values(self):
        self.driver_text = self.driver.get()
        self.query_text = self.seed_term.get()

        if self.query_text == "":
            print("Must specify a query")
            return

        try:
            self.max_layers_text = int(self.max_layers.get())
        except:
            print("The maximum number of layers must be an integer")
            return
        
        try:
            self.max_nodes_text = int(self.max_nodes.get())
        except:
            print("The maximum number of nodes must be an integer")
            return

    def start(self):
        self.get_values()
        self.wd = webdriver.Chrome(executable_path=self.driver_text)

        scraper = cs.NeighborNodeFinder(self.query_text, self.wd, self.max_nodes_text, self.max_layers_text)
        self.candidates = scraper.tmp_list
        self.wd.quit()


"""
root = Tk()
app = CandidateScraperGUI(root)
root.mainloop()
"""
