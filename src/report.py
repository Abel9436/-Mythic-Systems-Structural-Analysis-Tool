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
#from main import *
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

#from gui import *


#from read import extract_ifc_data
# import ifcopenshell
# import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
# from scipy.spatial import Delaunay, ConvexHull
# from tkinter import Tk, messagebox, Label, Checkbutton, BooleanVar, Entry
# from tkinterdnd2 import TkinterDnD, DND_FILES
# import os
from fpdf import FPDF
# import tkinter as tk
# from tkinter import simpledialog

def plot_coordinates(coordinates, areas, output_path, ifc_file_path):
    from read_methods import extract_ifc_data
    from calculate import calculate_perimeter,calculate_footing_perimeter
    if not all(len(coord) == 3 for coord in coordinates):
        raise ValueError("Some coordinates do not have exactly three values.")

    x_vals = [coord[0] for coord in coordinates]
    y_vals = [coord[1] for coord in coordinates]
    z_vals = [coord[2] for coord in coordinates]

    # Determine max height for plot uniformity
    fac = 0.30 * max(max(z_vals), max(x_vals), max(y_vals))
    max_height = max(z_vals)
    max_width = max(y_vals)
    max_length = max(x_vals)

    max_hw = max(max_height, max_width) + fac
    min_hw = min(min(y_vals), min(z_vals)) - fac

    max_lw = max(max_length, max_width) + fac
    min_lw = min(min(y_vals), min(x_vals)) - fac

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 14), constrained_layout=True)
    axes = axes.flatten()  # Flatten the 2x2 grid to 1D for easier indexing

    sns.set(style="whitegrid")
    
    # Font settings
    title_fontsize = 14
    label_fontsize = 12
    tick_fontsize = 10

    # XZ Plane
    axes[0].plot(x_vals, z_vals, color='royalblue', linewidth=1)
    axes[0].set_title('XZ Plane (Feet)', fontsize=title_fontsize)
    axes[0].set_xlabel('X (feet)', fontsize=label_fontsize)
    axes[0].set_ylabel('Z (feet)', fontsize=label_fontsize)
    axes[0].axis('equal')
    axes[0].set_xlim([min_lw, max_lw])
    axes[0].set_ylim([min_hw, max_hw])
    axes[0].tick_params(axis='both', which='major', labelsize=tick_fontsize)

        # YZ Plane
    axes[1].plot(y_vals, z_vals, color='royalblue', linewidth=1)
    axes[1].set_title('YZ Plane (Feet)', fontsize=title_fontsize)
    axes[1].set_xlabel('Y (feet)', fontsize=label_fontsize)
    axes[1].set_ylabel('Z (feet)', fontsize=label_fontsize)
    axes[1].axis('equal')
    axes[1].set_xlim([min_lw, max_lw])
    axes[1].set_ylim([min_hw, max_hw])
    axes[1].tick_params(axis='both', which='major', labelsize=tick_fontsize)

    # XY Plane
    axes[2].plot(x_vals, y_vals, color='royalblue', linewidth=1)
    axes[2].set_title('XY Plane (Feet)', fontsize=title_fontsize)
    axes[2].set_xlabel('X (feet)', fontsize=label_fontsize)
    axes[2].set_ylabel('Y (feet)', fontsize=label_fontsize)
    axes[2].axis('equal')
    axes[2].set_xlim([min_lw, max_lw])
    axes[2].set_ylim([min_hw, max_hw])
    axes[2].tick_params(axis='both', which='major', labelsize=tick_fontsize)

    ww = extract_ifc_data(ifc_file_path)
    perimeter = calculate_perimeter(coordinates)
    footing_perimeter_coords = calculate_footing_perimeter(coordinates)

    # Plot Footing Perimeter

    footing_perimeter_coords = calculate_footing_perimeter(coordinates)

    if footing_perimeter_coords:
        x_vals_fp = [point[0] for point in footing_perimeter_coords] + [footing_perimeter_coords[0][0]]
        y_vals_fp = [point[1] for point in footing_perimeter_coords] + [footing_perimeter_coords[0][1]]
        #axes[2].plot(x_vals_fp, y_vals_fp, color='red', linewidth=1)

    # Aux Info
    axes[3].axis('off')
    axes[3].text(0.1, 0.9, f'XZ Area: {areas[2]} sq. feet', horizontalalignment='left', verticalalignment='center', fontsize=label_fontsize)
    axes[3].text(0.1, 0.8, f'YZ Area: {areas[1]} sq. feet', horizontalalignment='left', verticalalignment='center', fontsize=label_fontsize)
    axes[3].text(0.1, 0.7, f'XY Area: {areas[0]} sq. feet', horizontalalignment='left', verticalalignment='center', fontsize=label_fontsize)
    axes[3].text(0.1, 0.6, f'CFS Weight: {ww} lbs.', horizontalalignment='left', verticalalignment='center', fontsize=label_fontsize)
    axes[3].text(0.1, 0.5, f'Footing Perimeter: {perimeter} feet', horizontalalignment='left', verticalalignment='center', fontsize=label_fontsize)

    plt.savefig(output_path)
    # plt.show()

def create_Aux_pdf(element_counts, output_path, ifc_path, floor_count, forces, moments, perimeter, roof_uplift, roof_downpressure, wind_force, wall_height, roof_perimeter, areas, wind_loads, dead_load, total_column_weight, total_beam_weight, total_snow_load, total_ice_load, live_loads, seismic_load):
    from calculate import calculate_linear_load, calculate_wall_moments
    pdf = FPDF()
    multi_story_msg = "The building is a single story."
    if floor_count > 1:
        multi_story_msg = f"The building has {floor_count} stories."

    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Auxiliary Data", ln=True, align='C')

    for element_type, count in element_counts.items():
        pdf.cell(200, 10, txt=f'{element_type} Count: {count}', ln=True)

    pdf.cell(200, 10, txt=multi_story_msg, ln=True)
    pdf.cell(200, 10, txt=f'Total Beam Weight: {total_beam_weight} lbs', ln=True)
    pdf.cell(200, 10, txt=f'Total Column Weight: {total_column_weight} lbs', ln=True)

    for floor in forces:
        total_force = np.sum(forces[floor])
        total_moment = np.sum(moments[floor])
        pdf.cell(200, 10, txt=f'{floor} - Total Force: {total_force} N, Total Moment: {total_moment} Nm', ln=True)

    linear_load = calculate_linear_load(perimeter, roof_uplift, roof_downpressure)
    wall_moment = calculate_wall_moments(wind_force, wall_height)
    
    wind_pressure = wind_loads['Wind Pressure']

    pdf.cell(200, 10, txt=f'Estimated Linear Load on Perimeter: {linear_load} lbs/ft', ln=True)
    pdf.cell(200, 10, txt=f'Wall Moment from Wind: {wall_moment} Nm', ln=True)
    pdf.cell(200, 10, txt=f'Wind Pressure on Roof: {wind_pressure} lbs/ft²', ln=True)

    pdf.cell(200, 10, txt=f'Roof Perimeter: {roof_perimeter} feet', ln=True)
    pdf.cell(200, 10, txt=f'XZ Area: {areas[2]} sq. feet', ln=True)
    pdf.cell(200, 10, txt=f'YZ Area: {areas[1]} sq. feet', ln=True)
    pdf.cell(200, 10, txt=f'XY Area: {areas[0]} sq. feet', ln=True)

    pdf.cell(200, 10, txt="Wind Load Calculation Results:", ln=True)
    pdf.cell(200, 10, txt=f"Wind Pressure: {wind_loads['Wind Pressure']} lbs/ft", ln=True)
    pdf.cell(200, 10, txt=f"Wall Moment: {wind_loads['Wall Moment']} ft-lbs", ln=True)

    pdf.cell(200, 10, txt="Dead Load Calculation Results:", ln=True)
    pdf.cell(200, 10, txt=f"Total Dead Load: {dead_load} lbs", ln=True)

    pdf.cell(200, 10, txt="Snow Load Calculation Results:", ln=True)
    pdf.cell(200, 10, txt=f"Total Snow Load: {total_snow_load} lbs", ln=True)

    pdf.cell(200, 10, txt="Ice Load Calculation Results:", ln=True)
    pdf.cell(200, 10, txt=f"Total Ice Load: {total_ice_load} lbs", ln=True)
    
    pdf.cell(200, 10, txt="Live Loads:", ln=True)
    for load_info in live_loads:
        pdf.cell(200, 10, txt=f"Floor {load_info['floor']} - Percentage Load: {load_info['percentage_load']}%, Area Load: {load_info['area_load']} sq. feet", ln=True)

    pdf.output(output_path)
