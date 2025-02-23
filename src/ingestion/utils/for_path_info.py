import os
import re
import shutil
import numpy as np
import pandas as pd
from pandas import Timedelta
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
    organize_sub_folders(os.path.join(sourcedata,"data"))

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

def fetch_stoppage_times(sourcedata, participant_folder, session_name):
    
    # Create IDs for checkpoints
    participant_num = participant_folder[2:]
    full_id = 'OE123' + participant_num

    # LSL data
    df_lsl = pd.read_csv(os.path.join(sourcedata, 'supp', 'stress_csv', f'sub-{participant_folder}', f'ses-{session_name}','lsl_markers.csv'))
    # SAM data
    df_sam = pd.read_excel(os.path.join(sourcedata, 'supp', 'sam.xlsx'))

    # Compute beginning and end times in seconds
    df_sam["Carimbo de data/hora"] = pd.to_datetime(df_sam["Carimbo de data/hora"])
    df_lsl["Seconds"] = pd.to_datetime(df_lsl["Seconds"])
    beg_sec = df_lsl.loc[df_lsl["MarkerIdx"] == 35005, "Seconds"].dt.round("1s")
    end_sec = df_lsl.loc[df_lsl["MarkerIdx"] == 35006, "Seconds"].dt.round("1s")

    # Define the coordinates for each checkpoint and questionnaire
    checkpoint_coords = [
        {
            "check_coords": ("9.1946400°W", "38.6964075°N"),
            "quest_coords": ("9.1945664°W", "38.6963377°N")
        },
        {
            "check_coords": ("9.1933845°W", "38.6958142°N"),
            "quest_coords": ("9.1932788°W", "38.6958434°N")
        },
        {
            "check_coords": ("9.1931279°W", "38.6957859°N"),
            "quest_coords": ("9.1933166°W", "38.6957510°N")
        },
        {
            "check_coords": ("9.1961935°W", "38.6957208°N"),
            "quest_coords": ("9.1965557°W", "38.6957057°N")
        },
        {
            "check_coords": ("9.1934005°W", "38.6958538°N"),
            "quest_coords": ("9.1931204°W", "38.6959132°N")
        }
    ]

    times = list()
    checkpoints = ('_1', '_2', '_3', '_4', '_5')

    for i, check in enumerate(checkpoints):
        check_num = int(check.strip('_'))  # Extract checkpoint number
        check_id = full_id + check  # Create checkpoint ID

        # Create the checkpoint ID (e.g., full_id + '_1')
        check_id = full_id + check

        # Compute time for checkpoint (35200 + check_num) - (35100 + check_num)
        time_walk = df_lsl.loc[df_lsl["MarkerIdx"] == 35200 + check_num, "Seconds"].iloc[0]
        time_stop = df_lsl.loc[df_lsl["MarkerIdx"] == 35100 + check_num, "Seconds"].iloc[0]

        # Perform the subtraction and round to the nearest second
        time_in_check = (time_walk - time_stop).round('1s')

        quest_time = df_sam.loc[df_sam["Escreva o código de participante"] == check_id, "Carimbo de data/hora"].iloc[0]
        marker_time = df_lsl.loc[df_lsl["MarkerIdx"] == 35300 + check_num, "Seconds"].iloc[0]
        time_in_quest = (quest_time - marker_time).round('1s')
        # Handle negative Timedelta (e.g., '-1 days +23:59:46')
        if time_in_quest < Timedelta('0s'):
            time_in_quest = Timedelta('15s')  # Assume 15 seconds duration

        # Append results
        times.append({
            "checkpoint": check_num,
            "time_in_check": time_in_check,
            "time_in_quest": time_in_quest,
            "check_coords": checkpoint_coords[i]["check_coords"],  # Checkpoint coordinates
            "quest_coords": checkpoint_coords[i]["quest_coords"],   # Questionnaire coordinates
            "beg_sec": beg_sec,  # First moment of the walk
            "end_sec": end_sec   # Last moment of the walk
        })

    return times