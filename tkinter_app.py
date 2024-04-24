from tkinter import ttk
from tkinter import *


class TK_inter:
    def __init__(self, root, app):
        self.app = app
        self.app.daemon = True
        self.app.start()

        self.mainframe = ttk.Frame(root, padding="100 10 50 40")
        self.root = root
        self.root.title(app)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        ttk.Label(self.mainframe, text='Pack_id').grid(column=1, row=1)

        if 'M3' not in str(self.app):
            ttk.Label(self.mainframe, text='Exchange').grid(column=1, row=2)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.get()

    def get(self):
        pack_id = ttk.Label(self.mainframe)
        pack_id["text"] = self.app.Pack_id
        pack_id.grid(column=2, row=1)
        exchange = ttk.Label(self.mainframe)
        exchange["text"] = self.app.Exchange
        exchange.grid(column=2, row=2)
        self.root.after(2000, self.get)
