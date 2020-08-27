# Change this later to only import the widgets needed from tkinter
from tkinter import *
from tkinter import ttk
import threading

import candidate_scraper_gui as csg
import image_scraper as imgx

class DownloaderGUI(Frame):
    def __init__(self, master):
        self.master = master
        self.content = ttk.Frame(self.master)
        self.version = "hws-0.0"
        self.init_window()

        # Status of the find_candidates thread
        self.fc_running = 0

    def init_window(self):
        self.master.title(self.version)
        self.content.columnconfigure(1, minsize=50)
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
        self.candidate_terms = Text(self.content, height=25, width=25)
        self.candidate_terms.grid(column=0, row=2, padx=10, pady=10, rowspan=40,
                sticky=W)

        # COLUMN 1
        find_candidates_btn = Button(self.content, text="Find Candidates",
                width=20, command=self.control_find_candidates)
        find_candidates_btn.grid(column=1, row=1, padx=30, pady=10, sticky=NE)

        scrape_btn = Button(self.content, text="Scrape Images", width=20,
                command=self.scrape_images)
        scrape_btn.grid(column=1, row=4, padx=10, pady=5, sticky=N)

        pause_btn = Button(self.content, text="Pause", width=20)
        pause_btn.grid(column=1, row=5, padx=10, pady=5, sticky=N)

        cancel_btn = Button(self.content, text="Cancel", width=20)
        cancel_btn.grid(column=1, row=6, padx=10, pady=5, sticky=N)

        save_btn = Button(self.content, text="Save", width=20)
        save_btn.grid(column=1, row=7, padx=10, pady=5, sticky=N)

    # TODO: clean up thread management overall
    def control_find_candidates(self):
        if self.fc_running == 0:
            fc_thread = threading.Thread(target=self.find_candidates)
            fc_thread.start()
            fc_running = 1
        if self.fc_running == 1:
            # TODO: pausing and stopping threads
            pass

    # Opens a separate window to find candidate nearest neighbor nodes.
    def find_candidates(self):
        csg_root = Tk()
        app = csg.CandidateScraperGUI(csg_root)
        csg_root.mainloop()
        self.candidate_terms.insert(END, app.candidates)

    # TODO: blocked terms that remove unwanted queries from final results.
    # Takes search terms from the Text box and returns a workable list of
    # terms for sequential search and download.
    def process_candidate_terms(self):
        terms = self.candidate_terms.get("1.0", END)
        # Dividing by newline happens first.
        terms = terms.split('\n')

        # Additionally separate by commas afterward
        # TODO: more thorough sanitization of input; user has access to Text
        # box.
        terms = [i.split(',') for i in terms]
        flat_terms = [i for sub in terms for i in sub]

        # Remove emptry strings that keep coming up
        final_terms = [i for i in flat_terms if i != '']
        return final_terms

    # TODO: Run on separate thread?
    # TODO: Add mechanism to keep track of which terms have been downloaded
    # in case of interruption.
    # TODO: logging, statistics about downloads, candidates for sites to be
    # added to block list.
    # Opens web drivers in sequence to download images for search terms found
    # in the Text box.
    def scrape_images(self):
        terms = self.process_candidate_terms()
        print(terms)
        scraper = imgx.ImageScraper(terms)

"""
root = Tk()
app = DownloaderGUI(root)
root.mainloop()
"""
