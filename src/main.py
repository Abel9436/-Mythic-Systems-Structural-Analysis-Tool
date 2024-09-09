import os
import customtkinter as ctk
import tkinter  as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinterdnd2 import TkinterDnD, DND_ALL

from Seismicwidget import create_seismic_input_widgets
from PIL import Image
from tkinter import BooleanVar
import entry_info

mode = "dark"
class CTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
class CircularProgressBar(ctk.CTkFrame):
    def __init__(self, parent, size=100, thickness=10, speed=10, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.size = size
        self.thickness = thickness
        self.speed = speed
        self.angle = 0

        # Create a Canvas to draw the circular arc
        self.canvas = tk.Canvas(self, width=self.size, height=self.size, highlightthickness=0, bg="gray")
        self.canvas.pack(expand=True, fill="both")

        # Create the arc for the spinner
        self.arc = self.canvas.create_arc(
            self.thickness, self.thickness, self.size - self.thickness, self.size - self.thickness,
            start=0, extent=150, style="arc", outline="#4C7766", width=self.thickness
        )

        # Start the animation
        self.animate()
        
    def animate(self):
        
        # Increment the angle and rotate the arc
        self.angle = (self.angle + self.speed) % 360
        self.canvas.itemconfig(self.arc, start=self.angle)
        # Continue the animation
        self.after(50, self.animate)

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

file_path=''
text='\n\n\n\n\n\nDrag and Drop an IFC File Here ...'

def get_path(event,label):
    global file_path
    global text

    dropped_file = event.data.replace("{","").replace("}", "")
    print (str(dropped_file))
    file_path=dropped_file
    file_name = os.path.basename(dropped_file)
    label.configure(text="\n\n\n\n\n\nDroped File : "+file_name,text_color='#4C7766')
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

def on_submit(entries,submit_button):
    # Collect all the values
    values = {
        "snow_load_entry": entries["snow_load_entry"].get().strip(),
        "ice_load_entry": entries["ice_load_entry"].get().strip(),
        "wind_speed_entry": entries["wind_speed_entry"].get().strip(),
        "remove_zero_point_var": entries["remove_zero_point_var"].get(),
        "site_class_entry": entries["site_class_entry"].get().strip(),
        "importance_factor_entry": entries["importance_factor_entry"].get().strip(),
        "spectral_response_acceleration_entry": entries["spectral_response_acceleration_entry"].get().strip(),
    }
    from CTkMessagebox import CTkMessagebox
    if values:
        CTkMessagebox(title="Entries Submissions",message='Entries Submitted Successfully')
        submit_button.configure(state=ctk.DISABLED)
    # Process or print the collected values
      # Replace this with actual processing code

def on_calculate(entries,root):
    # Collect all the values from entry widgets
    from gui import on_drop
    values = {
        "snow_load_entry": entries["snow_load_entry"].get().strip(),
        "ice_load_entry": entries["ice_load_entry"].get().strip(),
        "wind_speed_entry": entries["wind_speed_entry"].get().strip(),
        "remove_zero_point_var": entries["remove_zero_point_var"].get(),
        "site_class_entry": entries["site_class_entry"].get().strip(),
        "importance_factor_entry": entries["importance_factor_entry"].get().strip(),
        "spectral_response_acceleration_entry": entries["spectral_response_acceleration_entry"].get().strip(),
    }
    progress_bar = CircularProgressBar(root, size=150, thickness=15, speed=10)
    progress_bar.grid(row=5, column=1, columnspan=1, pady=0)
    # progress_bar.pack()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(17, weight=1)

    on_drop(file_path,values)
    # Perform calculations based on the collected values
    # Replace this with your actual calculation logic
    result = f"Calculated values based on: {values}"
    print(result)  # Or display it in a label or messagebox

def handle_click_info(entry):
    from CTkMessagebox import CTkMessagebox
    
    CTkMessagebox(title=entry,message=entry_info.entry_info[entry])
def main():
    
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
                                    
                                    dark_image=Image.open("dark-light.png"), size=(25, 25))
    
    my_button = ctk.CTkButton(content_frame, text='Change Mode', command=change, font=("Arial", 16, "bold"), fg_color='#4C7766', hover_color='#4C7766', image=dark_light_image, compound='left')
    my_button.grid(row=0, column=10, pady=(10,0), padx=(100, 0))  # Adjusted to be visible
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
    
    
    label = ctk.CTkLabel(content_frame, text=text, corner_radius=10, font=("Arial", 16, "bold"), image=image,text_color='gray')
    label.grid(row=12, columnspan=2, pady=(10, 20), padx=(100, 0))
    
    ctk.CTkLabel(content_frame, text="Snow Load (lbs/sq. ft.):", font=("Arial", 16, "bold")).grid(row=4, column=0, sticky='w', pady=10, padx=(100, 0))
    snow_load_entry = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Enter Snow load")
    snow_load_entry.grid(row=4, column=1, sticky='w')

    ctk.CTkLabel(content_frame, text="Ice Load (lbs/sq. ft.):", font=("Arial", 16, "bold")).grid(row=5, column=0, sticky='w', pady=10, padx=(100, 0))
    ice_load_entry = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Enter ICE Load")
    ice_load_entry.grid(row=5, column=1, sticky='w')

    remove_zero_point_var =BooleanVar(value=False)
    checkbox = ctk.CTkCheckBox(content_frame, text="Remove (0,0,0) Point", variable=remove_zero_point_var, font=("Arial", 16, "bold"), fg_color='#4C7766', hover_color='#4C7766', )
    checkbox.grid(row=0, column=0, sticky='w', pady=(100,0), padx=(100, 0))

    # ctk.CTkLabel(content_frame, text="Roof Uplift Pressure (psf)", font=("Arial", 16, "bold")).grid(row=8, column=0, sticky='w', pady=10, padx=(100, 0))
    # roof_uplift_entry = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Enter Roof Uplift")
    # roof_uplift_entry.grid(row=8, column=1, sticky='w')

    # ctk.CTkLabel(content_frame, text="Roof Downpressure (psf)", font=("Arial", 16, "bold")).grid(row=9, column=0, sticky='w', pady=10, padx=(100, 0))
    # roof_downpressure_entry = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Enter Roof Down Pressure")
    # roof_downpressure_entry.grid(row=9, column=1, sticky='w')

    ctk.CTkLabel(content_frame, text="Wind Force (lbs)", font=("Arial", 16, "bold")).grid(row=6, column=0, sticky='w', pady=10, padx=(100, 0))
    wind_force_entry = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Enter Wind force")
    wind_force_entry.grid(row=6, column=1, sticky='w')

    # ctk.CTkLabel(content_frame, text="Wall Height (feet)", font=("Arial", 16, "bold")).grid(row=11, column=0, sticky='w', pady=10, padx=(100, 0))
    # wall_height_entry = ctk.CTkEntry(content_frame, width=entry_width, placeholder_text="Enter Wall Height")
    # wall_height_entry.grid(row=11, column=1, sticky='w')

    entries={
            "snow_load_entry": snow_load_entry,
            "ice_load_entry": ice_load_entry,
            # "roof_uplift_entry": roof_uplift_entry,
            # "roof_downpressure_entry": roof_downpressure_entry,
            "wind_speed_entry": wind_force_entry,
            # "wall_height_entry": wall_height_entry,
            "remove_zero_point_var": remove_zero_point_var,
            "site_class_entry": site_class_entry,
            "importance_factor_entry": importance_factor_entry,
            "spectral_response_acceleration_entry": spectral_response_acceleration_entry,
        }
    submit_button = ctk.CTkButton(content_frame, text="Submit", font=("Arial", 16, "bold"), fg_color='#4C7766', hover_color='#4C7766',
                                  command=lambda: on_submit(entries,submit_button))
    submit_button.grid(row=16, column=0, pady=20, padx=(100, 0), sticky='w')

    calculate_button = ctk.CTkButton(content_frame, text="Calculate", font=("Arial", 16, "bold"),fg_color='#4C7766', hover_color='#4C7766',
                                     command=lambda: on_calculate(entries,content_frame))
    calculate_button.grid(row=16, column=1, pady=20, padx=(0, 0), sticky='w')
    # info Buttons
    info_image = ctk.CTkImage(light_image=Image.open("info.png"),
                                    
                                    dark_image=Image.open("info.png"), size=(25, 25))
    info_button1 = ctk.CTkButton(content_frame, image=info_image, text="", width=10, height=1,bg_color="transparent",fg_color="transparent",command=lambda:handle_click_info('remove_point'))
    info_button1.grid(row=0, column=3, pady=(100, 0), padx=(0, 0))
    info_button2 = ctk.CTkButton(content_frame, image=info_image, text="", width=10, height=1,bg_color="transparent",fg_color="transparent",command=lambda:handle_click_info('site_class'))
    info_button2.grid(row=1, column=3, pady=(0, 0), padx=(0, 0))

    info_button3 = ctk.CTkButton(content_frame, image=info_image, text="", width=10, height=1,bg_color="transparent",fg_color="transparent",command=lambda:handle_click_info('importance_factor'))
    info_button3.grid(row=2, column=3, pady=(0, 0), padx=(0, 0))
    info_button4 = ctk.CTkButton(content_frame, image=info_image, text="", width=10, height=1,bg_color="transparent",fg_color="transparent",command=lambda:handle_click_info('spectral_response'))
    info_button4.grid(row=3, column=3, pady=(0, 0), padx=(0, 0))
    info_button5 = ctk.CTkButton(content_frame, image=info_image, text="", width=10, height=1,bg_color="transparent",fg_color="transparent",command=lambda:handle_click_info('snow_load'))
    info_button5.grid(row=4, column=3, pady=(0, 0), padx=(0, 0))
    info_button6 = ctk.CTkButton(content_frame, image=info_image, text="", width=10, height=1,bg_color="transparent",fg_color="transparent",command=lambda:handle_click_info('ice_load'))
    info_button6.grid(row=5, column=3, pady=(0, 0), padx=(0, 0))
    info_button7 = ctk.CTkButton(content_frame, image=info_image, text="", width=10, height=1,bg_color="transparent",fg_color="transparent",command=lambda:handle_click_info('wind_force'))
    info_button7.grid(row=6, column=3, pady=(0, 0), padx=(0, 0))

    ###############
    root.drop_target_register(DND_ALL)

    # Fetch the latest values during the drop event
    def fetch_values():
        return entries
    # Bind the drop event to the on_drop function and pass the values fetched during the event
    root.dnd_bind('<<Drop>>', lambda event: get_path(event,label))

    root.mainloop()
if __name__ == '__main__':
    main()