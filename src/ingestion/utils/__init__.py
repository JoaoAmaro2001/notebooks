# __init__.py

import os
import sys
import glob

# Initialize current directory and user-specific paths
cdir = os.getcwd()
user = os.environ.get('USER') or os.environ.get('UserName')

# Define user-specific paths
def set_user_paths(user):
    try:
        if user == 'joaop':  # Personal computer
            root = r'Z:\Exp_4-outdoor_walk\lisbon'  # LAN
            os.chdir(root)
        elif user == 'Administrator':  # MSI computer
            root = r'I:\Joao\Exp_4-outdoor_walk\lisbon'
        elif user == 'NGR_FMUL':  # University machine
            root = r'I:\Joao\Exp_4-outdoor_walk\lisbon'
        else:
            sys.exit('The directories for the input and output data could not be found')

        os.chdir(cdir)  # Return to the current working directory
        return root
    except Exception as e:
        print(f"Error setting user paths: {e}")
        sys.exit(1)

# Set root path and script paths
root = set_user_paths(user)
scripts = os.path.join(root, 'scripts')
sourcedata = os.path.join(root, 'sourcedata')
bidsroot = os.path.join(root, 'bids')
results = os.path.join(root, 'results')
derivatives = os.path.join(root, 'derivatives')

# Add scripts directory and subdirectories to the Python path
for path in glob.glob(os.path.join(scripts, '**'), recursive=True):
    if os.path.isdir(path):
        sys.path.append(path)

# Expose specific paths and variables to make them accessible
__all__ = ["cdir", "user", "root", "scripts", "sourcedata", "bidsroot", "results", "derivatives"]
