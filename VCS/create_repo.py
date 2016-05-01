import os
import shutil
from sys import argv
from datetime import datetime

g_NAME_OF_REPO = argv[1] + "/repo343" # Repo Directory Path.
g_NAME_OF_MANIFEST_FOLDER = argv[1] + "/repo343/MANIFEST" # Manifest Directory Path.


# Creates a repo343 that stores all the files for the project tree.
# Globals: parameter use for g_NAME_OF_REPO, g_NAME_OF_MANIFEST_FOLDER.
# ALine count = 9
def initialize_repo():
    """Creates a repo343 that stores all the files for the project tree."""
    # checks if the g_NAME_OF_REPO path exist.
    if not os.path.exists(g_NAME_OF_REPO):
        copy_tree() # calls copy_tree function

        # checks if g_NAME_OF_MANIFEST_FOLDER path exist.
        if not os.path.exists(g_NAME_OF_MANIFEST_FOLDER):
            os.makedirs(g_NAME_OF_MANIFEST_FOLDER) # Creates Manifest Directory

        file_path = walk_tree() # Walks the initial repo343 Project Tree. Stores all the files at a given directory.

        create_manifest(file_path) # Create Manifest file.

        create_leaf(file_path) # Creates leaf folders for files.

        return True # Return True for Assert purpose
    else:
        print g_NAME_OF_REPO + " Already Exists\n" # Print Debug

        return False # Return False for Assert purpose

# Copies the project tree where backend.py is located.
# Globals: parameter use for g_NAME_OF_REPO
# ALine count = 2
def copy_tree():
    """Copies the project tree where backend.py is located."""

    # All the files to ignore when copying the Project Tree.
    FILES_TO_IGNORE = '.DS_Store'

    # Copies the project tree to the repo343 directory.
    shutil.copytree(argv[0], g_NAME_OF_REPO + "/" + argv[0].split("/")[-1], ignore = shutil.ignore_patterns(FILES_TO_IGNORE))

# Walk through the initial repo343 directory.
# Globals: parameter use for g_NAME_OF_REPO and g_NAME_OF_MANIFEST_FOLDER
# ALine count = 8
def walk_tree():
    """Walk through the initial repo343 directory."""

    a_path_for_files = {} # Map to store list of files

    # Walks the repo343 directory.
    for (dir_path, dir_names, file_names) in os.walk(g_NAME_OF_REPO):

        # Check if the dir_path is not the Manifest Directory.
        if dir_path != g_NAME_OF_MANIFEST_FOLDER:

            a_list_of_files = [] # Array to hold list of files.

            # Walks to get all the files in a directory
            for file_name in file_names:
                a_list_of_files.append(file_name) # Appends file name to array

            # Map dir_path to list of files.
            a_path_for_files[dir_path] = a_list_of_files

    return a_path_for_files # return Map of directory and files.

# Creates the manifest file for the repo343 directory.
# Globals: g_NAME_OF_MANIFEST_FOLDER use for file path.
# ALine count = 5
def create_manifest(directory_list):
    """Creates the manifest file for the repo343 directory."""

    # Manifest File Name
    manifest_name = "MANIFEST_" + str(datetime.now()) + ".txt"

    # Sets the file name of MANIFEST to the current datetime.
    MANIFEST = g_NAME_OF_MANIFEST_FOLDER + "/" + manifest_name

    # Create and open manifest file.
    manifest_file = open(MANIFEST, 'w+')

    # Write project tree hierachy to manifest file.
    write_hierarchy(manifest_file, directory_list)

    # Write parent manifest file to current manifest file.
    manifest_file.write("\nParent file: null")

    # Close manifest file.
    manifest_file.close()

    # Copy manifest file to the Project Tree Folder
    src = ""
    for x in range (len(argv[0].split("/")) - 1):
        src += argv[0].split("/")[x] + "/"

    shutil.copyfile(MANIFEST, src + manifest_name)

# Write the project tree to the manifest file.
# Globals: None.
# ALine count = 7
def write_hierarchy(manifest_file, directory_list):
    """Writes the project hierarchy to the manifest file."""

    file_byte = 0L # Variable to get total byte size of files.

    # Write to file and get the path for all the files.
    a_file_listing = write_file(manifest_file, directory_list)

    # Get total byte size for every files.
    for file in a_file_listing:
        file_byte += os.stat(file).st_size

    # Write the number of files and the total size of files.
    manifest_file.write(str(len(a_file_listing)) + " Files\t" + str(file_byte) + " Bytes" + "\n")

    # sets the current_date to todays month/day/year respectively.
    current_date = str(datetime.now().month) + "/" + str(datetime.now().day) + "/" + str(datetime.now().year)

    # Write the current date to the file.
    manifest_file.write(current_date)

# Helper function for write_hierarchy.
# Globals: None.
# ALine count = 9
def write_file(manifest_file, directory_list):
    """Helper function for write_hierarchy."""

    a_file_listing = [] # Array to hold all file path.

    manifest_file.write("Project Tree Structure: \n") # Write string to file

    # loop through the directory in the list of directories
    for directory in directory_list:

        # Write the directory path in file except for the mainfest file.
        if directory != g_NAME_OF_MANIFEST_FOLDER and directory != g_NAME_OF_REPO:
            manifest_file.write("\t" + directory + "\n")

            # loop through the file in the list of files
            for files in directory_list[directory]:

                # Append path for files to listing
                a_file_listing.append(directory + "/" + files)

                # write the path for the file and its checksum
                manifest_file.write("\t\t" + directory + "/" + files + "/" + check_sum(directory + "/" + files) + "\n")
    return a_file_listing # return list of file paths.


# Creates the leaf directory folder for the files.
# Globals: None.
# ALine count = 8
def create_leaf(directory_list):
    """Creates the leaf directory folder for the files.
    """

    # loop through the directory in the list of directories
    for directory in directory_list:

        # loop through the file in the list of files
        for files in directory_list[directory]:

            file_path = directory + "/" # set the file path

            # get check sum name for the files
            check_sum_name = check_sum(file_path + files)

            # rename the file to the checksum name.
            os.rename(file_path + files, file_path + check_sum_name)

            # check if a directory exist to files (Leaf folder)
            if not os.path.exists(file_path + files):
                os.makedirs(file_path + files) # Create Leaf Folder

            # move the file to the leaf folder.
            shutil.move(file_path + check_sum_name, file_path + files + "/" + check_sum_name)

# Gets the check_sum for the file.
# Globals: None.
# ALine Count = 7
def check_sum(file_name):
    """Gets the check_sum for the file."""

    file = open(file_name, 'r') # open file name.

    check_sum = 0 # set check sum variable to 0.

    for line in file: # get every line for the file.
        for char in line: # get every char in line.
            check_sum += ord(char) # add the char to the check_sum.

    file.close() # close the file.

    return str(check_sum) # return string representation of check_sum.

# Check if the script is ran independently.
if __name__ == "__main__":
    initialize_repo()
