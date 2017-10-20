import tkinter as tk
import tkinter.messagebox as messagebox
from model.Request import Request, InvalidRequestError
from webservice_caller.GoogleAPI import GoogleAPICaller

READABLE_FIELD_NAMES = {
    '_from_x': 'Depart x',
    '_from_y': 'Depart y',
    '_to_x': 'Destination x',
    '_to_y': 'Destination y'
}

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
            from_x = self.fields['Depart x'].get()
            from_y = self.fields['Depart y'].get()
            to_x = self.fields['Arrivee x'].get()
            to_y = self.fields['Arrivee y'].get()
            self.request = Request(from_x, from_y, to_x, to_y)
            self.process_request()
        except InvalidRequestError as e:
            field_name = e.field_name
            readable_name = READABLE_FIELD_NAMES[field_name]
            messagebox.showinfo("Lawen", "Le champ {} est mal rempli".format(readable_name))
    
    def process_request(self):
        google_api_caller = GoogleAPICaller(self.request)
        print(google_api_caller.get_times())
        

