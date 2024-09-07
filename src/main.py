import customtkinter as ctk
import tkinter  as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinterdnd2 import TkinterDnD, DND_ALL
from Seismicwidget import create_seismic_input_widgets
from PIL import Image
mode = "dark"
class CTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

def calculate_seismic_load(site_class_entry, importance_factor_entry, spectral_response_acceleration_entry):
    # Retrieve user input
    site_class = float(site_class_entry.get().strip() or "0")  # Get value from Entry widget
    importance_factor = float(importance_factor_entry.get().strip() or "0")
    spectral_response_acceleration = float(spectral_response_acceleration_entry.get().strip() or "0")

    # Calculate seismic load
    seismic_load = compute_seismic_load(site_class, importance_factor, spectral_response_acceleration)
    print(f"Seismic Load: {seismic_load} kN")


def compute_seismic_load(site_class, importance_factor, spectral_response_acceleration):
    # site_class is now a float, so we don't need to call .get()
    # You might need a conversion or validation based on what you expect

    # Assuming amplification_factors is a dictionary of floats
    amplification_factors = {
        # Example data; replace with actual values
        0.0: 1.0,  # This is a placeholder; replace with your actual values
        1.0: 1.5,
        2.0: 2.0,
    }
    
    # Use the float value to get the amplification factor
    amplification_factor = amplification_factors.get(site_class, 1.0)  # Default to 1.0 if not found

    # Perform the computation (assuming you have other code here)
    # For example:
    seismic_load = (importance_factor * spectral_response_acceleration * amplification_factor)

    return seismic_load


def get_path(event):
    dropped_file = event.data.replace("{","").replace("}", "")
    return (str(dropped_file))
    # do further operation

def change():
    global mode
    if mode == "dark":
        ctk.set_appearance_mode("light")
        mode = "light"
        # Clear text box if needed
    else:
        ctk.set_appearance_mode("dark")
        mode = "dark"
        # Clear text box if needed

def main():
    from gui import on_drop
    ctk.set_appearance_mode("system")  # Default to light mode
    entry_width = 200
    
    # Create a TkinterDnD.Tk root window
    root = CTk()
    
    # Create a CTkScrollableFrame
    scrollable_frame = ctk.CTkScrollableFrame(root)
    scrollable_frame.pack(expand=True, fill='both')

    # Add a nested frame inside the scrollable frame to hold the widgets
    content_frame = ctk.CTkFrame(scrollable_frame)
    content_frame.pack(expand=True, fill='both')
    # Create and place the appearance mode toggle button
    
    image = ctk.CTkImage(light_image=Image.open("drag.png"),
                         dark_image=Image.open("drag.png"), size=(100, 100))
    dark_light_image = ctk.CTkImage(light_image=Image.open("dark-light.png"),
                                    dark_image=Image.open("dark-light.png"), size=(30, 30))
    my_button = ctk.CTkButton(content_frame, text='Change Mode', command=change, font=("Arial", 16, "bold"), fg_color='#4C7766', hover_color='#4C7766', image=dark_light_image, compound='left')
    my_button.grid(row=0, column=10, pady=(0, 0), padx=(150, 0))  # Adjusted to be visible
    # integer_values = list((range(0, 11)))
    site_class_label = ctk.CTkLabel(content_frame, text="Site Class", fg_color='transparent', font=("Arial", 16, "bold"))
    site_class_label.grid(row=1, column=0, pady=10, padx=(100, 0),sticky='w')
    site_class_entry = ctk.CTkComboBox(content_frame, values=[str(i) for i in range(0, 11)], width=entry_width)
    site_class_entry.grid(row=1, column=1)
    
    importance_factor_label = ctk.CTkLabel(content_frame, text="Importance Factor", fg_color='transparent', font=("Arial", 16, "bold"))
    importance_factor_label.grid(row=2, column=0, pady=10, padx=(100, 0),sticky='w')
    importance_factor_entry = ctk.CTkEntry(content_frame, placeholder_text="Enter Importance Factor", width=entry_width)
    importance_factor_entry.grid(row=2, column=1)
    importance_factor_entry.insert(1, "1")
    spectral_response_acceleration_label = ctk.CTkLabel(content_frame, text="Spectral Response Acceleration", fg_color='transparent', font=("Arial", 16, "bold"))
    spectral_response_acceleration_label.grid(row=3, column=0, pady=10, padx=(100, 0),sticky='w')
    spectral_response_acceleration_entry = ctk.CTkEntry(content_frame, placeholder_text="Enter Spectral Response Acceleration", width=entry_width)
    spectral_response_acceleration_entry.grid(row=3, column=1, pady=10)

    # calculate_button = ctk.CTkButton(content_frame, height=40, width=200, font=("Arial", 16, "bold"), fg_color='#4C7766', hover_color='#4C7766', text="Calculate Seismic Load", 
    #                                  command=lambda: calculate_seismic_load(site_class_entry, 
    #                                                                         importance_factor_entry, 
    #                                                                         spectral_response_acceleration_entry))
    # calculate_button.grid(row=3, columnspan=5, pady=30, padx=(3100, 0))
    root.title("IFC to PDF Converter")
    root.geometry("900x900")
    root.resizable(False, False)
    
    
    label = ctk.CTkLabel(content_frame, text='\n\n\n\n\n\nDrag and Drop an IFC File Here ...', corner_radius=10, font=("Arial", 16, "bold"), image=image,text_color='gray')
    label.grid(row=12, columnspan=2, pady=(10, 20), padx=(100, 0))

    ctk.CTkLabel(content_frame, text="Snow Load (lbs/sq. ft.):", font=("Arial", 16, "bold")).grid(row=5, column=0, sticky='w', pady=10, padx=(100, 0))
    snow_load_entry = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Enter Snow load")
    snow_load_entry.grid(row=5, column=1, sticky='w')

    ctk.CTkLabel(content_frame, text="Ice Load (lbs/sq. ft.):", font=("Arial", 16, "bold")).grid(row=6, column=0, sticky='w', pady=10, padx=(100, 0))
    ice_load_entry = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Enter ICE Load")
    ice_load_entry.grid(row=6, column=1, sticky='w')

    remove_zero_point_var = tk.BooleanVar(value=False)
    checkbox = ctk.CTkCheckBox(content_frame, text="Remove (0,0,0) Point", variable=remove_zero_point_var, font=("Arial", 16, "bold"), fg_color='#4C7766', hover_color='#4C7766', )
    checkbox.grid(row=0, column=0, sticky='w', pady=(100,0), padx=(100, 0))

    # ctk.CTkLabel(content_frame, text="Roof Uplift Pressure (psf)", font=("Arial", 16, "bold")).grid(row=8, column=0, sticky='w', pady=10, padx=(100, 0))
    # roof_uplift_entry = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Enter Roof Uplift")
    # roof_uplift_entry.grid(row=8, column=1, sticky='w')

    # ctk.CTkLabel(content_frame, text="Roof Downpressure (psf)", font=("Arial", 16, "bold")).grid(row=9, column=0, sticky='w', pady=10, padx=(100, 0))
    # roof_downpressure_entry = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Enter Roof Down Pressure")
    # roof_downpressure_entry.grid(row=9, column=1, sticky='w')

    ctk.CTkLabel(content_frame, text="Wind Force (lbs)", font=("Arial", 16, "bold")).grid(row=10, column=0, sticky='w', pady=10, padx=(100, 0))
    wind_force_entry = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Enter Wind force")
    wind_force_entry.grid(row=10, column=1, sticky='w')

    # ctk.CTkLabel(content_frame, text="Wall Height (feet)", font=("Arial", 16, "bold")).grid(row=11, column=0, sticky='w', pady=10, padx=(100, 0))
    # wall_height_entry = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Enter Wall Height")
    # wall_height_entry.grid(row=11, column=1, sticky='w')

    

    root.drop_target_register(DND_ALL)

    # Fetch the latest values during the drop event
    def fetch_values():
        return {
            "snow_load_entry": snow_load_entry.get().strip(),
            "ice_load_entry": ice_load_entry.get().strip(),
            # "roof_uplift_entry": roof_uplift_entry.get().strip(),
            # "roof_downpressure_entry": roof_downpressure_entry.get().strip(),
            "wind_force_entry": wind_force_entry.get().strip(),
            # "wall_height_entry": wall_height_entry.get().strip(),
            "remove_zero_point_var": remove_zero_point_var,
            "site_class_entry": site_class_entry.get().strip(),
            "importance_factor_entry": importance_factor_entry.get().strip(),
            "spectral_response_acceleration_entry": spectral_response_acceleration_entry.get().strip(),
        }

    # Bind the drop event to the on_drop function and pass the values fetched during the event
    root.dnd_bind('<<Drop>>', lambda event: on_drop(event, fetch_values()))

    root.mainloop()
if __name__ == '__main__':
    main()