### VCS-Project
* Author: Kumin In and Nick Saikaly
  * Github: @kuminin and @nsaikaly
  * Team: NKX
  * Contact Info: kumin.in1@gmail.com
  * Contact Info: nsaikaly12@gmail.com
* CECS 343 - 07/08
* Project Part 3

### Introduction
This is the third part of our VCS (Version Control System) project. In this project part, we add the ability to merge two project trees. Note that we already have a natural branching effect due to check- out (to a new project tree) coupled with tracking its Mom manifest.
The merge ability lets the user, merge a project tree that is already in the repo (as represented by a manifest file) into a project tree outside the repo.
For example, Fred can merge Jack's changes (checked-in from Jack's project tree) that are in the repo into Fred's current project tree. If the merge succeeds (merge software is only able to handle simple file differences) then Fred can eyeball the merge (maybe also run some tests) and check-in his resulting project tree.


### External Requirements:
User must have a Linux OS or Mac OS running with diff3 available for merge.

### Build, Installation, and Setup.
Copy this VCS-Project directory anywhere you'd wish.

We are assuming that the user knows where the repo directories and the project directories are at all timtes, checked_in must be called before merging, you cannot check_out to a directory that contains a "MANIFEST_" file, and we are assuming the main success path for this given project.

### Usage
#### Create_Repo
##### To create a repo for your project:
Assuming that you have the VCS-Project directory in Downloads and you want to create a repo for a given project tree...
```
python ~/Downloads/VCS-Project/main.py create_repo ~/Desktop/home/Fred/PT ~/Desktop
```
The user should not type / at the end of all arguments.

#### Check_In
##### To Check In a Project:
Assuming that you have changed the file in Fred and you want to check in...
```
python ~/Downloads/VCS-Project/main.py check_in ~/Desktop/home/Fred/PT ~/Desktop
```
The user should not type / at the end of all arguments.

#### Check_Out
##### To Check Out a Project to a new destination:
Assuming that you created a new directory of Jack in the home directory...
```
python ~/Downloads/VCS-Project/main.py check_out ~/Desktop ~/Desktop/home/Jack
```
The user should not type / at the end of all arguments and the destination is an empty directory that doesn't have a "MANIFEST_" file.

#### Merge
##### To Merge a Project:
Assuming that you checked in the directory you are merging...
```
python ~/Downloads/VCS-Project/main.py merge ~/Desktop ~/Desktop/home/Fred/PT
```
The user should not type / at the end of all arguments

If you would like to see auto merge in action, without conflicts, please run the following and make sure the VCS-Project is in the Downloads Directory:
```
python ~/Downloads/VCS-Project/main.py merge ~/Downloads/Sample/VCS-Project ~/Downloads/NonConflict/Fred/PT
```
When asked for input please type in 3 and press enter.

If you would like to see auto merge in action, without conflicts, please run the following and make sure the VCS-Project is in the Downloads Directory:
```
python ~/Downloads/VCS-Project/main.py merge ~/Downloads/Sample/VCS-Project ~/Downloads/Conflict/Fred/PT
```
When asked for input please type in 2 and press enter.

### Extra Features
None

### Bugs
We are still not sure if the script will run on Windows OS.

There is a known issue with Ubuntu, am not sure with all linux platforms, where it creates a back directory inside the repo. This directory will have a "~" before the directory name.

Simple hierarchys of a given project tree will work, however, a complex hierarcy will not.

Working Example:
```
Fred
|-------PT
        |-------hello.txt
        |-------world.txt
        |-------java.fool
        |-------FA
        |       |-------h.txt
        |-------FB
        |       |-------Car.txt
        |       |-------Bye.txt
        |-------FC
                |-------Hello.java
```

Not Working Example:
```
Fred
|-------PT
        |-------FA
        |       |-------Have.txt
        |       |-------FD
        |       |       |-------A.txt
        |-------FB
        |       |-------Wonderful.txt
        |       |-------Summer.txt
        |       |-------FF
        |       |       |-------Professor.txt
        |       |       |-------Siska.txt
        |-------FC
                |-------Good_Bye_It_was_fun.java
```