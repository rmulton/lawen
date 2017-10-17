"""main module for the interface"""

import tkinter as tk
import os
from model.Request import Request
from gui.GUIApplication import GUIApplication

if __name__ == "__main__":

    root = tk.Tk()
    app = GUIApplication(master=root)
    app.mainloop()