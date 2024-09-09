'''

**LICENSE**

Include a proper license file according to Mythic Systems' guidelines.

**Documentation Files**

Update any existing documentation files to include Mythic Systems' branding.

### 2. Add Branding to Code

Include a header with Mythic Systems branding in each Python file:

```python
# Mythic Systems Structural Analysis Tool
# (c) 2024 Mythic Systems
# All rights reserved.
'''
import matplotlib
#from main import *

# from calculate import calculate_area_from_coords
matplotlib.use('Agg')  # Use a non-interactive backend


from read_methods import *
from report import *
from widget import *
# import tkinterDnD
# import ifcopenshell
# import re
# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np
# from scipy.spatial import Delaunay, ConvexHull
# from tkinter import Tk, messagebox, Label, Checkbutton, BooleanVar, Entry
# from tkinterdnd2 import TkinterDnD, DND_FILES
import os
# from fpdf import FPDF
# import tkinter as tk
# from tkinter import simpledialog
from CTkMessagebox import CTkMessagebox
import traceback
import logging

error_msg=''
logging.basicConfig(filename='error.log', level=logging.ERROR)
def on_drop(event, values):
    try:
        print("Drop event triggered!")
        
        # Print the event data
        print(f"Event data: {event}")
        
        ifc_file_path = event.strip('{}')  # Remove curly braces if present
        print(f"Processed file path: {ifc_file_path}")
        # print(event, type(event))
        # for d in dir(event):
        #     try:
        #         print(">>> 1. ", d, eval(f'event.{d}()'))
        #     except Exception as e:
        #         print(">>> 2. ", d, eval(f'event.{d}'))
        # print(dir(values['snow_load_entry']))
        print(values)
        for k, v in values.items():
            try:
                print(k, v)
            except:
                pass

        # Entry widgets
        roof_uplift_entry = values["roof_uplift_entry"]
        
        roof_downpressure_entry = values["roof_downpressure_entry"]
        wind_force_entry = values["wind_force_entry"]
        wall_height_entry = values["wall_height_entry"]
        snow_load_entry = values["snow_load_entry"]
        ice_load_entry = values["ice_load_entry"]
        print('going')
        zero_check = values["remove_zero_point_var"]
        site_class_entry = values["site_class_entry"]
        importance_factor_entry = values["importance_factor_entry"]
        spectral_response_acceleration_entry = values["spectral_response_acceleration_entry"]
        
        
        # Assume parse_ifc_file, extract methods, calculate methods are correctly implemented
        from read_methods import parse_ifc_file, extract_element_counts, extract_section_types, extract_floor_data, extract_forces_moments
        from calculate import calculate_perimeter, calculate_roof_perimeter, calculate_area_from_coords, calculate_snow_load, calculate_ice_load, calculate_wind_loads, calculate_dead_load, calculate_beam_column_weight
        from report import create_Aux_pdf, plot_coordinates
        from widget import live_load_widget
        from Seismicwidget import compute_seismic_load
        
        
        ifc_file_path = event.data.strip('{}')  # Remove curly braces if present
        coordinates = parse_ifc_file(ifc_file_path, zero_val=zero_check)
        areas = calculate_area_from_coords(coordinates)

        output_path = os.path.splitext(ifc_file_path)[0] + "_coordinate_plots.pdf"
        floor_count = extract_floor_data(ifc_file_path)
        forces, moments = extract_forces_moments(ifc_file_path)
        perimeter = calculate_perimeter(coordinates)
        roof_perimeter = calculate_roof_perimeter(coordinates)

        # Call the live_load_widget function to get live load inputs
        live_loads = live_load_widget(floor_count)
        print("Live Loads: ", live_loads)
        print('ready to plot')
        try:

            plot_coordinates(coordinates, areas, output_path, ifc_file_path)
            print("plotted successffully")
        except:

            print("can't plot the coordinates")
        print(f"Output saved to: {output_path}")

        Aux_output_path = os.path.splitext(ifc_file_path)[0] + "_Aux.pdf"

        # Validate and convert inputs safely
        try:
            roof_uplift = float(roof_uplift_entry or "0")
            print('daaaaaa',roof_uplift)
            roof_downpressure = float(roof_downpressure_entry or "0")
            wind_force = float(wind_force_entry or "0")
            wall_height = float(wall_height_entry or "0")
            snow_load_per_unit_area = float(snow_load_entry or "0")
            ice_load_per_unit_area = float(ice_load_entry or "0")

            # Calculate total snow and ice loads
            roof_area = areas[0]  # Assuming the XY area is the roof area
            total_snow_load = calculate_snow_load(roof_area, snow_load_per_unit_area)
            ice_load_total = calculate_ice_load(roof_area, ice_load_per_unit_area)
            seismic_load = compute_seismic_load (float(site_class_entry or "0"),float (importance_factor_entry or "0"), float (spectral_response_acceleration_entry or "0"))
            # Extract element counts
            element_counts = extract_element_counts(ifc_file_path)

            # Calculate wind loads
            wind_loads = calculate_wind_loads(ifc_file_path)

            # Calculate dead load
            dead_load = calculate_dead_load(ifc_file_path)

            # Calculate beam and column weights
            total_beam_weight, total_column_weight = calculate_beam_column_weight(ifc_file_path)
            print(total_beam_weight)
            
            # Create Auxiliary PDF
            print("ready to aux")
            create_Aux_pdf(
                element_counts, Aux_output_path, ifc_file_path, floor_count, forces, moments, perimeter,
                roof_uplift, roof_downpressure, wind_force, wall_height, roof_perimeter, areas,
                wind_loads, dead_load, total_column_weight, total_beam_weight, total_snow_load, ice_load_total, live_loads,
                seismic_load
            )
            print('plot finished')
            # Message about the number of stories
            multi_story_msg = "The building is a single story."
            if floor_count > 1:
                multi_story_msg = f"The building has {floor_count} stories."

            # messagebox.showinfo("Info", f"Plot saved to {output_path}\nAuxiliary data saved to {Aux_output_path}\n{multi_story_msg}")
            # CTkMessagebox(title="Info", message=f"Plot saved to {output_path}\nAuxiliary data saved to {total_beam_weight}\n{total_beam_weight}")
            CTkMessagebox(title="Info", message=f"Plot saved to {output_path}\nAuxiliary data saved to {Aux_output_path}\n{multi_story_msg}")

        except ValueError as e:
            # messagebox.showerror("Input Error", f"Please enter valid numbers: {e}")
            CTkMessagebox(title="Error", message=f"Please enter valid numbers: {e}")
    except Exception as e:
        print(f"Error in on_drop function: {e}")
        error_msg=traceback.format_exc()
        logging.error(error_msg)
        # messagebox.showerror("Error", f"An error occurred: {e}")
        CTkMessagebox(title="Error", message=f"An error occurred: {e}", icon="cancel")