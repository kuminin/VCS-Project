from create_repo import check_sum
from datetime import datetime
from sys import argv
import create_repo
import os, shutil

# Current Working Directory Path.
g_NAME_OF_CURRENT_DIRECTORY = argv[1]
# Repo Directory Path.
g_NAME_OF_REPO = argv[0] + "/repo343"

# Manifest Directory Path.
g_NAME_OF_MANIFEST_FOLDER = argv[0] + "/repo343/MANIFEST"

# A set of files and directories to ignore.
g_DIRECTORY_AND_FILES_TO_IGNORE = set(["repo343", ".DS_Store"])

# Checks out a given project manifest based on user input.
# Globals: None.
# A line count = 6
def check_out():
    """Checks out a given project manifest based on user input."""

    a_manifest_files = get_manifest() # Gets the list of mainfest files.

    user_input = type_input(a_manifest_files) # Gets user input.

    # Checks for user input
    while user_input < 1 or len(a_manifest_files) < user_input:
        user_input = type_input(a_manifest_files)

    copy_files(a_manifest_files, user_input) # Copies the files into the current working directory.

# Copies the files into the current working directory.
# Globals: g_NAME_OF_MANIFEST_FOLDER use for manifest file path.
# A line count = 8
def copy_files(a_manifest_files, user_input):
    """Copies the files into the current working directory."""
    a_file_lines = [] # list to store all the lines in manifest file.

    manifest_file_path = g_NAME_OF_MANIFEST_FOLDER + "/" + a_manifest_files[user_input - 1]

    copy_manifest(manifest_file_path)

    # open manifest file as read only.
    manifest_file = open(manifest_file_path, "r")

    # reads the manifes_file line by line and trim white spaces
    for line in manifest_file:
        a_file_lines.append(line.strip())

    manifest_file.close() # close the manifes file

    print a_file_lines

    # copies the files from the project leaf tree into our target destination.
    for i in range(1, len(a_file_lines) - 3):
        a_file_path = a_file_lines[i].split("/")
        project_tree_name = a_file_path[a_file_path.index(manifest_file_path.split("_")[1]) + 1]
        project_tree_path = g_NAME_OF_CURRENT_DIRECTORY + "/" + project_tree_name
        if not os.path.exists(project_tree_path):
            os.makedirs(project_tree_path)
        if (len(a_file_path) - 1) - a_file_path.index(project_tree_name) > 2:
            sub_folder_directory = project_tree_path + "/" + a_file_path[a_file_path.index(project_tree_name) + 1]
            if not os.path.exists(sub_folder_directory):
                os.makedirs(sub_folder_directory)
            shutil.copy(get_file(a_file_path, manifest_file_path), sub_folder_directory + "/" + a_file_path[-2])
        else:
            shutil.copy(get_file(a_file_path, manifest_file_path), project_tree_path + "/" + a_file_path[-2])


def get_file(a_file_path, manifest_file_path):
    temp_name_of_repo = g_NAME_OF_REPO
    project_tree_name = a_file_path.index(manifest_file_path.split("_")[1]) + 1
    for i in range(project_tree_name, len(a_file_path)):
        temp_name_of_repo = temp_name_of_repo + "/" + a_file_path[i]
    return temp_name_of_repo

def copy_manifest(manifest_file_path):
    a_manifest_file_lines = []
    date_time_now = str(datetime.now())
    child_manifest_path = g_NAME_OF_CURRENT_DIRECTORY + "/" + "MANIFEST_" + argv[1].split("/")[-1] + "_" + date_time_now + ".txt"
    parent_manifest_file = open(manifest_file_path, "r")
    for line in parent_manifest_file:
        a_manifest_file_lines.append(line)
    parent_manifest_file.close()

    child_manifest_file = open(child_manifest_path, "w+")

    for i in range(len(a_manifest_file_lines)-1):
        child_manifest_file.write(a_manifest_file_lines[i])

    child_manifest_file.write("Parent file: " + manifest_file_path.split("/")[-1])

    child_manifest_file.close()
    shutil.copy(child_manifest_path, g_NAME_OF_MANIFEST_FOLDER)


# Ask user for the Manifest they'd like to check_out.
# Globals: None.
# A line count = 7
def type_input(a_manifest_files):
    """Ask user for the Manifest they'd like to check_out."""

    print "1: Oldest" # Print for user to know what input is oldest

    print str(len(a_manifest_files)) + ": Newest" # Print for user to know what input is newest

    # Print for user to show what are the valid inputs.
    print "Choose 1-" + str(len(a_manifest_files)) + ". The manifest files are:"

    # Loops through the manifest files and prints them
    for i in range(len(a_manifest_files)):

        print str(i + 1) + ":", a_manifest_files[i]

    # Gets User input.
    number = input("Please Enter, " + str(1) + "-" + str(len(a_manifest_files)) + ", The Manifest You'd Wish To Check Out: ")

    return number # return the user input.

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

    return a_manifest_files # return the list of file names.

# Check if the script is ran independently.
if __name__ == "__main__":
    check_out()
