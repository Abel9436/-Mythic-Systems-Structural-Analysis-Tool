import customtkinter as ctk

# import tkinterDnD
# from tkinterdnd2 import TkinterDnD, DND_FILES
# from Seismicwidget import create_seismic_input_widgets
# from PIL import Image
mode = "dark"

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
results = []
def live_load_widget(floor_count):
    live_loads = []

    # Create the main window
    root = ctk.CTk()
    root.title("Live Load Input")
    root.geometry("800x800")
    root.resizable(False, False)
    ctk.set_appearance_mode("system") 
    # Create a scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(master=root, width=480, height=480)
    scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)
    # dark_light_image = ctk.CTkImage(light_image=Image.open("dark-light.png"),
    #                     dark_image=Image.open("dark-light.png"), size=(30, 30))
    # Add headers for the columns
    header_percentage = ctk.CTkLabel(scrollable_frame, text="Live Load Percentage",font=("Arial", 16, "bold"),)
    header_percentage.grid(row=0, column=0, pady=50, padx=(20,0), sticky='w')

    header_area = ctk.CTkLabel(scrollable_frame, text="Live Load Area (sq. ft.)",font=("Arial", 16, "bold"))
    header_area.grid(row=0, column=1, pady=10, padx=(20,0), sticky='w')

    # Loop through each floor and create input fields
    for floor in range(1, floor_count + 1):
        load_info = {}
        load_info['floor'] = floor

        # Add a label and entry for percentage load
        percentage_label = ctk.CTkLabel(scrollable_frame, text=f"Floor {floor}:",font=("Arial", 12, "bold"))
        percentage_label.grid(row=floor, column=0, pady=5, padx=10, sticky='e',)

        percentage_entry = ctk.CTkEntry(scrollable_frame, placeholder_text="Enter %",font=("Arial", 12, "bold"))
        percentage_entry.grid(row=floor, column=1, pady=5, padx=10, sticky='w',columnspan=1)
        load_info['percentage_load'] = percentage_entry

        # Add a label and entry for area load
        area_entry = ctk.CTkEntry(scrollable_frame, placeholder_text="Enter sq. ft.",font=("Arial", 12, "bold"))
        area_entry.grid(row=floor, column=2, pady=5, padx=20, sticky='w',columnspan=2)
        load_info['area_load'] = area_entry
        
        percentage3 = load_info['percentage_load'].get()
        print(percentage3)
        live_loads.append(load_info)
    

    # Add a button to submit the inputs
    submit_button = ctk.CTkButton(scrollable_frame, text="Submit", command=lambda: on_submit(live_loads, root),font=("Arial", 16, "bold"),fg_color='#4C7766',hover_color='#4C7766',)
    submit_button.grid(row=floor_count + 1, columnspan=2, pady=20)
    my_button = ctk.CTkButton(scrollable_frame, text='Change Mode', command=change, font=("Arial", 16, "bold"), fg_color='#4C7766', hover_color='#4C7766', compound='left')
    my_button.grid(row=12, columnspan=1, pady=(50, 0), padx=(0, 0))
    root.mainloop()
    return results
    

def on_submit(live_loads, root):
    # Retrieve the input values and close the window
    
    for load_info in live_loads:
        percentage = load_info['percentage_load'].get()
        area = load_info['area_load'].get()
        results.append({
            "floor": load_info['floor'],
            "percentage_load": percentage,
            "area_load": area
        })
    root.destroy()
    print(results) 
    return results # You can process the results here
    
    


# a=live_load_widget(2)
# print(a)