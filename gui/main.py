import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.departure = tk.Entry(self)
        self.departure.insert(0 ,"Depart")
        self.departure.pack()
        self.destination = tk.Entry(self)
        self.destination.insert(0 ,"Arrivee")
        self.destination.pack()
        self.request = tk.Button(self)
        self.request["text"] = "Comment y aller ?"
        self.request["command"] = self.request_itinerary
        self.request.pack(side="top")
        self.quit = tk.Button(self, text="Quitter",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def request_itinerary(self):
        print('Going from {} to {}'.format(self.departure.get(), self.destination.get()))

root = tk.Tk()
app = Application(master=root)
app.mainloop()