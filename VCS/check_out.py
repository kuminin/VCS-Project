from create_repo import check_sum
from datetime import datetime
from sys import argv
import create_repo
import os, shutil

# Current Working Directory Path.
g_NAME_OF_PT_PATH = argv[1]

# Repo Directory Path.
g_NAME_OF_REPO_PATH = argv[0] + "/repo343"

# Manifest Directory Path.
g_NAME_OF_MANIFEST_PATH = argv[0] + "/repo343/MANIFEST"

# A set of files and directories to ignore.
g_DIRECTORY_AND_FILES_TO_IGNORE = set(["repo343", ".DS_Store"])

# Checks out a given project manifest based on user input.
# Globals: None.
# A line count = 5
def check_out():
    """Checks out a given project manifest based on user input."""

    a_manifest_files = get_manifest() # Gets the list of mainfest files.

    user_input = type_input(a_manifest_files) # Gets user input.

    # Validate user Input for the Manifest file
    while user_input < 1 or len(a_manifest_files) < user_input:
        user_input = type_input(a_manifest_files)

    copy_files(a_manifest_files, user_input) # Copies the files into the current working directory.

# Copies the files into the current working directory.
# Globals: g_NAME_OF_MANIFEST_PATH use for manifest file path.
# A line count = 7
def copy_files(a_manifest_files, user_input):
    """Copies the files into the current working directory."""

    a_file_lines = [] # list to store all the lines in manifest file.

    # The manifest file path from the user input
    manifest_file_path = g_NAME_OF_MANIFEST_PATH + "/" + a_manifest_files[user_input - 1]

    # copy the manifest to the Project Tree Destination
    copy_manifest(manifest_file_path)

    # open manifest file as read only.
    manifest_file = open(manifest_file_path, "r")

    # reads the manifes_file line by line and trim white spaces
    for line in manifest_file: # Each line...
        a_file_lines.append(line.strip())

    manifest_file.close() # close the manifes file

    # copies the files from the project leaf tree into our target destination.
    for num in range(1, len(a_file_lines) - 3): # Each file...
        copy_helper(num, a_file_lines, manifest_file_path)

# Copies files from the repo to our target destination.
# Globals: g_NAME_OF_PT_PATH use for project tree path.
# A Line Count = 9
def copy_helper(num, a_file_lines, manifest_file_path):
        """copies files from the repo to our target destination."""

        # Array of a file path that was from the line of manifest.
        a_file_path = a_file_lines[num].split("/")

        # The project tree name for the from the a_file_path
        project_tree_name = a_file_path[a_file_path.index(manifest_file_path.split("_")[1]) + 1]

        # The project_tree_path is the name of the PT destination and the project tree name
        project_tree_path = g_NAME_OF_PT_PATH + "/" + project_tree_name

        create_directory(project_tree_path) # Call create_directory

        # Check if the root has a file
        if (len(a_file_path) - 1) - a_file_path.index(project_tree_name) > 2:

            # get the sub_folder_directory_path from the project_tree_path and the subdirectory name
            sub_folder_directory_path = project_tree_path + "/" + a_file_path[a_file_path.index(project_tree_name) + 1]

            # Call create directory to create the sub_folder_directory
            create_directory(sub_folder_directory_path)

            # Copy the file to the sub directory
            shutil.copy(get_file(a_file_path, manifest_file_path), sub_folder_directory + "/" + a_file_path[-2])

        else:
            # copy the file to the root
            shutil.copy(get_file(a_file_path, manifest_file_path), project_tree_path + "/" + a_file_path[-2])

# Creates a project directory if a path to that directory doesn't exist.
# Globals: None
# A Line Count = 2
def create_directory(project_path):
    """Creates a project directory if a path to that directory doesn't exist."""

    # Check if the path exists
    if not os.path.exists(project_path):
        os.makedirs(project_path) # Make the directory for the path

# Gets the path of the file in our new checked out rep
# Globals: g_NAME_OF_REPO_PATH use for temporary variable
# A Line Count = 5
def get_file(a_file_path, manifest_file_path):
    """Gets the path of the file in our new checked out rep"""

    temp_name_of_repo = g_NAME_OF_REPO_PATH # set temp_name_of_repo

    # set the project tree name index
    project_tree_name_index = a_file_path.index(manifest_file_path.split("_")[1]) + 1

    # project_tree_name_index ... length of a_file_path
    for num in range(project_tree_name_index, len(a_file_path)):

        # Appends to the temp_name_of_repo to create a file path
        temp_name_of_repo = temp_name_of_repo + "/" + a_file_path[num]

    return temp_name_of_repo # return the temp_name_of_repo

# Copies the chose manifest file to the Repo destination.
# Globals: g_NAME_OF_PT_PATH use for creating the child manifest path
# Globals: g_NAME_OF_MANIFEST_PATH use for copying to the manifest folder path
# A Line Count = 8
def copy_manifest(manifest_file_path):
    """Copies the chose manifest file to the Repo destination."""

    a_manifest_file_lines = [] # Declare an Array

    # Declare a child_manifest_path to be the name of the project tree destination and its time.
    child_manifest_path = g_NAME_OF_PT_PATH + "/" + "MANIFEST_" + g_NAME_OF_PT_PATH.split("/")[-1] + "_" + str(datetime.now()) + ".txt"

    # open the manifest file as read only.
    parent_manifest_file = open(manifest_file_path, "r")


    for line in parent_manifest_file: # line...

        # append the lines from the manifest file inside the array
        a_manifest_file_lines.append(line)

    # Close the parent file.
    parent_manifest_file.close()

    # Call the write file function to create the new manifest file.
    write_file(a_manifest_file_lines, child_manifest_path, manifest_file_path)

    # Copy the new manifest file into the manifest file path.
    shutil.copy(child_manifest_path, g_NAME_OF_MANIFEST_PATH)


# A helper function to help write to the new manifest file
# Globals: None
# A Line Count = 5
def write_file(a_manifest_file_lines, child_manifest_path, manifest_file_path):

    # Create and open a file
    child_manifest_file = open(child_manifest_path, "w+")

   # 0 ... length of a_manifest_file_lines - 1
    for index in range(len(a_manifest_file_lines)-1):

        # Write the contents from to the new manifest file from the child manifest.
        child_manifest_file.write(a_manifest_file_lines[index])

    # Write the parent file for the new manifest file.
    child_manifest_file.write("Parent file: " + manifest_file_path.split("/")[-1])

    child_manifest_file.close() # Close the new manifest file.

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

# Gets the list of mainfest files from the manifest folder in the Repo.
# Globals: g_NAME_OF_MANIFEST_PATH to walk the directory for manifest path
# Globals: g_DIRECTORY_AND_FILES_TO_IGNORE for removing ignoring files and directories.
# A line count = 7
def get_manifest():
    """Gets the list of mainfest files."""

    a_manifest_files = [] # list to contain the manifest file names.

    # walk through the manifest folder directory
    for (a_dir_path, a_dir_name, a_file_names) in os.walk(g_NAME_OF_MANIFEST_PATH):
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
