#!/usr/bin/env python3
"""
triangle_stl.py - Generate a triangular prism STL for OpenFOAM refinement

This script creates a closed volume STL surface from a triangle with thickness,
useful for wake refinement in OpenFOAM ship simulations.

The geometry is parameterized by 'length' and 'h' from system/shipDict.
"""

import numpy as np
import struct
import os
import sys
import re

def create_kelvin2_stl(point1, point2, point3, thickness, output_path="kelvin2.stl"):
    


    """
    Generate a closed volume STL surface from a triangle with thickness.
    
    Parameters:
    -----------
    point1, point2, point3 : list or tuple
        3D coordinates of the triangle vertices [x, y, z]
    thickness : float
        Thickness of the triangular volume
    output_path : str, optional
        Path to save the STL file
    
    Returns:
    --------
    bool
        True if successful
    """
    try:
        # Convert points to numpy arrays
        p1 = np.array(point1, dtype=float)
        p2 = np.array(point2, dtype=float)
        p3 = np.array(point3, dtype=float)
        
        # Calculate normal vector for the triangle (using cross product)
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        
        # Check if the points form a valid triangle
        if np.linalg.norm(normal) < 1e-6:
            print("Error: The three points do not form a valid triangle.")
            return False
        
        normal = normal / np.linalg.norm(normal)  # Normalize
        
        # Create the offset points (triangle at thickness distance)
        offset = thickness * normal
        p4 = p1 + offset
        p5 = p2 + offset
        p6 = p3 + offset
        
        # Define the 8 triangular faces of the closed volume
        # Two original triangles (front and back)
        # Plus 6 triangles for the three rectangular sides (2 triangles per rectangle)
        faces = [
            # Front triangle (original)
            [p1, p2, p3],
            
            # Back triangle (offset)
            [p6, p5, p4],  # Note reversed order for correct normal direction
            
            # Side 1 (rectangle split into 2 triangles)
            [p1, p4, p2],
            [p2, p4, p5],
            
            # Side 2 (rectangle split into 2 triangles)
            [p2, p5, p3],
            [p3, p5, p6],
            
            # Side 3 (rectangle split into 2 triangles)
            [p3, p6, p1],
            [p1, p6, p4]
        ]
        
        # Calculate normals for each face
        normals = []
        for face in faces:
            v1 = face[1] - face[0]
            v2 = face[2] - face[0]
            n = np.cross(v1, v2)
            n = n / np.linalg.norm(n) if np.linalg.norm(n) > 0 else n
            normals.append(n)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Write binary STL file
        with open(output_path, 'wb') as f:
            # Write STL header (80 bytes)
            header = f"OpenFOAM triangular refinement volume ({len(faces)} facets)"
            header = header.ljust(80, ' ')
            f.write(header.encode('ascii'))
            
            # Write number of triangles (4 bytes)
            f.write(struct.pack('<I', len(faces)))
            
            # Write each triangle
            for i, face in enumerate(faces):
                # Normal vector (3 floats, 12 bytes)
                f.write(struct.pack('<3f', *normals[i]))
                
                # Vertex 1 (3 floats, 12 bytes)
                f.write(struct.pack('<3f', *face[0]))
                
                # Vertex 2 (3 floats, 12 bytes)
                f.write(struct.pack('<3f', *face[1]))
                
                # Vertex 3 (3 floats, 12 bytes)
                f.write(struct.pack('<3f', *face[2]))
                
                # Attribute byte count (2 bytes) - typically zero
                f.write(struct.pack('<H', 0))
        
        print(f"STL file successfully created at: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating STL file: {e}")
        return False  

    


    """
    Generate a closed volume STL surface from a triangle with thickness.
    
    Parameters:
    -----------
    point1, point2, point3 : list or tuple
        3D coordinates of the triangle vertices [x, y, z]
    thickness : float
        Thickness of the triangular volume
    output_path : str, optional
        Path to save the STL file
    
    Returns:
    --------
    bool
        True if successful
    """
    try:
        # Convert points to numpy arrays
        p1 = np.array(point1, dtype=float)
        p2 = np.array(point2, dtype=float)
        p3 = np.array(point3, dtype=float)
        
        # Calculate normal vector for the triangle (using cross product)
        v1 = p2 - p1
        v2 = p3 - p1
        normal = np.cross(v1, v2)
        
        # Check if the points form a valid triangle
        if np.linalg.norm(normal) < 1e-6:
            print("Error: The three points do not form a valid triangle.")
            return False
        
        normal = normal / np.linalg.norm(normal)  # Normalize
        
        # Create the offset points (triangle at thickness distance)
        offset = thickness * normal
        p4 = p1 + offset
        p5 = p2 + offset
        p6 = p3 + offset
        
        # Define the 8 triangular faces of the closed volume
        # Two original triangles (front and back)
        # Plus 6 triangles for the three rectangular sides (2 triangles per rectangle)
        faces = [
            # Front triangle (original)
            [p1, p2, p3],
            
            # Back triangle (offset)
            [p6, p5, p4],  # Note reversed order for correct normal direction
            
            # Side 1 (rectangle split into 2 triangles)
            [p1, p4, p2],
            [p2, p4, p5],
            
            # Side 2 (rectangle split into 2 triangles)
            [p2, p5, p3],
            [p3, p5, p6],
            
            # Side 3 (rectangle split into 2 triangles)
            [p3, p6, p1],
            [p1, p6, p4]
        ]
        
        # Calculate normals for each face
        normals = []
        for face in faces:
            v1 = face[1] - face[0]
            v2 = face[2] - face[0]
            n = np.cross(v1, v2)
            n = n / np.linalg.norm(n) if np.linalg.norm(n) > 0 else n
            normals.append(n)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Write binary STL file
        with open(output_path, 'wb') as f:
            # Write STL header (80 bytes)
            header = f"OpenFOAM triangular refinement volume ({len(faces)} facets)"
            header = header.ljust(80, ' ')
            f.write(header.encode('ascii'))
            
            # Write number of triangles (4 bytes)
            f.write(struct.pack('<I', len(faces)))
            
            # Write each triangle
            for i, face in enumerate(faces):
                # Normal vector (3 floats, 12 bytes)
                f.write(struct.pack('<3f', *normals[i]))
                
                # Vertex 1 (3 floats, 12 bytes)
                f.write(struct.pack('<3f', *face[0]))
                
                # Vertex 2 (3 floats, 12 bytes)
                f.write(struct.pack('<3f', *face[1]))
                
                # Vertex 3 (3 floats, 12 bytes)
                f.write(struct.pack('<3f', *face[2]))
                
                # Attribute byte count (2 bytes) - typically zero
                f.write(struct.pack('<H', 0))
        
        print(f"STL file successfully created at: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating STL file: {e}")
        return False    
    

def extract_value(value_str):
    """
    Extract numeric value from a string, ignoring #eval expressions.
    
    Parameters:
    -----------
    value_str : str
        String containing the value
        
    Returns:
    --------
    float or None
        Extracted value or None if not found
    """
    # Check if it's a simple numeric value
    try:
        return float(value_str)
    except ValueError:
        # If it contains #eval, extract the numeric value inside the expression
        if "#eval" in value_str:
            # Simple extraction of numeric values inside curly braces
            match = re.search(r'\{[^{}]*?(\d+(?:\.\d+)?)[^{}]*\}', value_str)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    pass
    return None

def read_ship_dict(path="shipDict"):
    """
    Read parameters from OpenFOAM dictionary file.
    
    Parameters:
    -----------
    path : str
        Path to the shipDict file
        
    Returns:
    --------
    dict
        Dictionary containing the parameters
    """
    # Hardcoded fallback values from the example file
    params = {'length': 6, 'h': 6/6.0}
    print(f"Using fallback values: length={params['length']}, h={params['h']}")
    
    try:
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"Successfully opened {path} with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        # If we still need to parse the file for more accurate values:
        # First, ensure we have the shipParameters block
        if "shipParameters" in content and "{" in content and "}" in content:
            # Just look for the specific lines we need
            length_line = None
            h_line = None
            
            for line in content.split('\n'):
                line = line.strip()
                if 'length' in line and '#eval' in line and ';' in line:
                    length_line = line
                if 'h ' in line and '#eval' in line and '$length/6' in line and ';' in line:
                    h_line = line
            
            # Process found lines
            if length_line:
                # Try to extract the number 8 from line like: length #eval {round(8)};
                length_value = re.search(r'round\s*\(\s*(\d+(?:\.\d+)?)\s*\)', length_line)
                if length_value:
                    params['length'] = float(length_value.group(1))
                    print(f"Extracted length = {params['length']} from line: {length_line}")
            
            if h_line:
                print(f"Found h line: {h_line}")
                # For h, we know it's length/6 from the file
                params['h'] = params['length'] / 6.0
                print(f"Set h = {params['h']} (length/6)")
        
        return params
    except Exception as e:
        print(f"Error reading shipDict: {e}")
        print("Using fallback values instead")
        return params

def main():
    """
    Main function to run when script is executed.
    Reads parameters from shipDict and generates the STL file.
    """
    # Check if we're in an OpenFOAM case directory structure
    if not os.path.isfile("shipDict"):
        print("Error: system/shipDict not found. Make sure you are in an OpenFOAM case directory.")
        return
    
    # Read parameters from shipDict
    params = read_ship_dict()
    
    # Check if required parameters exist
    if "length" not in params or "h" not in params:
        print("Error: Required parameters 'length' and 'h' not found in shipDict.")
        print("Available parameters:", list(params.keys()))
        return
    
    length = params["length"]
    h = round(params["h"])
    
    print(f"Parameters read from shipDict: length={length}, h={h}")
    
    # Define the triangle based on length
    # Simple triangle in the XY plane with thickness along Z
    point1 = [-1.45*length, -length*1.75, -h]                # Origin
    point2 = [length*1.85, 0 , -h]           # Length along X-axis
    point3 = [-1.45*length, length*1.75, -h]  # Point forming a triangle
    
    point4 = [-1.2*length, -length*1.25, -h]                # Origin
    point5 = [length*1.55, 0 , -h]           # Length along X-axis
    point6 = [-1.2*length, length*1.25, -h]  # Point forming a triangle
    
    point7 = [-0.6*length, -0.7*length, -h]                # Origin
    point8 = [length*1.2, 0 , -h]           # Length along X-axis
    point9 = [-0.6*length, 0.7*length, -h]  # Point forming a triangle
    
    
    
    # Define thickness based on h
    thickness = 2.05*h
    
    # Output path in constant/triSurface
    output_path2 = "kelvin2.stl"
    output_path3 = "kelvin3.stl"
    output_path4 = "kelvin4.stl"
    
    # Ensure the directory exists
    #os.makedirs("constant/triSurface", exist_ok=True)
    
    
    # Get FOAM_CASE environment variable
    
    #print(f"Creating triangle with:")
   # print(f"Points: {point1}, {point2}, {point3}")
    #print(f"Thickness: {thickness}")
    
    # Create the triangular kelvin2.STL
    create_kelvin2_stl(point1, point2, point3, thickness, output_path2)
    
    create_kelvin2_stl(point4, point5, point6, thickness, output_path3)
    
    create_kelvin2_stl(point7, point8, point9, thickness, output_path4)

    
   # create_kelvin2_stl(point7, point8, point9, thickness, output_path4)




if __name__ == "__main__":
    main()
