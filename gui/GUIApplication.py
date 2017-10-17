import tkinter as tk
from model.Request import Request
from webservice_caller.GoogleAPI import GoogleAPICaller

class GUIApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.departure_x = tk.Entry(self)
        self.departure_x.insert(0 ,"Depart x")
        self.departure_x.pack()

        self.departure_y = tk.Entry(self)
        self.departure_y.insert(0 ,"Depart y")
        self.departure_y.pack()

        self.destination_x = tk.Entry(self)
        self.destination_x.insert(0 ,"Arrivee x")
        self.destination_x.pack()

        self.destination_y = tk.Entry(self)
        self.destination_y.insert(0 ,"Arrivee y")
        self.destination_y.pack()

        self.request = tk.Button(self)
        self.request["text"] = "Comment y aller ?"
        self.request["command"] = self.request_itinerary
        self.request.pack(side="top")
        self.quit = tk.Button(self, text="Quitter",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def request_itinerary(self):
        request_from = [self.departure_x.get(), self.departure_y.get()]
        request_to = [self.destination_x.get(), self.destination_y.get()]
        print('Going from {} to {}'.format(request_from, request_to))
        self.request = Request(request_from,request_to)
        self.process_request()
    
    def process_request(self):
        google_api_caller = GoogleAPICaller(self.request)
        print(google_api_caller.get_possibilities())
        

