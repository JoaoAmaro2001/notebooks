import os
import sys
import glob
from pathlib import Path


def setpath_city(CITY='lisbon'):

    # --- Set your default city here ---
    print(f"Current city is {CITY}!")
    print("If you wish to change the city, please edit the value in the __init__.py file")

    # --- Get current directory and user name ---
    cdir = os.getcwd()
    user = os.environ.get('USER') or os.environ.get('UserName')

    # --- Determine paths based on the chosen city and the current user ---
    if CITY.lower() == 'lisbon':
        if user == 'joaop':
            try:
                root = r'Z:\Exp_4-outdoor_walk\lisbon'  # LAN
                os.chdir(root)
                os.chdir(cdir)
            except Exception:
                root = r'D:\Joao\Exp_4-outdoor_walk\lisbon'  # Local
            scripts = r'C:\Users\joaop\git\JoaoAmaro2001\WorkRepo'
        elif user == 'Administrator':
            try:
                root = r'Z:\Exp_4-outdoor_walk\lisbon'
                os.chdir(root)
                os.chdir(cdir)
            except Exception:
                root = r'I:\Joao\Exp_4-outdoor_walk\lisbon'
            scripts = r'C:\git\JoaoAmaro2001\WorkRepo'
        elif user == 'NGR_FMUL':
            try:
                root = r'Z:\Exp_4-outdoor_walk\lisbon'
                os.chdir(root)
                os.chdir(cdir)
            except Exception:
                root = r'I:\Joao\Exp_4-outdoor_walk\lisbon'
            scripts = r'C:\github\JoaoAmaro2001\WorkRepo'
        else:
            sys.exit('The directories for the input and output data could not be found for Lisbon.')

    elif CITY.lower() == 'copenhagen':
        if user == 'joaop':
            try:
                root = r'Z:\Exp_4-outdoor_walk\copenhagen'  # LAN
                os.chdir(root)
                os.chdir(cdir)
            except Exception:
                root = r'D:\Joao\Exp_4-outdoor_walk\copenhagen'  # Local
            scripts = r'C:\Users\joaop\git\JoaoAmaro2001\WorkRepo'
        elif user == 'Administrator':
            try:
                root = r'Z:\Exp_4-outdoor_walk\copenhagen'
                os.chdir(root)
                os.chdir(cdir)
            except Exception:
                root = r'I:\Joao\Exp_4-outdoor_walk\copenhagen'
            scripts = r'C:\git\JoaoAmaro2001\WorkRepo'
        elif user == 'NGR_FMUL':
            try:
                root = r'Z:\Exp_4-outdoor_walk\copenhagen'
                os.chdir(root)
                os.chdir(cdir)
            except Exception:
                root = r'I:\Joao\Exp_4-outdoor_walk\copenhagen'
            scripts = r'C:\github\JoaoAmaro2001\WorkRepo'
        else:
            sys.exit('The directories for the input and output data could not be found for Copenhagen.')

    elif CITY.lower() == 'london':
        if user == 'joaop':
            try:
                root = r'Z:\Exp_4-outdoor_walk\london'  # LAN
                os.chdir(root)
                os.chdir(cdir)
            except Exception:
                root = r'D:\Joao\Exp_4-outdoor_walk\london'  # Local
            scripts = r'C:\Users\joaop\git\JoaoAmaro2001\WorkRepo'
        elif user == 'Administrator':
            try:
                root = r'Z:\Exp_4-outdoor_walk\london'
                os.chdir(root)
                os.chdir(cdir)
            except Exception:
                root = r'I:\Joao\Exp_4-outdoor_walk\london'
            scripts = r'C:\git\JoaoAmaro2001\WorkRepo'
        elif user == 'NGR_FMUL':
            try:
                root = r'Z:\Exp_4-outdoor_walk\london'
                os.chdir(root)
                os.chdir(cdir)
            except Exception:
                root = r'I:\Joao\Exp_4-outdoor_walk\london'
            scripts = r'C:\github\JoaoAmaro2001\WorkRepo'
        else:
            sys.exit('The directories for the input and output data could not be found for London.')

    elif CITY.lower() == 'lansing':
        if user == 'joaop':
            try:
                root = r'Z:\Exp_4-outdoor_walk\lansing'  # LAN
                os.chdir(root)
                os.chdir(cdir)
            except Exception:
                root = r'D:\Joao\Exp_4-outdoor_walk\lansing'  # Local
            scripts = r'C:\Users\joaop\git\JoaoAmaro2001\WorkRepo'
        elif user == 'Administrator':
            try:
                root = r'Z:\Exp_4-outdoor_walk\lansing'
                os.chdir(root)
                os.chdir(cdir)
            except Exception:
                root = r'I:\Joao\Exp_4-outdoor_walk\lansing'
            scripts = r'C:\git\JoaoAmaro2001\WorkRepo'
        elif user == 'NGR_FMUL':
            try:
                root = r'Z:\Exp_4-outdoor_walk\lansing'
                os.chdir(root)
                os.chdir(cdir)
            except Exception:
                root = r'I:\Joao\Exp_4-outdoor_walk\lansing'
            scripts = r'C:\github\JoaoAmaro2001\WorkRepo'
        else:
            sys.exit('The directories for the input and output data could not be found for Lansing.')
    else:
        sys.exit(f"City '{CITY}' not recognized. Please choose from: lisbon, copenhagen, london, lansing.")

    # --- Define additional paths based on the root ---
    sourcedata  = os.path.join(root, 'sourcedata')
    bidsroot    = os.path.join(root, 'bids')
    results     = os.path.join(root, 'results')
    derivatives = os.path.join(root, 'derivatives')

    return sourcedata, bidsroot, results, derivatives, scripts

    # # --- Add all subdirectories of the scripts folder to sys.path ---
    # for path_entry in glob.glob(os.path.join(scripts, '**'), recursive=True):
    #     if os.path.isdir(path_entry) and path_entry not in sys.path:
    #         sys.path.append(path_entry)
