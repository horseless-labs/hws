from tkinter import *
from tkinter import ttk

class CandidateScraperGUI(Frame):
    def __init__(self, master):
        self.master = master
        self.content = ttk.Frame(self.master)
        self.init_window()

    def init_window(self):
        self.master.title("Candidate Scraper Panel")
        self.content.grid(column=0, row=0)

        # COLUMN 0
        driver = ttk.Entry(self.content, justify=LEFT)
        driver.grid(column=0, row=0, padx=10, pady=8)

        query = ttk.Entry(self.content, justify=LEFT)
        query.grid(column=0, row=1, padx=10, pady=8)

        max_layers = ttk.Entry(self.content, justify=LEFT)
        max_layers.grid(column=0, row=2, padx=10, pady=8)

        max_nodes = ttk.Entry(self.content, justify=LEFT)
        max_nodes.grid(column=0, row=3, padx=10, pady=8)

        # COLUMN 1
        start_btn = Button(self.content, text="Start", width=15)
        start_btn.grid(column=1, row=0, padx=10, pady=8)

        pause_btn = Button(self.content, text="Pause", width=15)
        pause_btn.grid(column=1, row=1, padx=10, pady=8)

        cancel_btn = Button(self.content, text="Cancel", width=15)
        cancel_btn.grid(column=1, row=2, padx=10, pady=8)

"""
root = Tk()
app = CandidateScraperGUI(root)
root.mainloop()
"""
