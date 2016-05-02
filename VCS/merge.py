import os
import shutil
from sys import argv
from datetime import datetime
from check_out import type_input


g_NAME_OF_REPO = argv[0] + "/repo343"  # Repo Directory Path.

# Manifest Directory Path.
g_NAME_OF_MANIFEST_FOLDER = argv[0] + "/repo343/MANIFEST"

# Project tree path location
g_NAME_OF_PT_PATH = argv[1]

# A set of files and directories to ignore.
g_DIRECTORY_AND_FILES_TO_IGNORE = set(['.DS_Store', "repo343"])

def merge_interface():

    a_manifest_files = get_manifest() # Gets the list of mainfest files.

    user_input = type_input(a_manifest_files) # Gets user input.

    # Checks for user input
    while user_input < 1 or len(a_manifest_files) < user_input:
        user_input = type_input(a_manifest_files)

    print a_manifest_files[user_input]


# Gets the list of mainfest files.
# Globals: g_NAME_OF_MANIFEST_FOLDER.
# A line count = 5
def get_manifest():
    """Gets the list of mainfest files."""

    a_manifest_files = [] # list to contain the manifest file names.

    # walk through the manifest folder directory
    for (a_dir_path, a_dir_name, a_file_names) in os.walk(g_NAME_OF_MANIFEST_FOLDER):
                # get rid of directories that are in the ignore set.
        a_dir_name[:] = [d for d in a_dir_name if d not in g_DIRECTORY_AND_FILES_TO_IGNORE]

        # get rid of files that are in the ignore set.
        a_file_names[:] = [d for d in a_file_names if d not in g_DIRECTORY_AND_FILES_TO_IGNORE]

        # Set the file names in the manifest folder directory to the a_manifest_files
        a_manifest_files = a_file_names

    a_manifest_files.sort() # Sort the list of file names.

    return remove_target(a_manifest_files) # return the list of file names.


def remove_target(a_manifest_files):
    a_temp_manifest_files = []
    owner = g_NAME_OF_PT_PATH.split("/")[-1]

    for files in a_manifest_files:
        if owner not in files:
            a_temp_manifest_files.append(files)

    return a_temp_manifest_files