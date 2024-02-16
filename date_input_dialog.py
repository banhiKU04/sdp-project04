from tkinter import ttk, simpledialog

class DateInputDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt):
        self.prompt = prompt
        super().__init__(parent, title)

    def body(self, master):
        ttk.Label(master, text=self.prompt).grid(row=0)
        self.entry = ttk.Entry(master)
        self.entry.grid(row=1)
        return self.entry

    def apply(self):
        self.result = self.entry.get()
