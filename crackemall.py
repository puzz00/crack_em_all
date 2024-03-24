#!usr/bin/python3

# a program to clean up unshadowed Linux password hash files
# it creates a .txt file with a username:hash format and removes the other junk
# the resulting hashes can be attakced using hashcat -m 1800
# a user can use the -c flag to automate the hashcat cracking attempt
# (assuming they have hashcat installed on their OS of course!)

# by puzz00

import optparse
import subprocess
import time

def crack(p, w, path):
    # uses subprocess to execute hashcat commands on the system to crack the hashes
    # the username:hash:cracked_hash file called cracked_hashes.txt will be saved
    # in the same directory as given by the user for the path
    command_one = "hashcat -a 0 -m 1800 --potfile-path=one.pot --username {} {} -O".format(p, w)
    command_two = "hashcat -m 1800 -o {}cracked_hashes.txt --potfile-path=one.pot --username --show {} -O".format(path, p)
    subprocess.call(command_one, shell=True)
    subprocess.call(command_two, shell=True)
    print("\n\n[++]\tCRACKING ENDS!!!")
    time.sleep(3)
    print("\n\n[++]\tThe username:hash:cracked_hash file can be found @ {}cracked_hashes.txt".format(path))
    choice = input("\n\n[**]\tWould you like to see the contents of this file now? Enter y or n --> ")
    if choice.lower().startswith("y"):
        print()
        subprocess.call("cat {}cracked_hashes.txt".format(path), shell=True)
    print("\n\n[**]\tThankyou and goodbye!")

# main    
parser = optparse.OptionParser()
parser.add_option("-c", "--crackemall", action="store", dest="crackemall",
                  help="use -c with a path to a wordlist to use hashcat to (try to) crackemall!")

options, args = parser.parse_args()

hashes = []


unshadowed_file = input("\n\n[**]\tEnter the path to the unshadowed file like so /home/user/unshadowed.txt --> ")
print("\n\n[**]\tPreparing the username:hash file...")
with open(unshadowed_file, "r") as f:
    for line in f:
        new_line = line.split(":") # separates at : and puts pieces into a list
        if len(new_line[1]) == 98: # will only add users who have a hash
            prepared_line = "{}:{}".format(new_line[0], new_line[1]) # combines username:hash
            hashes.append(prepared_line) # adds the cleaned line to the hashes list

path = input("\n\n[**]\tPlease enter the path for where you would like to save the file --> ")
name = input("\n[**]\tPlease enter the name for the new file --> ")
# add a final / if the user does not add one to the path
if path[-1] != "/":
    path = "{}/".format(path)
# create a full path to where the file will be saved
full_path = path + name

with open(full_path, "w") as f:
    # writes the cleaned user:hash lines into a new .txt file for use with hashcat
    for item in hashes:
        f.write(item)
        f.write("\n")
print("\n\n[++]\tComplete! You can find the prepared user:hash file @ {}".format(full_path))

# calls the crack method if the user has specified they would like hashcat to try
# to crack-em-all
if options.crackemall:
    pass_path = options.crackemall
    input("\n\n[**]\tPress enter and let the cracking commence!!!")
    crack(full_path, pass_path, path)






