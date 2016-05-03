import sys
import os

if __name__ == "__main__":
    commands_allowed = set(["create_repo", "check_in", "check_out", "help", "merge"])
    if sys.argv[1] == "help":
        print "python main.py create_repo [Project Tree Source Location] [Repo Destination]"
        print "python main.py check_in [Project Tree Source Location] [Repo Destination]"
        print "python main.py check_out [Repo Source Location] [Project Tree Destination]"
        print "python main.py merge [Repo Source Location] [Project Tree Source Location]"
    elif len(sys.argv) < 4:
        print "Please type python main.py help to show allowed commands"
    else:
        sys.path.insert(0, os.getcwd() + "/VCS")
        argument = sys.argv[1]
        if argument not in commands_allowed:
            print "The command " + argument + " is not allowed."
            print "Allowed arguments are: " + commands_allowed
        else:
            sys.argv = [sys.argv[2], sys.argv[3]]
            execfile("VCS/" + argument + ".py")
