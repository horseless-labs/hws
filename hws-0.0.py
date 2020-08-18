# Change this later to only import the widgets needed from tkinter
from tkinter import *
from tkinter import ttk

class ScraperControlPanel(Frame):
    def __init__(self, master):
        self.master = master
        self.content = ttk.Frame(self.master)
        self.version = "hws-0.0"
        self.init_window()

    def init_window(self):
        self.master.title(self.version)

        self.content.grid(column=0, row=0)

        # COLUMN 0
        seed_label = ttk.Label(self.content, text="Seed Search Term",
                justify=LEFT)
        seed_label.grid(column=0, row=0, padx=10, pady=5, sticky=W)

        # User entry for the initial search term, whose neighbors will be
        # found by a driver on a separate thread.
        search_seed = ttk.Entry(self.content, justify=LEFT)
        search_seed.grid(column=0, row=1, padx=10, pady=5, sticky=W)

        # List of terms neighboring the seed term that were found by the
        # driver
        candidate_terms = Text(self.content, height=25, width=25)
        candidate_terms.grid(column=0, row=2, padx=10, pady=5, sticky=W)

        # COLUMN 1
        find_candidates_btn = Button(self.content, text="Find Candidates",
                width=20)
        find_candidates_btn.grid(column=1, row=0, padx=10, pady=10, sticky=NE)

        scrape_btn = Button(self.content, text="Scrape Images", width=20)
        scrape_btn.grid(column=1, row=1, padx=10, pady=5, sticky=N)

        pause_btn = Button(self.content, text="Pause", width=20)
        pause_btn.grid(column=1, row=2, padx=10, pady=5, sticky=N)

        cancel_btn = Button(self.content, text="Cancel", width=20)
        cancel_btn.grid(column=1, row=3, padx=10, pady=5, sticky=N)

        save_btn = Button(self.content, text="Save", width=20)
        save_btn.grid(column=1, row=4, padx=10, pady=5, sticky=N)

root = Tk()
app = ScraperControlPanel(root)
root.mainloop()
