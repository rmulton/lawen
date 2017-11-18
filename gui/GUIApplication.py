import tkinter as tk
import tkinter.messagebox as messagebox
from model.Request import Request, InvalidRequestError, NotInParisRequestError
from webservice_caller.AllAPICaller import AllAPICaller, MainCallerError
from model.UserRequest import UserRequest, LocationNotFoundError, EmptyFieldError
from webservice_caller.GeocodingAPICaller import AddressNotFoundError, GeocodingAPICallerError
import time

# Readable names of the fields required in the GUI form
READABLE_FIELD_NAMES = {
    '_from_location': 'Departure',
    '_to_location': 'Destination',
}

class GUIApplication(tk.Frame):
    '''
    GUI form. Get the gps coordinates of A and B. Returns the best way to go from A to B.
    '''
    def __init__(self, master=None):
        super().__init__(master)

        # Input form
        self.form_fields = {'Departure':True, 'Destination':True}
        self.form_buttons = {'How can I go there ?': self.request_itinerary, 'Quit':self.master.destroy}
        self.form_frame = tk.Frame()

        # Result displayer
        self.result_fields = {'You asked : \n': 'user_request', 
                                '\nThe weather conditions are : \n': 'weather',
                                '\nThe best way to go is : \n': 'best_transport'}
        self.result_buttons = {'Back': self.back_to_form}
        self.result_frame = tk.Frame()

        self.pack()
        self.display_form_frame()
    
    def back_to_form(self):
        '''
        Go back to the input form
        '''
        self.delete_result_frame()
        self.result_frame.pack_forget()

        self.display_form_frame()

    # Form frame
    def display_form_frame(self):
        '''
        Display the input form frame
        '''
        # Text
        for title, is_mistaken in self.form_fields.items():
            label = tk.Label(self.form_frame, text=title)
            label.pack()
            entry = tk.Entry(self.form_frame)
            entry.pack()
            self.form_fields[title] = entry
        # Buttons
        for text, command in self.form_buttons.items():
            button = tk.Button(self.form_frame, text=text, command=command)
            button.pack()
        # Pack
        self.form_frame.pack()
        
    def delete_form_frame(self):
        '''
        Display the input form frame
        '''
        self.form_frame.pack_forget()
        self.form_frame = tk.Frame()
   
    # Result frame
    def display_result_frame(self):
        '''
        Display the result frame
        '''
        # Update results
        self.best_transport = self.possibilities.best_transport
        self.weather = self.possibilities.weather
        # Display results
        for title, name in self.result_fields.items():
            text = title + str(getattr(self, name))
            label = tk.Label(self.result_frame, text=str(text))
            label.pack()
        for text, command in self.result_buttons.items():
            button = tk.Button(self.result_frame, text=str(text), command=command)
            button.pack()
        self.result_frame.pack()
    
    def delete_result_frame(self):
        '''
        Delete the result frame
        '''
        self.result_frame.pack_forget()
        self.result_frame = tk.Frame()
    
    # Process the request
    def request_itinerary(self):
        '''
        Get the inputs and check their format
        '''
        self.delete_form_frame()
        try:
            from_location = self.form_fields['Departure'].get()
            to_location = self.form_fields['Destination'].get()
            self.user_request = UserRequest(from_location, to_location)
            self.process_request()
        except LocationNotFoundError as e:
            field_name = e.field_name
            readable_name = READABLE_FIELD_NAMES[field_name]
            messagebox.showinfo("Lawen", "{} field not found\nPlease fill in with the address".format(readable_name))
            self.back_to_form()
        except EmptyFieldError as e:
            field_name = e.field_name
            readable_name = READABLE_FIELD_NAMES[field_name]
            messagebox.showinfo("Lawen", "{} field not found\nPlease fill in with the address".format(readable_name))
            self.back_to_form()
        except NotInParisRequestError as e:
            point_name = e.field_name
            readable_name = READABLE_FIELD_NAMES[point_name]
            messagebox.showinfo("Lawen", "{} must be inside paris".format(readable_name))
            self.back_to_form()
        except GeocodingAPICallerError as e:
            print(e)
            messagebox.showinfo('Lawen', 'Their seems to be a problem with the internet. You may have to change your API key.')
            self.back_to_form()
        except MainCallerError as e:
            print(e)
            messagebox.showinfo('Lawen', 'Their seems to be a problem with the internet. You may have to change your API key.')
            self.back_to_form()
    
    def process_request(self):
        '''
        Process the request given the inputs and display the results
        '''
        api_caller = AllAPICaller(self.user_request.coordinates)
        self.possibilities = api_caller.get_possibilities()
        self.display_result_frame()

        