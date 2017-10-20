import tkinter as tk
import tkinter.messagebox as messagebox
from model.Request import Request
from webservice_caller.GoogleAPI import GoogleAPICaller

class GUIApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.fields = {'Depart x':True, 'Depart y':True, 'Arrivee x':True, 'Arrivee y':True}
        self.buttons = {'Comment y aller ?': self.request_itinerary, 'Quitter':self.master.destroy}
        self.create_widgets()
    
    def pack_fields_with_label(self):
        for title, is_mistaken in self.fields.items():
            label = tk.Label(self, text=title)
            label.pack()
            entry = tk.Entry(self)
            entry.pack()
            self.fields[title] = entry
    
    def pack_buttons(self):
        for text, command in self.buttons.items():
            button = tk.Button(self, text=text, command=command)
            button.pack()

    def create_widgets(self):
        self.pack_fields_with_label()
        self.pack_buttons()

    def request_itinerary(self):
        try:
            request_from = [self.fields['Depart x'].get(), self.fields['Depart y'].get()]
            request_to = [self.fields['Arrivee x'].get(), self.fields['Arrivee y'].get()]
            self.request = Request(request_from,request_to)
            self.process_request()
        except ValueError:
            messagebox.showinfo("Lawen", "Tu as oublie de remplir un champ")
    
    def process_request(self):
        google_api_caller = GoogleAPICaller(self.request)
        print(google_api_caller.get_possibilities())
        

