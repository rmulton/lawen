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
        self.form_fields = {'Depart x':True, 'Depart y':True, 'Arrivee x':True, 'Arrivee y':True}
        self.form_buttons = {'Comment y aller ?': self.request_itinerary, 'Quitter':self.master.destroy}
        self.result_fields = {'Meilleur moyen d\'y aller : ': 'best_transport'}
        self.result_buttons = {'Retour': self.back_to_form}
        self.pack()
        self.display_form_frame()
    
    def back_to_form(self):
        self.result_frame.pack_forget()
        self.display_form_frame()

    def display_form_frame(self):
        self.create_form_frame()
        self.form_frame.pack()
    
    def pack_form_fields(self):
        for title, is_mistaken in self.form_fields.items():
            label = tk.Label(self.form_frame, text=title)
            label.pack()
            entry = tk.Entry(self.form_frame)
            entry.pack()
            self.form_fields[title] = entry
    
    def pack_form_buttons(self):
        for text, command in self.form_buttons.items():
            button = tk.Button(self.form_frame, text=text, command=command)
            button.pack()
    
    def create_form_frame(self):
        self.form_frame = tk.Frame(self)
        self.pack_form_fields()
        self.pack_form_buttons()
    
    def pack_results(self):
        for title, name in self.result_fields.items():
            label = tk.Label(self.result_frame, text=getattr(self, name))
            label.pack()
        for text, command in self.result_buttons.items():
            button = tk.Button(self.result_frame, text=text, command=command)
            button.pack()
    
    def create_result_frame(self):
        self.result_frame = tk.Frame(self)
        self.pack_results()

    def request_itinerary(self):
        try:
            from_x = self.form_fields['Depart x'].get()
            from_y = self.form_fields['Depart y'].get()
            to_x = self.form_fields['Arrivee x'].get()
            to_y = self.form_fields['Arrivee y'].get()
            self.request = Request(from_x, from_y, to_x, to_y)
            self.process_request()
        except InvalidRequestError as e:
            field_name = e.field_name
            readable_name = READABLE_FIELD_NAMES[field_name]
            messagebox.showinfo("Lawen", "Le champ {} doit etre une coordonnee GPS".format(readable_name))
    
    def process_request(self):
        google_api_caller = GoogleAPICaller(self.request)
        self.form_frame.pack_forget()
        self.best_transport = str(google_api_caller.get_times().best_transport)
        print(self.best_transport)
        self.create_result_frame()
        self.result_frame.pack()

        