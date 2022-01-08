import bashlex
import copy
import os
import re

command_filter = "C "
start_filter = "S"

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

scientist_parsed = []
experienced_parsed = []
non_programmers_parsed = []
novice_parsed = []

for i in range(len(scientists_files)):
    scientists_files[i] = scientists_dir + scientists_files[i]
    
for i in range(len(experienced_files)):
    experienced_files[i] = experienced_dir + experienced_files[i]

for i in range(len(non_programmers_files)):
    non_programmers_files[i] = non_programmers_dir + non_programmers_files[i]

for i in range(len(novice_files)):
    novice_files[i] = novice_dir + novice_files[i]


for file_path in scientists_files:
    file1 = open(file_path, encoding="ISO-8859-1")
    lines = file1.readlines()
    
    for line in lines:
        if re.match(command_filter, line) is not None:
            scientist_commands.append(line[2:-1])
            try:
                parts = bashlex.parse(scientist_commands[-1])
                scientist_parsed.append(parts[0].dump())
            except Exception as inst:
                pass


for file_path in experienced_files:
    file1 = open(file_path, encoding="ISO-8859-1")
    lines = file1.readlines()
    
    for line in lines:
        if re.match(command_filter, line) is not None:
            experienced_commands.append(line[2:-1])
        try:
            parts = bashlex.parse(experienced_commands[-1])
            experienced_parsed.append(parts[0].dump())
        except Exception as inst:
            pass

for file_path in non_programmers_files:
    file1 = open(file_path, encoding="ISO-8859-1")
    lines = file1.readlines()
    
    for line in lines:
        if re.match(command_filter, line) is not None:
            non_programmers_commands.append(line[2:-1])
        try:
            parts = bashlex.parse(non_programmers_commands[-1])
            non_programmers_parsed.append(parts[0].dump())
        except Exception as inst:
            pass
            
for file_path in novice_files:
    file1 = open(file_path, encoding="ISO-8859-1")
    lines = file1.readlines()
    
    for line in lines:
        if re.match(command_filter, line) is not None:
            novice_commands.append(line[2:-1])
        try:
            parts = bashlex.parse(novice_commands[-1])
            novice_parsed.append(parts[0].dump())
        except Exception as inst:
            pass

# TODO: add logic so each session (between starts) is in its own list
# DRAFT
def parse_commands(command_list, parsed_list, files_list):
    for file_path in files_list: 
        file1 = open(file_path, encoding="ISO-8859-1")
        lines = file1.readlines()

        for line in lines:
            if re.match(command_filter, lines) is not None:
                command_list.append(line[2:-1])
            try:
                parts = bashlex.parse(command_list[-1])
                parsed_list.append(parts[0].dump())
            except Exception as inst:
                pass

    return parsed_list
            
