# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                              IMPORT LIBRARIES                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import pandas as pd
import numpy as np

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                          PROCESSING FUNCTIONS                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def infer_participant_code(city, subject_id, session, stimulus):
    """
    Infers the participant code based on the city, subject ID, session, and stimulus.

    Parameters:
    - city (str): The city name ('lisbon' or 'copenhagen').
    - subject_id (int): The subject's ID number.
    - session (str): The session name.
    - stimulus (str): The stimulus identifier (can be an empty string if not applicable).

    Returns:
    - str: The inferred participant code.

    Raises:
    - ValueError: If the session name or stimulus is invalid.

    Examples:
    ---------
    # With stimulus (Lisbon)
    participant_id = infer_participant_code('lisbon', 3, 'Baixa', 'D12')
    print(participant_id)  # Output: 'OE104003_1'

    # Without stimulus (Lisbon)
    participant_id = infer_participant_code('lisbon', 5, 'Parque', '')
    print(participant_id)  # Output: 'OE106005'

    # For Copenhagen
    participant_id = infer_participant_code('copenhagen', 7, 'Nordhavn', 'B32')
    print(participant_id)  # Expected Output: 'OE203007_2'  (if 'B32' is the 2nd stimulus in the Nordhavn session)
    """

    if city.lower() == 'lisbon':
        # Lisbon mapping: (session name, session number)
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

        # Checkpoints for Lisbon sessions (order corresponding to session number)
        checkpoints = [
            ['A7', 'C9', 'C10'],            # Belem - 1
            ['A16', 'C17', 'C18'],          # Lapa - 2
            ['A3', 'B4', 'B6', 'B7'],       # Gulbenkian - 3
            ['D12', 'D27', 'D26', 'B10'],   # Baixa - 4
            ['C31', 'C32', 'D31', 'D32'],   # Graca - 5
            ['A24', 'A25'],                 # Parque (das Nações) - 6
            ['A99','A98','A97','A96','B99'] # Maat - 23
        ]

        # Find the session number from the session name.
        ses_num = None
        for name, number in sessions:
            if name.lower() == session.lower():
                ses_num = number
                break
        if ses_num is None:
            raise ValueError('Invalid session name.')

        # Format session and subject IDs.
        path_num = f"{ses_num:02d}"
        subject_id_str = f"{subject_id:03d}"

        # Determine the checkpoint index if a stimulus is provided.
        chk_num = None
        if stimulus != 'all' and stimulus:
            checkpoints_for_session = checkpoints[ses_num - 1]
            for idx, stim in enumerate(checkpoints_for_session):
                if stim.lower() == stimulus.lower():
                    chk_num = idx + 1  # MATLAB-like indexing (starting at 1)
                    break
            if chk_num is None:
                raise ValueError('Invalid stimulus for the given session.')
        else:
            chk_num = "f"

        if not stimulus:
            participant_id = f"OE1{path_num}{subject_id_str}"
        else:
            participant_id = f"OE1{path_num}{subject_id_str}_{chk_num}"
        return participant_id

    elif city.lower() == 'copenhagen':
        # Copenhagen mapping: (session name, session number)
        sessions = [
            ('Hellerup', 4),
            ('Norrebro', 1),
            ('Norreport', 2),
            ('Nordhavn', 3)         
        ]
        # Checkpoints for Copenhagen sessions:
        checkpoints = [
            ['C11','D12','B13'],  # Norrebro - session 1
            ['D21','A22','C23'],  # Norreport - session 2
            ['C31','B32','C33'],  # Nordhavn - session 3
            ['A41','A42','A43']   # Hellerup - session 4
        ]
        
        # Find the session number based on the session name.
        ses_num = None
        for name, number in sessions:
            if name.lower() == session.lower():
                ses_num = number
                break
        if ses_num is None:
            raise ValueError('Invalid session name.')

        # Format the session and subject IDs.
        path_num = f"{ses_num:02d}"
        subject_id_str = f"{subject_id:03d}"
        
        # Determine the checkpoint index if a stimulus is provided.
        chk_num = None
        if stimulus != 'all' and stimulus:
            checkpoints_for_session = checkpoints[ses_num - 1]
            for idx, stim in enumerate(checkpoints_for_session):
                if stim.lower() == stimulus.lower():
                    chk_num = idx + 1  # Using 1-indexing
                    break
            if chk_num is None:
                raise ValueError('Invalid stimulus for the given session.')
        else:
            chk_num = "f"

        # Construct the participant ID with the prefix "OE2" for Copenhagen.
        if not stimulus:
            participant_id = f"OE2{path_num}{subject_id_str}"
        else:
            participant_id = f"OE2{path_num}{subject_id_str}_{chk_num}"
        return participant_id

    else:
        raise ValueError('City not supported.')


def parse_participant_code(participant_code):
    """
    Parses the participant code to extract city, subject ID, session, and stimulus.

    Parameters:
    - participant_code (str): The participant code (e.g., 'OE106005' or 'OE104003_1').

    Returns:
    - dict: A dictionary containing 'city', 'subject_id', 'session', and 'stimulus'.

    Raises:
    - ValueError: If the participant code is invalid.

    Example:
    --------
    participant_info = parse_participant_code('OE104003_1')
    print(participant_info)
    # Output: {'city': 'Lisbon', 'subject_id': 3, 'session': 'Baixa', 'stimulus': 'D12'}
    """

    # Lisbon
    if participant_code.startswith('OE1'):

        city = 'lisbon'

        # Initialize mappings (same as in infer_participant_code)
        sessions = [
            ('Baixa', 4),
            ('Belem', 1),
            ('Parque', 6),
            ('Gulbenkian', 3),
            ('Lapa', 2),
            ('Graca', 5),
            ('Maat', 23)
        ]

        # Reverse mapping for session numbers to names
        session_num_to_name = {number: name for name, number in sessions}

        checkpoints = [
            ['A7', 'C9', 'C10'],            # Belem - 1
            ['A16', 'C17', 'C18'],          # Lapa - 2
            ['A3', 'B4', 'B6', 'B7'],       # Gulbenkian - 3
            ['D12', 'D27', 'D26', 'B10'],   # Baixa - 4
            ['C31', 'C32', 'D31', 'D32'],   # Graca - 5
            ['A24', 'A25'],                 # Parque (das Nações) - 6
            ['A99','A98','A97','A96','B99'] # Maat - 23
        ]

    # Copenhagen
    elif participant_code.startswith('OE2'):   

        city = 'copenhagen'; 

        # Initialize mappings (same as in infer_participant_code)
        sessions = [
            ('Hellerup', 4),
            ('Norrebro', 1),
            ('Norreport', 2),
            ('Nordhavn', 3)         
        ]

        # Reverse mapping for session numbers to names
        session_num_to_name = {number: name for name, number in sessions}

        checkpoints = [
            ['C11','D12','B13'],  # Norrebro - 1
            ['D21','A22','C23'],  # Norreport - 2
            ['C31','B32','C33'],  # Nordhavn - 3
            ['A41','A42','A43'],  # Hellerup - 4
        ]          

    # Extract path_num and subject_id
    rest = participant_code[3:]  # Remove 'OEx'
    if '_' in rest:
        # Participant code includes stimulus
        main_part, chk_num_str = rest.split('_')
        chk_num = int(chk_num_str)
    else:
        main_part = rest
        chk_num = None

    if len(main_part) < 5:
        raise ValueError('Invalid participant code format.')

    path_num_str = main_part[:2]
    subject_id_str = main_part[2:]

    # Convert to integers
    try:
        ses_num = int(path_num_str)
        subject_id = int(subject_id_str)
    except ValueError:
        raise ValueError('Invalid participant code format.')

    # Get session name
    session = session_num_to_name.get(ses_num)
    if not session:
        raise ValueError('Invalid session number in participant code.')

    # Get stimulus if available
    if chk_num is not None:
        try:
            stimulus = checkpoints[ses_num - 1][chk_num - 1]
        except IndexError:
            raise ValueError('Invalid checkpoint number in participant code.')
    else:
        stimulus = ''

    participant_info = {
        'city': city,
        'subject_id': subject_id,
        'session': session,
        'stimulus': stimulus
    }
    return participant_info
    
def fetch_beh_ratings(sourcedata, id):
    """Fetch behavioral data for a participant.
    Parameters
    ----------
    sourcedata : str
        Path to the directory containing the behavioral data.
    id : str 
        Output from infer_participant_code
    ----------
    Example:
    --------
        id = 'OE104003_1'
        sam = fetch_beh_ratings(sourcedata, id)
    """
    # Load behavioral data
    beh = pd.read_excel(os.path.join(sourcedata, 'sam.xlsx'))
    # Select behavioral data for the participant
    sam = beh[beh.iloc[:,1] == id].iloc[:,2:].values.astype(int)
    
    return sam


