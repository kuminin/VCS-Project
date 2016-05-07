import os
import shutil
import subprocess
from sys import argv
from datetime import datetime
from create_repo import check_sum
from create_repo import write_hierarchy
from check_out import type_input


import time

g_NAME_OF_REPO = argv[0] + "/repo343"  # Repo Directory Path.

# Manifest Directory Path.
g_NAME_OF_MANIFEST_FOLDER = argv[0] + "/repo343/MANIFEST"

# Project tree source path location
g_NAME_OF_PT_PATH = argv[1]

# A set of files and directories to ignore.
g_DIRECTORY_AND_FILES_TO_IGNORE = set(['.DS_Store', "repo343"])


# Begins the Merge.
# Globals: None
# A Line Count = 5
def merge_interface():
    """Begins the Merge."""

    a_manifest_files = get_manifest() # Gets the list of mainfest files.

    user_input = type_input(a_manifest_files) # Gets user input.

    # Validates the user input to see if it is in range
    while user_input < 1 or len(a_manifest_files) < user_input:
        user_input = type_input(a_manifest_files)

    merge_repo(a_manifest_files, user_input) # Commence Merge.

# Merge the given target file and the manifest repo together.
# Globals: g_NAME_OF_MANIFEST_FOLDER use for creating the manifest path for a given manifest file.
# Globals: g_NAME_OF_PT_PATH use for creating the manifest name for a given project tree location
# A Line Count = 8
def merge_repo(a_manifest_files, user_input):
    """Merge the given target file and the manifest repo together."""

    # the manifest path inside the repo that the user chose.
    repo_manifest_path = g_NAME_OF_MANIFEST_FOLDER + "/" + a_manifest_files[user_input-1]

    # the manifest name for our project tree location.
    manifest_name = "MANIFEST_" + g_NAME_OF_PT_PATH.split("/")[-2] + "_" + str(datetime.now()) + ".txt"

    # path for our new manifest for a given project tree.
    current_manifest_path = target_directory() + manifest_name

    # check for conflict files.
    if check_conflict(repo_manifest_path):

        # create a new manifest file with our conflict files.
        create_manifest(manifest_name, walk_directory(), a_manifest_files[user_input - 1])

        # replaces our current manifest file with a new manifest file
        replace_manifest_file(current_manifest_path, manifest_name)

        # Commence the auto merge.
        call_auto_merge(create_log_file(), manifest_name, a_manifest_files, user_input)
    else:

        # If no conflict files exist, create a new manifest file.
        create_manifest(manifest_name, walk_directory(), a_manifest_files[user_input - 1])


# Replaces the current manifest file with a new one
# Globals: g_NAME_OF_MANIFEST_FOLDER use for removing the current manifest
# A Line Count = 4
def replace_manifest_file(current_manifest_path, manifest_name):
    """Replaces the current manifest file with a new one"""

    # Copies the current manifest file
    shutil.copy(current_manifest_path, create_temp_manifest_path(current_manifest_path))

    # Removes current manifest
    os.remove(current_manifest_path)

    # Removes the manifest located in the repo
    os.remove(g_NAME_OF_MANIFEST_FOLDER + "/" + manifest_name)

    # Renames our new manifest to be the current manifest
    os.rename(create_temp_manifest_path(current_manifest_path), current_manifest_path) #


# Creates the path for the temporary manifest file
# Globals: None
# A Line Count = 4
def create_temp_manifest_path(current_manifest_path):
    """Creates the path for the temporary manifest file."""

    # Creates an array of the current manifest path split by a "/"
    a_temp_manifest_path = current_manifest_path.split("/")

    # Pops the last element of the temp manifest path
    a_temp_manifest_path.pop()

    # appends _TMP to be the last element of the manifest path
    a_temp_manifest_path.append("_TMP")

    # Returns a string of the array joined by a "/"
    return "/".join(a_temp_manifest_path)


# Merges the conflicting files automatically.
# Globals: g_NAME_OF_MANIFEST_FOLDER use for removing the manifest if there is a conflict
# A Line Count = 8
def call_auto_merge(log_file_name, manifest_name, a_manifest_files, user_input):
    """Merges the conflicting files automatically."""

    # Checks if the all the conflicting files have been merged successfully
    if check_all_merge(log_file_name) == 0: #

        # removes the old log file since there are no conflicts
        os.remove(target_directory() + log_file_name)

        # Creates the new manifest file based off our new merged files
        create_manifest(manifest_name, walk_directory(), a_manifest_files[user_input - 1])

    else: # All the conflicting files have not been merged successfully.

        # removes the old log file
        os.remove(target_directory() + log_file_name)

        # creates a new manifest from the log file
        create_manifest(manifest_name, walk_directory(), a_manifest_files[user_input - 1])

        # creates a log file based off the manifest file.
        log_file_name = create_log_file()

        # removes the manifest file since there were conflicts.
        os.remove(target_directory() + manifest_name)

        # removes the manifest file from the repo due to conflicts.
        os.remove(g_NAME_OF_MANIFEST_FOLDER + "/" + manifest_name)


# Will check to see if all conflicting files were merged.
# Globals: None
# A Line Count = 6
def check_all_merge(log_file):
    """Will check to see if all conflicting files were merged."""

    # variable for checking conflict
    conflict = 0

    # Array to hold the path of the conflicting files.
    a_conflict_file_path = []

    # Opens the log file which has all the path for the conflicting files.
    file = open(get_logfile_path(log_file), "r")

    # Each line...
    for line in file:

        # append the line to a_conflict_file_path
        a_conflict_file_path.append(line)

        # check if the length of the conflict files is equal to 3 since MR_, MT_, and MG_
        if len(a_conflict_file_path) == 3:

            # Check if there wasn't any conflict to merge the files.
            if merge_files(a_conflict_file_path) != 0:

                # Set conflict to -1 since there were merging issues.
                conflict = -1

            # Empty our a_conflict_file_path array.
            a_conflict_file_path[:] = []

    # Close the file.
    file.close()

    # Return the conflict variable.
    return conflict


# Gets the log file path for our target project
# Globals: None
# A Line Count = 5
def get_logfile_path(log_file):
    """Gets the log file path for our target project."""

    # Split the target manifest path by "/" into an array.
    a_log_file_path = get_target_manifest().split("/")

    # Pop the last two elements in the log file path
    a_log_file_path.pop()
    a_log_file_path.pop()

    # append the log file name to the array.
    a_log_file_path.append(log_file)

    # return the string path from the array joined by a "/"
    return "/".join(a_log_file_path)


# Mereges the conflict files into a new single file.
# Globals: None
# A Line Count = 4
def merge_files(a_conflict_file_path):
    """Mereges the conflict files into a new single file."""

    # gets the path for the grandpa, repo, and target file.
    grandpa_file = a_conflict_file_path[0].strip()
    repo_file    = a_conflict_file_path[1].strip()
    target_file  = a_conflict_file_path[2].strip()

    # Checks if the conflicting file has been sucessfully merged.
    if subprocess.call(["diff3", "-m", repo_file, grandpa_file, target_file]) == 0:

        # Copies the merged files to the repo
        copy_merge_file_to_repo(create_merged_file(repo_file, grandpa_file, target_file))

        # removes the old conflict files.
        remove_conflict_files(grandpa_file, repo_file, target_file)

        # returns 0 since the merge has been successful.
        return 0

    # returns -1 since the merege was not successful.
    return -1


# Creates a new merged file from the conflict files.
# Globals: None
# A Line Count = 4
def create_merged_file(repo_file, grandpa_file, target_file):
    """Creates a new merged file from the conflict files."""

    # creates an array from the target file path for our new merged file.
    a_target_file_path = target_file.split("/")

    # sets the last element to be the name and the extension
    a_target_file_path[-1] = a_target_file_path[-1].split("_")[-1]

    # opens a new file from the a_target_file_path joined by a "/"
    file = open ("/".join(a_target_file_path), "w+")

    # calls a subprocess to write the mereged output into our file.
    subprocess.call(["diff3", "-m", repo_file, grandpa_file, target_file], stdout = file)

    # close the file.
    file.close()

    # return the array of the merged file path.
    return a_target_file_path


# Creates an Artifact ID for the merged file in our repo.
# Globals: g_NAME_OF_PT_PATH used for getting the project tree name
# Globals: g_NAME_OF_REPO used for creating a temporary repo path.
# A Line Count = 8
def copy_merge_file_to_repo(a_target_file_path):
    # Get check sum for new merged file
    check_sum_name = check_sum("/".join(a_target_file_path))

    # Variable for the name of the project tree.
    project_tree_name = g_NAME_OF_PT_PATH.split("/")[-1]

    # Array of the path for the repo split by a "/"
    a_temp_repo_path = g_NAME_OF_REPO.split("/")

    # variable to check for the project tree name.
    pt_directory_check = False

    # 0 ... length of the a_target_file_path
    for i in range (len(a_target_file_path)):

        # checks to see if the element for a_target_file_path at index i equals the project tree name.
        if(a_target_file_path[i] == project_tree_name):

            # Sets pt_directory_check to be true.
            pt_directory_check = True

        # checks to see if pt_directory_check has been set.
        if(pt_directory_check):

            # append the element for a_target_file_path at index i to the a_temp_repo_path
            a_temp_repo_path.append(a_target_file_path[i])

    # appends the check sum name to the a_temp_repo_path
    a_temp_repo_path.append(check_sum_name)

    # copies the merged file to our repo
    shutil.copy("/".join(a_target_file_path), "/".join(a_temp_repo_path))


# Removes the conflicting files.
# Globals: None
# A Line Count = 3
def remove_conflict_files(grandpa_file, repo_file, target_file):
    os.remove(grandpa_file) # Removes the grandpa file
    os.remove(repo_file) # Removes the repo file
    os.remove(target_file) # removes the target file


# Walks through the current working diretory.
# Globals: g_NAME_OF_CURRENT_DIRECTORY use for walking project tree.
# Globals: g_DIRECTORY_AND_FILES_TO_IGNORE use for ignoring directory and files.
# A line count = 6
def walk_directory():
    """Walks through the current working diretory."""
    a_path_for_files = {} # Map to store list of paths

    # Walk in the given current directory.
    for (a_dir_path, a_dir_name, a_file_names) in os.walk(g_NAME_OF_PT_PATH, topdown = True):

        # get rid of directories that are in the ignore set.
        a_dir_name[:] = [d for d in a_dir_name if d not in g_DIRECTORY_AND_FILES_TO_IGNORE]

        # get rid of files that are in the ignore set.
        a_file_names[:] = [d for d in a_file_names if d not in g_DIRECTORY_AND_FILES_TO_IGNORE]

        a_list_of_files = [] # List to store path of files.

        for file_name in a_file_names: # file_name...

            a_list_of_files.append(file_name) # append files to list.

        a_path_for_files[a_dir_path] = a_list_of_files # Map the list

    return a_path_for_files # return the map of file paths.


# Checks to see if there is any conflicts between merging the files.
# Globals: None
# A Line Count = 5
def check_conflict(repo_manifest_path):
    """Checks to see if there is any conflicts between merging the files."""

    # gets the array of tree path along with the map of tree files.
    a_tree_path, map_tree_file = get_file(get_target_manifest()) #

    # gets the array of repo path along with the map of repo files.
    a_repo_path, map_repo_file = get_file(repo_manifest_path) #

    # gets the array of tree path along with the map of tree files.
    a_grandpa_path, map_grandpa_file = get_file(find_grandpa(repo_manifest_path, False))

    # Copies the non conflicting files to our target project tree.
    copy_non_conflict_files(a_repo_path, map_repo_file, map_tree_file)

    # returns whether or not if there is a conflict.
    return copy_conflict_files(map_tree_file, map_repo_file, map_grandpa_file, a_tree_path, a_repo_path, a_grandpa_path)


# Copies the conlficitng files from our repo to our project tree.
# Globals: None.
# A Line Count = 6
def copy_conflict_files(map_tree_file, map_repo_file, map_grandpa_file, a_tree_path, a_repo_path, a_grandpa_path):
    """Copies the conlficitng files from our repo to our project tree."""

    # Sets initial conflict variable to non since there isn't any.
    conflict = False

    for key in map_tree_file: # key ...

        # Checks if the artifact ID are not equal and if the key is in the map_repo_file
        if key in map_repo_file and map_tree_file[key] != map_repo_file[key]:

            # Create a new conflicting file
            manipulate_file_name(a_tree_path, a_tree_path, key, "MT_")

            # Create a new conflicting file
            manipulate_file_name(a_tree_path, a_repo_path, key, "MR_")

            # Checks to see if the key was in the map_grandpa_file
            if key in map_grandpa_file:

                # Create a new conflicting file
                manipulate_file_name(a_tree_path, a_grandpa_path, key, "MG_")

            # Sets conflict to true since conflict files were made.
            conflict = True

    # Return Conflict
    return conflict


# Copies the non conflicting files from the repo to our project tree.
# Globals: None
# A Line Count = 3
def copy_non_conflict_files(a_repo_path, map_repo_file, map_tree_file):
    """Copies the non conflicting files from the repo to our project tree."""


    for key in map_repo_file: # key...

        # Checks to see if key is in the map_tree_file
        if key not in map_tree_file:

            # Copies the file if the key was not conflicting.
            copy_non_conflict_repo_files(a_repo_path, key)


# Copies the nonconflicting files from the repo files to our proejct tree.
# Globals: None
# A Line Count = 10
def copy_non_conflict_repo_files(a_repo_path, file):
    """Copies the nonconflicting files from the repo files to our proejct tree."""

    # Gets the path for the file that is inside the repo.
    file_path = get_path(a_repo_path, file)

    # Create an empty array to hold path
    a_temp_path = []


    # Sets an array from the file_path that was split by a "/"
    a_temp_repo_path = file_path.split("/")

    # Check if there exists a sub folder.
    if (len(a_temp_repo_path)-1) - a_temp_repo_path.index(g_NAME_OF_PT_PATH.split("/")[-1]) >= 3:

        # pop the last three elements in the temp_repo_path
        a_temp_repo_path.pop()
        a_temp_path.append(a_temp_repo_path.pop())
        a_temp_path.append(a_temp_repo_path.pop())
    else:
        # Pop the last two element in the temporary repo_path
        a_temp_repo_path.pop()
        a_temp_repo_path.pop()

        # finds the project tree owner and sets it to the temp path.
        a_temp_path = find_project_tree_owner(a_temp_repo_path)

    # Copies the non conflicting files to our project tree.
    copy_files(file_path, create_target_file_path(a_temp_path), "") #


# Creates a file path for our target path.
# Globals: None
# A Line Count = 6
def create_target_file_path(a_temp_path):
    """Creates a file path for our target path."""

    # Sets the target path to be the name of the project tree path
    target_path = g_NAME_OF_PT_PATH

    # Checks to see if the temp_path has a length greater than 3 for more directories.
    if len(a_temp_path) >= 2:
        # appends to the target path for the sub directories.
        target_path = target_path + "/" + a_temp_path.pop()

    # Check if the path exists.
    if not os.path.exists(target_path):

        # Create a directory for the target_path.
        os.makedirs(target_path)

    # Checks to see if the a_temp_path length is 0...
    while len(a_temp_path) != 0:

        # Append the last element from the temp_path to our target path.
        target_path = target_path + "/" + a_temp_path.pop()

    # return the target path.
    return target_path


# Find the owner of the project tree path in array form.
# Globals: g_NAME_OF_PT_PATH used for finding the project tree name
# A Line Count = 4
def find_project_tree_owner(a_path):
    """Find the owner of the project tree path in array form."""

    # Sets the project tree name to be the last element from the splitted g_NAME_OF_PT path.
    project_tree_name = g_NAME_OF_PT_PATH.split("/")[-1]

    # sets the temp_path to be an empty array.
    a_temp_path = []

    while True: #...

        # pop the last element from the path and set it to name
        name = a_path.pop()

        # append name to the a_temp_path
        a_temp_path.append(name)

        # check if name equals the project_tree_name
        if name == project_tree_name:

            # break if true.
            break

    # return the a_temp_path
    return a_temp_path


# Creates a new file from the repo into our project tree with a prefix.
# Globals: None
# A Line Count = 8
def manipulate_file_name(a_target_file_path, a_repo_file_path, file, prefix):
    """Creates a new file from the repo into our project tree with a prefix."""

    # Gets the file path from our array of target file path
    target_path = get_path(a_target_file_path, file)

    # Gets the file path from our array of repo file path
    repo_path = get_path(a_repo_file_path, file)

    # Creates an array of file path from the target path
    a_file_path = target_path.split("/")

    # pop the last element since its AID
    a_file_path.pop()

    # join the array of file path
    file_path = "/".join(a_file_path)

    # check if the path already exists b/c duplicate
    if os.path.exists(file_path):

        # remove the file from our project tree
        os.remove(file_path)

    # Copies the file ito our project tree with a prefix.
    copy_files(repo_path, target_path, prefix) #

# gets the path for a file
# Globals: None
# A Line Count = 3
def get_path(certain_file_path, file):
    """gets the path for a file"""

    # Sets an empty string variable
    certain_path = ""

    # 0 ... length(certain_file_path)
    for i in range(len(certain_file_path)):

        # check if a file substring is in the element at index i from certain_file_path
        if file in certain_file_path[i]:

            # set certain_path to be the element at index i from the certain_file_path
            certain_path = certain_file_path[i]

    # return the certain_path
    return certain_path


# creates a file path from our given parameter of an array of file name path
# Globals: g_NAME_OF_REPO used for keeping repo path.
# A Line Count = 3
def append_file_name(a_file_name_path):
    """creates a file path from our given parameter of an array of file name path"""

    # Sets file_path_name variable to be the repo path
    file_path_name = g_NAME_OF_REPO

    # length of array does not equal 0 ...
    while len(a_file_name_path) != 0:

        # appends the popped element from the array to the file_path_name
        file_path_name = file_path_name + "/" + a_file_name_path.pop() #

    # returns the file_path_name
    return file_path_name


# Copies the files from the repo to our project tree with a given prefix.
# Globals: None
# A Line Count = 8
def copy_files(repo_file_path, target_file_path, prefix):
    """Copies the files from the repo to our project tree with a given prefix."""

    # creates an array of file path from our given repo file path
    a_file_path = repo_file_path.split("/")
    print "a_file_path: ", a_file_path, "\n"
    print
    # Sets the file path name to be the path of our given project tree with the file name appended
    file_path_name = append_file_name(find_project_tree_owner(a_file_path)) #
    print "file_path_name: ", file_path_name, "\n"
    print

    print "target_file_path: ", target_file_path, "\n"
    print
    # Checks if the prefix is empty
    if prefix == "":

        # copies the file from our file_path to our project tree
        shutil.copy(file_path_name, target_file_path)

    else: # if the prefix is not empty

        # Create an array of target file path from the splitted target_file_path
        a_target_file_path = target_file_path.split("/")

        # pop the last element since its AID
        a_target_file_path.pop()

        # sets the last element to be the prefix and the name of the file
        a_target_file_path[-1] = prefix + a_target_file_path[-1]

        # creates the new conflict file from repo to project tree
        shutil.copy(file_path_name, "/".join(a_target_file_path))


# Gets the path and the map of files of the given argument
# Globals: None
# A Line Count = 7
def get_file(target_manifest_path):
    """ Gets the path and the map of files of the given argument"""

    # Sets an empty map variable
    files = {}

    # Sets an empty array variable
    path = []

    # opens the argument path location for read only.
    file = open(target_manifest_path, "r")

    for line in file: # line...

        # Check if "/" is in line.
        if "/" in line:

            # Append the path with blank spaces stripped away.
            path.append(line.strip())

            # Map the file name to its artifact id.
            files[line.split("/")[-2]] = line.split("/")[-1].strip()

    # Close the file.
    file.close()

    # Return a tuple of the array of path and the map of files.
    return path, files


# Recursive function to find the grandpa file.
# Globals: g_NAME_OF_MANIFEST_FOLDER used for the parent File Path
# Globals: g_NAME_OF_PT_PATH used to check for the parent file of PT
# A Line Count = 6
def find_grandpa(repo_manifest_path, found):

    # find the parent file
    parentfile = find_parent(repo_manifest_path)

    # set the parent manifest file path
    parentFilePath = g_NAME_OF_MANIFEST_FOLDER + "/" + parentfile

    # Checks if found as base case
    if (found):
        if "null" in parentfile:
            return repo_manifest_path
        else:
            return parentFilePath

    # Checks to see if this is the parent file.
    if g_NAME_OF_PT_PATH.split("/")[-2] in parentfile:

        # find_grandpa with true since the next parent is the grandpa file.
        return find_grandpa(parentFilePath, True)


    else:

        # find_grandpa with false since grandpa is not found
        return find_grandpa(parentFilePath, False)


# Find the parent of a given manifest
# Globals: None
# A Line Count = 4
def find_parent(repo_manifest_path):
    """Find the parent of a given manifest"""

    # Sets an empty string variable
    parentfile = ""

    # Opens the given argument, the manifest path, as read only.
    file = open(repo_manifest_path, "r")

    for line in file: # line...

        # sets parentfile to be the line.
        parentfile = line

    # close the file.
    file.close()

    # return the parent manifest file name.
    return parentfile.split(": ")[1] #


# Gets the path for a project tree target manifest
# Globals: g_NAME_OF_PT_PATH used for creating an array
# A Line Count = 7
def get_target_manifest():
    """Gets the path for a project tree target manifest"""

    # Create an array from g_NAME_OF_PT_PATH split by "/"
    a_split_path = g_NAME_OF_PT_PATH.split("/")

    # Pop the last element
    a_split_path.pop()

    # Create a path variable with an array join by a "/"
    path = "/".join(a_split_path)

    # Walk the path.
    for (a_dir_path, a_dir_name, a_file_name) in os.walk(path):

        # file_name...
        for file_name in a_file_name:

            # Check if file name has substring MANIFEST_
            if "MANIFEST_" in file_name:

                # Appaend that file name to the path.
                path = path + "/" + file_name

        # Break from walking.
        break

    # Return the path of the MANIFEST file
    return path


# Gets the list of mainfest files.
# Globals: g_NAME_OF_MANIFEST_FOLDER.
# A line count = 6
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

    return remove_unneeded_manifest(a_manifest_files) # return the list of file names.


# Removes the manifest files that are not needed to be merged to the project tree.
# Globals: g_NAME_OF_PT_PATH used for getting the parent directory of the project tree.
# A Line Count = 4
def remove_unneeded_manifest(a_manifest_files):

    # Creates an empty array to hold the manifest file names
    a_temp_manifest_files = []

    # Sets the parent directory name
    owner = g_NAME_OF_PT_PATH.split("/")[-2]

    for files in a_manifest_files: # files...

        # Check if the substring owner is not in files
        if owner not in files:

            # Append files to the array.
            a_temp_manifest_files.append(files)


    # Return the array of manifest file names
    return a_temp_manifest_files



# Creates the manifest file for the repo343 directory.
# Globals: g_NAME_OF_MANIFEST_FOLDER use for file path.
# A line count = 5
def create_manifest(manifest_name, directory_list, repo_manifest_file):
    """Creates the manifest file for the repo343 directory."""

    # Sets the file name of MANIFEST to the current datetime.
    MANIFEST = g_NAME_OF_MANIFEST_FOLDER + "/" + manifest_name

    # Create and open manifest file.
    manifest_file = open(MANIFEST, 'w+')

    # Write project tree hierachy to manifest file.
    write_hierarchy(manifest_file, directory_list)

    # Writes the parent file to the manifest
    write_parent(manifest_file, repo_manifest_file)

    # Close manifest file.
    manifest_file.close()

    # Copy manifest file to the Project Tree Folder
    shutil.copyfile(MANIFEST, target_directory() + manifest_name)

# Writes the parent manifest file to the current manifest file.
# Globals: g_NAME_OF_MANIFEST_FOLDER use for getting manifest files.
# A line count = 4
def write_parent(manifest_file, repo_manifest_file):
    """Writes the parent manifest file to the current manifest file."""

    # Sets the current manifest file name
    current_manifest = get_target_manifest().split("/")[-1]

    # Write parent to the manifest file
    manifest_file.write("\nParent file: " + current_manifest)

    # Write the other parent to the manifest file
    manifest_file.write(": " + repo_manifest_file)

    # Remove old manifest file in the Projet Tree
    os.remove(target_directory() + current_manifest)


# Creates the parent directory path for a given project tree directory.
# Globals: g_NAME_OF_PT_PATH used for creating the parent diretory path
# A Line Count = 2
def target_directory():
    """Creates the parent directory path for a given project tree directory."""

    # Sets Empty String Variable
    src = ""

    # For 0 ... length of PT_PATH - 1
    for index in range(len(g_NAME_OF_PT_PATH.split("/")) - 1):

        # Append to src with the element at index and "/"
        src += g_NAME_OF_PT_PATH.split("/")[index] + "/"

    # Return src
    return src


# Writes conlict files to log file and gets log file name.
# GLobals: None.
# A Line Count = 5
def create_log_file():
    """Writes conlict files to log file and gets log file name."""

    # Creates an array for our conflict file paths
    a_conflict_files = get_conflict_file_paths(get_target_manifest())

    # Create variables for the path and name of our log file
    log_file_path, log_file_name = get_log_file_path(get_target_manifest())

    # Open the file given its path to write to it
    file = open(log_file_path, "w+")

    # Loop through concflict files in the array of conflict file paths
    for conflict_file in a_conflict_files:

        # Write the confilct files to the log file
        file.write(conflict_file + "\n")

    # Close the file
    file.close()

    # Return the name of the log file
    return log_file_name


# Creates log file path and log file name.
# Globals: None.
# A Line Count = 6
def get_log_file_path(manifest_path):
    """Creates log file path and log file name."""

    # Set variable log_file_name to name of manifest
    log_file_name = manifest_path.split("/")[-1].split(".")[0]

    # Append  _log.txt to the log file name
    log_file_name += "_log.txt"

    # Creates an array from the manifest path split by "/"
    a_manifest_path = manifest_path.split("/")

    # Pop the last element from the array
    a_manifest_path.pop()

    # Append the log file name to the array
    a_manifest_path.append(log_file_name)

    # Return the log file path and the log file name
    return "/".join(a_manifest_path), log_file_name


# Gets the paths for the conflic files from the manifest
# Globals: None.
# A Line Count = 6
def get_conflict_file_paths(manifest_path):
    """Gets the paths for the conflic files from the manifest"""

    # Creates an empty array
    a_conflict_files = []

    # Opens the manifest file as read only
    file = open(manifest_path, "r")

    # line...
    for line in file:

        # Check if line has MT_, MR_, or MG_
        if ("MT_" in line) or ("MR_" in line) or ("MG_" in line):

            # Creates an array of the line with white spaces stripped split by "/"
            a_path = line.strip().split("/")

            # Pop the last element
            a_path.pop()

            # Append the joined a_path to an array
            a_conflict_files.append("/".join(a_path)) #

    # Close the file
    file.close()

    # Return the list of conflict files
    return a_conflict_files


# Check if the script is ran independently.
if __name__ == "__main__":
    merge_interface()