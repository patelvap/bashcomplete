import bashlex
import os
import re

re_command_filter = "C"
re_error_filter = "X"
re_start_filter = "S" 

scientists_dir = "./unix-data/computer-scientists/"
experienced_dir = "./unix-data/experienced-programmers/"
non_programmers_dir = "./unix-data/non-programmers/"
novice_dir = "./unix-data/novice-programmers/"

scientists_files = os.listdir(scientists_dir)
experienced_files = os.listdir(experienced_dir)
non_programmers_files = os.listdir(non_programmers_dir)
novice_files = os.listdir(novice_dir)

scientist_commands = []
experienced_commands = []
non_programmers_commands = []
novice_commands = []

class Parse:
    def __init__(self):
        for i in range(len(scientists_files)):
            scientists_files[i] = scientists_dir + scientists_files[i]

        for i in range(len(experienced_files)):
            experienced_files[i] = experienced_dir + experienced_files[i]

        for i in range(len(non_programmers_files)):
            non_programmers_files[i] = non_programmers_dir + non_programmers_files[i]

        for i in range(len(novice_files)):
            novice_files[i] = novice_dir + novice_files[i]

    