import os
import re
import shutil
import numpy as np
import pandas as pd
from unidecode import unidecode
import geopandas as gpd
from shapely.geometry import Point, LineString

def fetch_path_num(data_path, city):
    """Fetch the session number from the data path.
    Extract the session number from the data path.
    It can be exctracted from original data_path or from the session name.
    """
    if '_' in data_path:
        path = str(data_path)
        path = path.split('\\')
        filename = path[-1]
        match = re.search(r'1(\d{2})', filename)
        if match:
            # The group(1) method returns the matched string
            numbers = match.group(1)
            print(numbers)
    else:        
        if city == "lisbon":
            # Load session information
            sessions = [
                ('Baixa', 4),
                ('Belem', 1),
                ('Parque', 6),
                ('Gulbenkian', 3),
                ('Lapa', 2),
                ('Graca', 5),
                ('Gulb1', 7),
                ('Casamoeda', 8),
                ('Agudo', 9),
                ('Msoares', 10),
                ('Marvila', 11),
                ('Oriente', 12),
                ('Madre', 13),
                ('Pupilos', 14),
                ('Luz', 15),
                ('Alfarrobeira', 16),
                ('Restauradores', 17),
                ('Restelo', 18),
                ('Estrela', 19),
                ('EstrelaA', 20),
                ('EstrelaB', 21),
                ('Prazeres', 22),
                ('Maat', 23)           
            ]

        elif city == "copenhagen":
            # Load session information
            sessions = [
                ('Hellerup', 4),
                ('Norrebro', 1),
                ('Norreport', 2),
                ('Nordhavn', 3)         
            ]

        elif city == "lansing":
            # Load session information
            sessions = [
                ('DownTownNatural', 3),
                ('DownTownUrban', 4),
                ('NorthNatural', 1),
                ('NorthUrban', 2),
                ('SouthNatural', 5),
                ('SouthUrban', 6)                            
            ]   

        elif city == "london":
            # Load session information
            sessions = [
                ('BigBen', 1),
                ('NottingHill', 2),
                ('WhiteChapel', 3),
                ('Woolwhich', 4)
            ]               

        # Get number from sessions
        for session_name, session_number in sessions:
            if session_name.lower() in data_path.lower():
                numbers = session_number
    
    return numbers

def extract_session_name(folder_name):
    """Fetch corret session name from the original folder name
    Extract the first string between underscores in the folder name.
    Normalize special characters like 'ç' to 'c'.
    
    Args:
        folder_name (str): Folder name to extract the session name.
    
    Returns:
        str: Normalized session name or the original folder name if no match is found.
    """
    match = re.search(r'_(.*?)_', folder_name)  # Find first string between underscores
    if match:
        session_name = match.group(1)
        return unidecode(session_name)  # Normalize special characters
    return unidecode(folder_name)  # Fallback to the original folder name

def organize_sub_folders(parent_dir):
    """
    Organizes folders in the given directory by extracting the ID that follows "sub-"
    from each folder name and moving the folder into a new folder named with that ID.

    For example, if a folder is named:
        Lansing_DownTownNatural_sub-OE109002_2023-09-10T195100Z
    the function extracts "OE109002", creates a folder called "OE109002" (if it doesn't exist),
    and moves the original folder inside "OE109002".

    Example:
    organize_sub_folders(os.path.join(path.sourcedata,"data"))

    Parameters:
    -----------
    parent_dir : str
        Path to the directory containing the folders to organize.
    """
    # List all entries in the parent directory
    for entry in os.listdir(parent_dir):
        entry_path = os.path.join(parent_dir, entry)
        # Process only directories
        if os.path.isdir(entry_path):
            # Look for the pattern "sub-<ID>" where ID is any sequence of characters not including underscore.
            match = re.search(r"sub-([^_]+)", entry)
            if match:
                sub_id = match.group(1)
                new_folder_path = os.path.join(parent_dir, sub_id)
                # Create the new folder if it doesn't already exist
                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)
                destination = os.path.join(new_folder_path, entry)
                print(f"Moving folder '{entry}' into '{new_folder_path}'")
                shutil.move(entry_path, destination)
            else:
                print(f"No 'sub-' pattern found in folder name '{entry}'")
