import ifcopenshell

# Load the IFC file
ifc_file_path = "C:\\Users\\abelb\\Downloads\\trial\\IFC\\src\\test\\ifc.ifc"
ifc_file = ifcopenshell.open(ifc_file_path)

# Function to extract roofupliftpressure value
def get_roof_uplift_pressure(ifc_file):
    # Iterate over all elements
    for element in ifc_file.by_type('IfcElement'):
        # Retrieve property sets associated with the element
        if hasattr(element, 'IsDefinedBy'):
            for rel in element.IsDefinedBy:
                # Check if it has property sets
                if rel.is_a('IfcRelDefinesByProperties') and rel.RelatingPropertyDefinition.is_a('IfcPropertySet'):
                    property_set = rel.RelatingPropertyDefinition
                    print('jcv,bk')
                    # Iterate through the properties of the set
                    for prop in property_set.HasProperties:
                        print('jcv,bk')
                        # Check if the property name matches 'roofupliftpressure'
                        if prop.is_a('IfcPropertySingleValue') and prop.Name == 'roofupliftpressure':
                            return prop.NominalValue.wrappedValue

    return None

# Get roofupliftpressure value
roof_uplift_pressure = get_roof_uplift_pressure(ifc_file)

if roof_uplift_pressure:
    print(f"Roof Uplift Pressure: {roof_uplift_pressure}")
else:
    print("Roof Uplift Pressure not found.")
