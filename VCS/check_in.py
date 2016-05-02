from create_repo import check_sum
from create_repo import get_directory
from create_repo import write_hierarchy
from datetime import datetime
from sys import argv
import os
import shutil

# Current Working Directory Path.
g_NAME_OF_CURRENT_DIRECTORY = argv[0]

# Repo Directory Path.
g_NAME_OF_REPO = argv[1] + "/repo343"

# Manifest Directory Path.
g_NAME_OF_MANIFEST_FOLDER = argv[1] + "/repo343/MANIFEST"

# A set of files and directories to ignore.
g_DIRECTORY_AND_FILES_TO_IGNORE = set(['.DS_Store', "repo343"])


# Checks in the given current working directory.
# Globals: None.
# A line count = 3
def check_in():
    """Checks in the given current working directory."""

    # Calls walk_directory function to get the map of file paths.
    a_file_path = walk_directory()

    copy_files(a_file_path)  # Calls copy_files function

    create_manifest(a_file_path)  # Calls create_manifest function

# Walks through the current working diretory.
# Globals: g_NAME_OF_CURRENT_DIRECTORY use for walking project tree.
# Globals: g_DIRECTORY_AND_FILES_TO_IGNORE use for ignoring directory and files.
# A line count = 9
def walk_directory():
    """Walks through the current working diretory."""
    a_path_for_files = {} # Map to store list of paths

    # Walk in the given current directory.
    for (a_dir_path, a_dir_name, a_file_names) in os.walk(g_NAME_OF_CURRENT_DIRECTORY, topdown = True):

        # get rid of directories that are in the ignore set.
        a_dir_name[:] = [d for d in a_dir_name if d not in g_DIRECTORY_AND_FILES_TO_IGNORE]

        # get rid of files that are in the ignore set.
        a_file_names[:] = [d for d in a_file_names if d not in g_DIRECTORY_AND_FILES_TO_IGNORE]

        a_list_of_files = [] # List to store path of files.

        for file_name in a_file_names:

            a_list_of_files.append(file_name) # append files to list.

        a_path_for_files[a_dir_path] = a_list_of_files # Map the list

    return a_path_for_files # return the map of file paths.

# Copies files to their respective project tree directory.
# Globals: g_NAME_OF_REPO use for writing project tree.
# A line count = 8
def copy_files(a_file_path):
    """Copies files to their respective project tree directory."""

    # loop for getting all the files in a map of lists.
    for files in a_file_path:
        for file in a_file_path[files]:

            # Path of project tree inside the repo.
            directoryPath = g_NAME_OF_REPO + "/" + argv[0].split("/")[-1]

            for x in range(len(files.split("/"))-1, files.split("/").index(argv[0].split("/")[-1]), -1):
                    directoryPath += "/" + files.split("/")[x]

            directoryPath = directoryPath + "/" + file

            # The check sum name of the given.
            checkSumName = check_sum(files + "/" + file)

            # Check if the file project tree directory exists.
            if not os.path.isdir(directoryPath):

                # Create the project tree directory.
                os.makedirs(directoryPath)

            # check if the checkSumName already exists in their respective project tree directory.
            if not os.path.exists(directoryPath + "/" + checkSumName):

                # Copy the files in the current working directory to their respective project tree directory.
                shutil.copyfile(files + "/" + file, directoryPath + "/" + checkSumName)

# Writes the parent manifest file to the current manifest file.
# Globals: g_NAME_OF_MANIFEST_FOLDER use for getting manifest files.
# A line count = 5
def write_parent(manifest_file):
    """Writes the parent manifest file to the current manifest file."""
    a_manifest_file = [] # Array to keep track of manifest file names

    # loop through the MANIFEST directory.
    for (a_dir_path, a_dir_name, a_file_names) in os.walk(get_directory(), topdown = True):

        # get rid of directories that are in the ignore set.
        a_dir_name[:] = [d for d in a_dir_name if d not in g_DIRECTORY_AND_FILES_TO_IGNORE]
        # get rid of files that are in the ignore set.
        a_file_names[:] = [d for d in a_file_names if d not in g_DIRECTORY_AND_FILES_TO_IGNORE]

        # set the a_manifest_file array to a_file_names
        for file in a_file_names:
            a_manifest_file.append(file)

    # Remove all files that doesn't have the MANIFEST_ prefix
    a_manifest_file = [a for a in a_manifest_file if "MANIFEST_" in a]

    # The latest manifest will be written as the parent.
    manifest_file.write("\nParent file: " + a_manifest_file[0])

    # Remove old manifest file in the Projet Tree
    os.remove(get_directory() + a_manifest_file[0])

# Creates the manifest file for the repo343 directory.
# Globals: g_NAME_OF_MANIFEST_FOLDER use for file path.
# A line count = 5
def create_manifest(directory_list):
    """Creates the manifest file for the repo343 directory."""

    # Manifest File Name
    manifest_name = "MANIFEST_" + argv[0].split("/")[-2] + "_" + str(datetime.now()) + ".txt"

    # Sets the file name of MANIFEST to the current datetime.
    MANIFEST = g_NAME_OF_MANIFEST_FOLDER + "/" + manifest_name

    # Create and open manifest file.
    manifest_file = open(MANIFEST, 'w+')

    # Write project tree hierachy to manifest file.
    write_hierarchy(manifest_file, directory_list)

    # Writes the parent file to the manifest
    write_parent(manifest_file)

    # Close manifest file.
    manifest_file.close()

    # Copy manifest file to the Project Tree Folder
    shutil.copyfile(MANIFEST, get_directory() + manifest_name)

# Check if the script is ran independently.
if __name__ == "__main__":
    check_in()