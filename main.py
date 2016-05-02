from sys import argv
from sys import path
from os import getcwd

if __name__ == "__main__":
    commands_allowed = set(["create_repo", "check_in", "check_out", "help", "merge"])
    if argv[1] == "help":
        print "python main.py create_repo [Project Tree Source Location] [Repo Destination]"
        print "python main.py check_in [Project Tree Source Location] [Repo Destination]"
        print "python main.py check_out [Repo Source Location] [Project Tree Destination]"
        print "python main.py merge [Repo Source Location] [Project Tree Destination]"
    elif len(argv) < 4:
        print "Please type python main.py help to show allowed commands"
    else:
        path.insert(0, getcwd() + "/VCS")
        argument = argv[1]
        if argument not in commands_allowed:
            print "The command " + argument + " is not allowed."
            print "Allowed arguments are: " + commands_allowed
        else:
            argv = [argv[2], argv[3]]
            execfile("VCS/" + argument + ".py")
