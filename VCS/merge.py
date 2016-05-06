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


# Begin the merge
# Globals:  gets g_NAME_OF_MANIFEST_FOLDER
def merge_interface():
    a_manifest_files = get_manifest() # Gets the list of mainfest files.

    user_input = type_input(a_manifest_files) # Gets user input.

    # Checks for user input
    while user_input < 1 or len(a_manifest_files) < user_input:
        user_input = type_input(a_manifest_files)

    # print a_manifest_files[user_input-1]
    repo_manifest_path = g_NAME_OF_MANIFEST_FOLDER + "/" + a_manifest_files[user_input-1]
    manifest_name = "MANIFEST_" + argv[1].split("/")[-2] + "_" + str(datetime.now()) + ".txt"
    name_of_current_manifest = target_directory() + manifest_name
    name_of_temp_manifest = name_of_current_manifest.split("/")
    name_of_temp_manifest.pop()
    name_of_temp_manifest.append("_TMP")
    name_of_temp_manifest = "/".join(name_of_temp_manifest)
    if check_conflict(repo_manifest_path):
        create_manifest(manifest_name, walk_directory(), a_manifest_files[user_input - 1])

        log_file_name = create_log_file()
        shutil.copy(name_of_current_manifest, name_of_temp_manifest)

        os.remove(name_of_current_manifest)
        os.remove(g_NAME_OF_MANIFEST_FOLDER + "/" + manifest_name)
        os.rename(name_of_temp_manifest, name_of_current_manifest)

        if auto_merge(log_file_name) == 0:
            os.remove(target_directory() + log_file_name)
            create_manifest(manifest_name, walk_directory(), a_manifest_files[user_input - 1])
        else:
            os.remove(target_directory() + log_file_name)
            create_manifest(manifest_name, walk_directory(), a_manifest_files[user_input - 1])

            log_file_name = create_log_file()
            os.remove(target_directory() + manifest_name)
            os.remove(g_NAME_OF_MANIFEST_FOLDER + "/" + manifest_name)
    else:
        create_manifest(manifest_name, walk_directory(), a_manifest_files[user_input - 1])


def auto_merge(log_file):
    conflict = 0

    file = open(auto_helper(), "r")
    a_conflict_file_path = []
    for line in file:
        print line
        print len(a_conflict_file_path)
        a_conflict_file_path.append(line)
        if len(a_conflict_file_path) == 3:
            if merge_files(a_conflict_file_path) != 0:
                conflict = -1
            a_conflict_file_path[:] = []
    file.close()
    return conflict

def auto_helper():
    log_file_path = target_manifest().split("/")
    log_file_path.pop()
    log_file_path.pop()
    log_file_path.append(log_file)
    log_file_path = "/".join(log_file_path)
    return log_file_path

def merge_files(a_conflict_file_path):
    grandpa_file = a_conflict_file_path[0].strip()
    repo_file = a_conflict_file_path[1].strip()
    target_file = a_conflict_file_path[2].strip()
    if subprocess.call(["diff3", "-m", repo_file, grandpa_file, target_file]) == 0:
        target_file_path = target_file.split("/")
        target_file_path[-1] = target_file_path[-1].split("_")[-1]
        file = open ("/".join(target_file_path), "w+")
        subprocess.call(["diff3", "-m", repo_file, grandpa_file, target_file], stdout = file)
        file.close()

        # Get check sum for new merged file
        check_sum_name = check_sum("/".join(target_file_path))
        project_tree_name = g_NAME_OF_PT_PATH.split("/")[-1]
        temp_repo_path = g_NAME_OF_REPO.split("/")
        pt_directory_check = False

        for i in range (len(target_file_path)):
            if(target_file_path[i] == project_tree_name):
                pt_directory_check = True

            if(pt_directory_check):
                temp_repo_path.append(target_file_path[i])


        temp_repo_path.append(check_sum_name)
        shutil.copy("/".join(target_file_path), "/".join(temp_repo_path))

        os.remove(grandpa_file)
        os.remove(repo_file)
        os.remove(target_file)
        return 0
    else:
        return -1

# Walks through the current working diretory.
# Globals: g_NAME_OF_CURRENT_DIRECTORY use for walking project tree.
# Globals: g_DIRECTORY_AND_FILES_TO_IGNORE use for ignoring directory and files.
# A line count = 9
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

        for file_name in a_file_names:

            a_list_of_files.append(file_name) # append files to list.

        a_path_for_files[a_dir_path] = a_list_of_files # Map the list

    return a_path_for_files # return the map of file paths.

def check_conflict(repo_manifest_path):
    conflict = False
    tree_path, tree_file = get_file(target_manifest())
    repo_path, repo_file = get_file(repo_manifest_path)
    grandpa_path, grandpa_file = get_file(find_grandpa(repo_manifest_path, False))
    for key in tree_file:
        if key in repo_file and tree_file[key] != repo_file[key]:
            manipulate_files(tree_path, tree_path, key, "MT_")
            manipulate_files(tree_path, repo_path, key, "MR_")
            if key in grandpa_file:
                manipulate_files(tree_path, grandpa_path, key, "MG_")
            conflict = True

    for key in repo_file:
        if key not in tree_file:
            manipulate_repo_files(repo_path, key)

    return conflict

def manipulate_repo_files(repo_file_path, file):
    repo_path = get_path(repo_file_path, file)
    temp_repo_path = repo_path.split("/")
    temp_repo_path.pop()
    project_tree_name = g_NAME_OF_PT_PATH.split("/")[-1]
    temp_path = []
    while True:
        name = temp_repo_path.pop()
        temp_path.append(name)
        if name == project_tree_name:
            break

    target_path = g_NAME_OF_PT_PATH

    if len(temp_path) >= 3:
        targe_path = target_path + "/" + temp_path.pop()
        target_path = target_path + "/" + temp_path.pop()

    if not os.path.exists(target_path):
        os.makedirs(target_path)

    while len(temp_path) != 0:
        target_path = target_path + "/" + temp_path.pop()
    print repo_path
    print target_path
    copy_files(repo_path, target_path, "")


def manipulate_files(target_file_path, repo_file_path, file, prefix):
    target_path = get_path(target_file_path, file)
    repo_path = get_path(repo_file_path, file)
    file_path = target_path.split("/")
    file_path.pop()
    file_path = "/".join(file_path)


    if os.path.exists(file_path):
        os.remove(file_path)


    copy_files(repo_path, target_path, prefix)

def get_path(certain_file_path, file):
    certain_path = ""
    for i in range(len(certain_file_path)):
        if file in certain_file_path[i]:
            certain_path = certain_file_path[i]
    return certain_path


def copy_files(repo_file_path, target_file_path, prefix):
    a_file_path = repo_file_path.split("/")
    a_file_name_path = []
    while True:
        name_path = a_file_path.pop()
        a_file_name_path.append(name_path)
        if name_path == g_NAME_OF_PT_PATH.split("/")[-1]:
            break
    file_path_name = g_NAME_OF_REPO

    while len(a_file_name_path) != 0:
        file_path_name = file_path_name + "/" + a_file_name_path.pop()

    if prefix == "":
        shutil.copy(file_path_name, target_file_path)
    else:
        target_file_path = target_file_path.split("/")
        target_file_path.pop()
        target_file_path[-1] = prefix + target_file_path[-1]
        shutil.copy(file_path_name, "/".join(target_file_path))

def get_file(target_manifest_path):
    file = open(target_manifest_path, "r")
    files = {}
    path = []
    for line in file:
        if "/" in line:
            path.append(line.strip())
            files[line.split("/")[-2]] = line.split("/")[-1].strip()
    file.close()
    return path, files


def find_grandpa(repo_manifest_path, found):
    parentfile = find_parent(repo_manifest_path)
    parentFilePath = g_NAME_OF_MANIFEST_FOLDER + "/" + parentfile
    if (found):
        if "null" in parentfile:
            return repo_manifest_path
        else:
            return parentFilePath
    if g_NAME_OF_PT_PATH.split("/")[-2] in parentfile:
        return find_grandpa(parentFilePath, True)
    else:
        return find_grandpa(parentFilePath, False)

def find_parent(repo_manifest_path):
    file = open(repo_manifest_path, "r")
    parentfile = ""
    for line in file:
        parentfile = line
    file.close()
    return parentfile.split(": ")[1]

def rename_files(prefix, path_of_manifest_file):
    file = path_of_manifest_file

def target_manifest():
    a_split_path = g_NAME_OF_PT_PATH.split("/")
    a_split_path.pop()
    path = "/".join(a_split_path)

    for (a_dir_path, a_dir_name, a_file_name) in os.walk(path):
        for file_name in a_file_name:
            if "MANIFEST_" in file_name:
                path = path + "/" + file_name
        break
    return path


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

# Removes the manifest files that the user can
def remove_target(a_manifest_files):
    a_temp_manifest_files = []
    owner = g_NAME_OF_PT_PATH.split("/")[-2]

    for files in a_manifest_files:
        if owner not in files:
            a_temp_manifest_files.append(files)

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
# A line count = 5
def write_parent(manifest_file, repo_manifest_file):
    """Writes the parent manifest file to the current manifest file."""

    current_manifest = target_manifest().split("/")[-1]
    # The latest manifest will be written as the parent.
    manifest_file.write("\nParent file: " + current_manifest)
    manifest_file.write(": " + repo_manifest_file)

    # Remove old manifest file in the Projet Tree
    os.remove(target_directory() + current_manifest)



def target_directory():
    src = ""
    for x in range(len(g_NAME_OF_PT_PATH.split("/")) - 1):
        src += g_NAME_OF_PT_PATH.split("/")[x] + "/"
    return src

def create_log_file():
    manifest_path = target_manifest()
    a_conflict_files = []
    file = open(manifest_path, "r")

    for line in file:
        if ("MT_" in line) or ("MR_" in line) or ("MG_" in line):
            path = line.strip().split("/")
            path.pop()
            a_conflict_files.append("/".join(path))

    file.close()

    manifest_file_name = manifest_path.split("/")[-1].split(".")[0]
    manifest_file_name += "_log.txt"

    a_manifest_path = manifest_path.split("/")
    a_manifest_path.pop()

    a_manifest_path.append(manifest_file_name)
    log_path = "/".join(a_manifest_path)
    file = open(log_path, "w+")

    for conflict_file in a_conflict_files:
        file.write(conflict_file + "\n")

    file.close()

    return manifest_file_name





# Check if the script is ran independently.
if __name__ == "__main__":
    merge_interface()