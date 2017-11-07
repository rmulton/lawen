import tkinter as tk
import tkinter.messagebox as messagebox
from model.Request import Request, InvalidRequestError, NotInParisRequestError
from webservice_caller.AllAPICaller import AllAPICaller, MainCallerError
from model.UserRequest import UserRequest, LocationNotFoundError, EmptyFieldError
from webservice_caller.GeocodingAPICaller import AddressNotFoundError, GeocodingAPICallerError
# Readable names of the fields required in the GUI form
READABLE_FIELD_NAMES = {
    '_from_location': 'Depart',
    '_to_location': 'Destination',
    'origin': 'L\'origine',
    'destination': 'La destination'
}

class GUIApplication(tk.Frame):
    '''
    GUI form. Get the gps coordinates of A and B. Returns the best way to go from A to B.
    '''
    def __init__(self, master=None):
        super().__init__(master)

        # Input form
        self.form_fields = {'Depart':True, 'Destination':True}
        self.form_buttons = {'Comment y aller ?': self.request_itinerary, 'Quitter':self.master.destroy}

        # Result displayer
        self.result_fields = {'Meilleur moyen d\'y aller : ': 'best_transport'}
        self.result_buttons = {'Retour': self.back_to_form}

        self.pack()
        self.display_form_frame()
    
    def back_to_form(self):
        '''
        Go back to the input form
        '''
        self.result_frame.pack_forget()
        self.display_form_frame()

    def display_form_frame(self):
        '''
        Display the input form
        '''
        self.create_form_frame()
        self.form_frame.pack()
    
    def pack_form_fields(self):
        '''
        Pack the input form fields in the GUI app
        '''
        for title, is_mistaken in self.form_fields.items():
            label = tk.Label(self.form_frame, text=title)
            label.pack()
            entry = tk.Entry(self.form_frame)
            entry.pack()
            self.form_fields[title] = entry
    
    def pack_form_buttons(self):
        '''
        Pack the input form buttons in the GUI app
        '''
        for text, command in self.form_buttons.items():
            button = tk.Button(self.form_frame, text=text, command=command)
            button.pack()
    
    def create_form_frame(self):
        '''
        Create the input form
        '''
        self.form_frame = tk.Frame(self)
        self.pack_form_fields()
        self.pack_form_buttons()
    
    def pack_results(self):
        '''
        Pack the result displayer in the GUI app
        '''
        for title, name in self.result_fields.items():
            text = title + getattr(self, name)
            label = tk.Label(self.result_frame, text=text)
            label.pack()
        for text, command in self.result_buttons.items():
            button = tk.Button(self.result_frame, text=text, command=command)
            button.pack()
    
    def create_result_frame(self):
        '''
        Create the result displayer
        '''
        self.result_frame = tk.Frame(self)
        self.pack_results()

    def request_itinerary(self):
        '''
        Get the inputs and check their format
        '''
        try:
            from_location = self.form_fields['Depart'].get()
            to_location = self.form_fields['Destination'].get()
            self.user_request = UserRequest(from_location, to_location)
            self.process_request()
        except LocationNotFoundError as e:
            field_name = e.field_name
            readable_name = READABLE_FIELD_NAMES[field_name]
            messagebox.showinfo("Lawen", "Le champ {} n\'a pas été trouvé\nVeuillez préciser l\'adresse".format(readable_name))
        except EmptyFieldError as e:
            field_name = e.field_name
            readable_name = READABLE_FIELD_NAMES[field_name]
            messagebox.showinfo("Lawen", "Le champ {} doit être rempli".format(readable_name))
        except InvalidRequestError as e:
            field_name = e.field_name
            readable_name = READABLE_FIELD_NAMES[field_name]
            messagebox.showinfo("Lawen", "Le champ {} doit etre une coordonnee GPS".format(readable_name))
        except NotInParisRequestError as e:
            point_name = e.field_name
            readable_name = READABLE_FIELD_NAMES[point_name]
            messagebox.showinfo("Lawen", "{} doit etre dans Paris : 48.816999,2.23851 -> 48.897749,2.410515".format(readable_name))
        except GeocodingAPICallerError as e:
            messagebox.showinfo('Lawen', 'Oups... problème de connexion internet, merci de réessayer.')
        except MainCallerError as e:
            messagebox.showinfo('Lawen', 'Oups... problème de connexion internet, merci de réessayer.')
    
    def process_request(self):
        '''
        Process the request given the inputs and display the results
        '''
        
        api_caller = AllAPICaller(self.user_request.coordinates)
        self.form_frame.pack_forget()
        possibilities = api_caller.get_possibilities()
        self.best_transport = str(possibilities.best_transport)
        self.create_result_frame()
        self.result_frame.pack()

        