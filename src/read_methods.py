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
from main import *
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

import ifcopenshell
import re
# import seaborn as sns
# import matplotlib.pyplot as plt
import numpy as np
# from scipy.spatial import Delaunay, ConvexHull
from tkinter import Tk, messagebox, Label, Checkbutton, BooleanVar, Entry
# from tkinterdnd2 import TkinterDnD, DND_FILES
# import os
# from fpdf import FPDF
# import tkinter as tk
# from tkinter import simpledialog

def explore_ifc_properties(ifc_path):
    import ifcopenshell
    ifc_file = ifcopenshell.open(ifc_path)

    for element in ifc_file.by_type('IfcElement'):
        material_set = element.IsDefinedBy
        if material_set:
            for definition in material_set:
                if definition.is_a('IfcRelDefinesByProperties'):
                    property_set = definition.RelatingPropertyDefinition
                    if property_set.is_a('IfcPropertySet'):
                        print(f"Element: {element.GlobalId}")
                        for prop in property_set.HasProperties:
                            if prop.is_a('IfcPropertySingleValue'):
                                print(f"Property Name: {prop.Name}, Value: {prop.NominalValue}")


def extract_element_counts(ifc_path):
    """Extracts the counts of specific elements from an IFC file."""
    ifc_file = ifcopenshell.open(ifc_path)
    element_counts = {
        'IfcBeam': len(ifc_file.by_type('IfcBeam')),
        'IfcColumn': len(ifc_file.by_type('IfcColumn'))
    }
    return element_counts


def extract_ifc_data(ifc_path):
    """Extracts IFC data and calculates the total weight from an IFC file using ifcopenshell."""
    total_weight = 0.0
    ifc_file = ifcopenshell.open(ifc_path)
    for quantity in ifc_file.by_type('IfcQuantityWeight'):
        if quantity:
            total_weight += quantity.WeightValue
    return round(total_weight, 2)

def extract_section_types(ifc_path):
    """Extracts unique section types from an IFC file using ifcopenshell."""
    section_types = set()
    ifc_file = ifcopenshell.open(ifc_path)
    for element in ifc_file.by_type('IfcStructuralProfileProperties'):
        section_types.add(element.ProfileName)
    for element in ifc_file.by_type('IfcCShapeProfileDef'):
        section_types.add(element.ProfileName)
    return section_types

def extract_Aux_data(ifc_path):
    """Extracts auxiliary data (section counts and weights) from an IFC file using ifcopenshell."""
    Aux_data = {}
    ifc_file = ifcopenshell.open(ifc_path)
    for element in ifc_file.by_type('IfcStructuralProfileProperties'):
        section_name = element.ProfileName
        if section_name not in Aux_data:
            Aux_data[section_name] = {'count': 0, 'total_weight': 0.0}
        Aux_data[section_name]['count'] += 1
    for element in ifc_file.by_type('IfcQuantityWeight'):
        section_name = element.Name
        if section_name in Aux_data:
            Aux_data[section_name]['total_weight'] += element.WeightValue
    for key in Aux_data:
        Aux_data[key]['total_weight'] = round(Aux_data[key]['total_weight'], 2)
    total_stud_count = sum(data['count'] for data in Aux_data.values())
    return total_stud_count, Aux_data

def extract_floor_data(ifc_path):
    """Extracts floor data to determine the number of stories in the building using ifcopenshell."""
    ifc_file = ifcopenshell.open(ifc_path)
    floors = len(ifc_file.by_type('IfcBuildingStorey'))
    return floors


def extract_forces_moments(ifc_path):
    """Extracts total forces and moments from an IFC file."""
    forces = {}
    moments = {}

    # Load the IFC file
    ifc_file = ifcopenshell.open(ifc_path)
    
    # Check the schema of the IFC file
    schema = ifc_file.schema

    # Define patterns based on schema
    if schema == "IFC2X3":
        # If the schema is IFC2X3, handle accordingly
        print("Using schema IFC2X3")
        # You may need to use different entity names or extraction methods
        # Currently, there's no direct equivalent for IfcForceVector and IfcMomentVector in IFC2X3
        # Hence, we would need to understand the exact requirement and map them accordingly
        return forces, moments
    elif schema.startswith("IFC4"):
        # If the schema is IFC4 or any of its derivatives
        print("Using schema IFC4")
        force_pattern = re.compile(r'IFCFORCEVECTOR\(([^,]+),([^,]+),([^,]+)\);')
        moment_pattern = re.compile(r'IFCMOMENTVECTOR\(([^,]+),([^,]+),([^,]+)\);')
        floor_pattern = re.compile(r'#\d+=\s*IFCBUILDINGSTOREY\(([^,]+),')

        current_floor = "Foundation"

        for line in open(ifc_path, 'r'):
            floor_match = floor_pattern.search(line)
            if floor_match:
                current_floor = floor_match.group(1).strip("'")
                if current_floor not in forces:
                    forces[current_floor] = np.zeros(3)
                    moments[current_floor] = np.zeros(3)
            force_match = force_pattern.search(line)
            if force_match:
                force_values = list(map(float, force_match.groups()))
                forces[current_floor] += np.array(force_values)
            moment_match = moment_pattern.search(line)
            if moment_match:
                moment_values = list(map(float, moment_match.groups()))
                moments[current_floor] += np.array(moment_values)

        return forces, moments
    else:
        raise ValueError(f"Unsupported IFC schema: {schema}")

def parse_ifc_file(ifc_path, zero_val=None):
    """Parses the IFC file to extract 3D coordinates using ifcopenshell."""
    remove_zero_point_var = BooleanVar(value=False)
    if zero_val is not None:
        remove_zero_point_var = zero_val
    coordinates = []
    ifc_file = ifcopenshell.open(ifc_path)
    for point in ifc_file.by_type('IfcCartesianPoint'):
        coord_tuple = tuple(point.Coordinates)
        if len(coord_tuple) == 3 and (not remove_zero_point_var.get() or coord_tuple != (0.0, 0.0, 0.0)):
            coordinates.append(tuple(round(x / 12, 2) for x in coord_tuple))
    return coordinates
