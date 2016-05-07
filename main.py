import sys
import os

if __name__ == "__main__":

    # Set of commands allowed
    commands_allowed = set(["create_repo", "check_in", "check_out", "help", "merge"])

    # Check if user argument is help
    if sys.argv[1] == "help":
        print "python main.py create_repo [Project Tree Source Location] [Repo Destination]"
        print "python main.py check_in [Project Tree Source Location] [Repo Destination]"
        print "python main.py check_out [Repo Source Location] [Project Tree Destination]"
        print "python main.py merge [Repo Source Location] [Project Tree Source Location]"

    # Check if system argument length is less than four
    elif len(sys.argv) < 4:
        print "Please type python main.py help to show allowed commands"
    else:

        # insert python files in VCS for import
        sys.path.insert(0, os.getcwd() + "/VCS")

        # Set the argument to the second argument in command line
        argument = sys.argv[1]

        # Check if argument is not in the allowed commands
        if argument not in commands_allowed:
            print "The command " + argument + " is not allowed."
            print "Allowed arguments are: " + commands_allowed

        else: # Argument was in allowed commands

            # Set the arguments to be the third and fourth command line arguments
            sys.argv = [sys.argv[2], sys.argv[3]]

            # Execute the file
            execfile("VCS/" + argument + ".py")
