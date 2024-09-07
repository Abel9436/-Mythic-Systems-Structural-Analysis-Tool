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
from read_methods import *
from report import *
from widget import *
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

import ifcopenshell
import re
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np
from scipy.spatial import Delaunay, ConvexHull
from tkinter import Tk, messagebox, Label, Checkbutton, BooleanVar, Entry
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
from fpdf import FPDF
import tkinter as tk
from tkinter import simpledialog

def calculate_dead_load_with_live_load(ifc_file, live_loads, roof_area, snow_load_per_unit_area, ice_load_per_unit_area):
    print(str(ifc_file))
    model = ifcopenshell.open(ifc_file)

    total_dead_load = 0.0
    total_live_load = 0.0

    for element in model.by_type('IfcElementQuantity'):
        for quantity in element.Quantities:
            if quantity.is_a('IfcQuantityWeight'):
                if 'Dead Load' in quantity.Name or 'DeadLoad' in quantity.Name or 'Gross Weight' in quantity.Name or 'GrossWeight' in quantity.Name:
                    total_dead_load += quantity.WeightValue

    for load in live_loads:
        area_load = load['area_load']
        if area_load:
            total_live_load += area_load * load['percentage_load'] / 100

    # Calculate snow load
    total_snow_load = calculate_snow_load(roof_area, snow_load_per_unit_area)

    # Calculate ice load
    total_ice_load = calculate_ice_load(roof_area, ice_load_per_unit_area)

    return total_dead_load, total_live_load, total_snow_load, total_ice_load

def calculate_beam_column_weight(ifc_path):

    """Calculate the total weight of beams and columns using 'Gross Weight' or 'IFCQUANTITYLENGTH'."""
    
    total_beam_weight = 0.0
    total_column_weight = 0.0

    ifc_file = ifcopenshell.open(ifc_path)

        # Helper function to get weight value
    def get_weight_value(element, attribute_names):
        for attr_name in attribute_names:
            attr_value = getattr(element, attr_name, None)
            if attr_value:
                return attr_value
        return 0.0

        # Define attribute names to check for weight values
    weight_attributes = ['GrossWeight', 'WeightValue']

        # Iterate over beams
    for beam in ifc_file.by_type('IfcBeam'):
        for quantity in beam.IsDefinedBy:
            if quantity.is_a('IfcRelDefinesByProperties'):
                prop_set = quantity.RelatingPropertyDefinition
                if prop_set.is_a('IfcElementQuantity'):
                    for quantity in prop_set.Quantities:
                        if quantity.is_a('IfcQuantityWeight') or quantity.Name == 'Gross Weight':
                            total_beam_weight += get_weight_value(quantity, weight_attributes)

        # Iterate over columns
    for column in ifc_file.by_type('IfcColumn'):
        for quantity in column.IsDefinedBy:
            if quantity.is_a('IfcRelDefinesByProperties'):
                prop_set = quantity.RelatingPropertyDefinition
                if prop_set.is_a('IfcElementQuantity'):
                    for quantity in prop_set.Quantities:
                        if quantity.is_a('IfcQuantityWeight') or quantity.Name == 'Gross Weight':
                            total_column_weight += get_weight_value(quantity, weight_attributes)

        return round(total_beam_weight, 2), round(total_column_weight, 2)
    


def calculate_area_from_coords(coord_list):
    coords = np.array(coord_list)

    def triangulation_area(points):
        if len(points) < 3:
            return 0.0
        tri = Delaunay(points)
        area = 0.0
        for simplex in tri.simplices:
            pts = points[simplex]
            a = np.linalg.norm(pts[0] - pts[1])
            b = np.linalg.norm(pts[1] - pts[2])
            c = np.linalg.norm(pts[2] - pts[0])
            s = (a + b + c) / 2
            area += np.sqrt(s * (s - a) * (s - b) * (s - c))
        return round(area, 1)

    area_xy = triangulation_area(coords[:, [0, 1]])
    area_yz = triangulation_area(coords[:, [1, 2]])
    area_xz = triangulation_area(coords[:, [0, 2]])

    return area_xy, area_yz, area_xz

def calculate_perimeter(coords):
    if len(coords) < 3:
        return 0.0
    hull = ConvexHull(coords)
    perimeter = 0.0
    for simplex in hull.simplices:
        p1 = np.array(coords[simplex[0]])
        p2 = np.array(coords[simplex[1]])
        perimeter += np.linalg.norm(p1 - p2)
    return round(perimeter / 12, 1)

def calculate_footing_perimeter(coords):
    if len(coords) < 3:
        return []

    hull = ConvexHull(coords)
    perimeter_coords = [coords[vertex] for vertex in hull.vertices]

    return perimeter_coords

def calculate_wind_loads_and_present(wind_force, building_height, roof_perimeter, ifc_path):
    """
    Calculate and present wind loads on the building.
    """
    # Calculate wind pressure (force per unit length)
    wind_pressure = wind_force / roof_perimeter

    # Calculate wall moments due to wind force
    wall_moment = wind_pressure * building_height

    # Prepare the results
    results = {
        'Wind Force': wind_force,
        'Building Height': building_height,
        'Roof Perimeter': roof_perimeter,
        'Wind Pressure': round(wind_pressure, 2),
        'Wall Moment': round(wall_moment, 2)
    }

    # Print the results in a structured format
    print("Wind Load Calculation Results:")
    print(f"Wind Force: {results['Wind Force']} lbs")
    print(f"Building Height: {results['Building Height']} feet")
    print(f"Roof Perimeter: {results['Roof Perimeter']} feet")
    print(f"Wind Pressure: {results['Wind Pressure']} lbs/ft")
    print(f"Wall Moment: {results['Wall Moment']} ft-lbs")

    return results

def calculate_linear_load(perimeter, roof_uplift, roof_downpressure):
    net_pressure = roof_downpressure - roof_uplift
    linear_load = net_pressure * perimeter
    return round(linear_load, 2)

def calculate_wall_moments(wind_force, height):
    moment = wind_force * height
    return round(moment, 2)

def calculate_roof_perimeter(coordinates):
    """Calculate the perimeter of the roof based on the given coordinates."""
    if not coordinates:
        return 0.0
    
    # Extract the Z-axis values
    z_vals = [coord[2] for coord in coordinates]
    
    # Find the maximum Z-axis value (highest elevation)
    max_z = max(z_vals)
    
    # Extract coordinates that are at the highest elevation
    roof_coords = [coord[:2] for coord in coordinates if coord[2] == max_z]
    
    if len(roof_coords) < 3:
        return 0.0

    perimeter = 0.0
    num_points = len(roof_coords)
    
    for i in range(num_points):
        x1, y1 = roof_coords[i]
        x2, y2 = roof_coords[(i + 1) % num_points]
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        perimeter += distance
    
    return round(perimeter, 2)

def calculate_dead_load(ifc_file):
    # Open the IFC file
    model = ifcopenshell.open(ifc_file)

    total_dead_load = 0.0

    for element in model.by_type('IfcElementQuantity'):
        for quantity in element.Quantities:
            if quantity.is_a('IfcQuantityWeight'):
                if 'Dead Load' in quantity.Name or 'DeadLoad' in quantity.Name or 'Gross Weight' in quantity.Name or 'GrossWeight' in quantity.Name:
                    total_dead_load += quantity.WeightValue

    return total_dead_load


def calculate_wind_loads(ifc_file):
    # Open the IFC file
    model = ifcopenshell.open(ifc_file)

    wind_pressure = 0.0
    wall_moment = 0.0

    # List of possible names for wind pressure and wall moment
    wind_pressure_names = ['Wind Pressure', 'WindPressure', 'Wind Load', 'WindLoad', 'Wind_Pressure', 'Wind_Load']
    wall_moment_names = ['Wall Moment', 'WallMoment', 'Wind Moment', 'WindMoment', 'Wall_Moment', 'Wind_Moment']

    for element in model.by_type('IfcElementQuantity'):
        for quantity in element.Quantities:
            # Check for wind pressure
            if any(name in quantity.Name for name in wind_pressure_names):
                if quantity.is_a('IfcQuantityArea'):
                    wind_pressure = quantity.AreaValue
                elif quantity.is_a('IfcQuantityLength'):
                    wind_pressure = quantity.LengthValue
                elif quantity.is_a('IfcQuantityVolume'):
                    wind_pressure = quantity.VolumeValue
                elif quantity.is_a('IfcQuantityForce'):
                    wind_pressure = quantity.ForceValue
                elif quantity.is_a('IfcQuantityPressure'):
                    wind_pressure = quantity.PressureValue

            # Check for wall moment
            if any(name in quantity.Name for name in wall_moment_names):
                if quantity.is_a('IfcQuantityArea'):
                    wall_moment = quantity.AreaValue
                elif quantity.is_a('IfcQuantityLength'):
                    wall_moment = quantity.LengthValue
                elif quantity.is_a('IfcQuantityVolume'):
                    wall_moment = quantity.VolumeValue
                elif quantity.is_a('IfcQuantityForce'):
                    wall_moment = quantity.ForceValue
                elif quantity.is_a('IfcQuantityMoment'):
                    wall_moment = quantity.MomentValue

    return {'Wind Pressure': wind_pressure, 'Wall Moment': wall_moment}

def calculate_snow_load(roof_area, snow_load_per_unit_area):
    """
    Calculate the total snow load on the roof.
    
    :param roof_area: Area of the roof in square feet.
    :param snow_load_per_unit_area: Snow load per unit area in lbs/sq. ft.
    :return: Total snow load in lbs.
    """
    total_snow_load = roof_area * snow_load_per_unit_area
    return round(total_snow_load, 2)

def calculate_ice_load(roof_area, ice_load_per_unit_area):
    """
    Calculate the total ice load on the roof.

    :param roof_area: Area of the roof in square feet.
    :param ice_load_per_unit_area: Ice load per unit area in lbs/sq. ft.
    :return: Total ice load in lbs.
    """
    total_ice_load = roof_area * ice_load_per_unit_area
    return round(total_ice_load, 2)

