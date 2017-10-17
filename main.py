"""main module for the interface"""

import tkinter as tk
import os
from model.Request import Request
from gui.GUIApplication import GUIApplication

if __name__ == "__main__":

    app = GUIApplication(master=tk.Tk())
    app.mainloop()