import bashlex
import os
import re
import copy
from tqdm import tqdm

re_command_filter = "C"
re_error_filter = "X"
re_start_filter = "S" 
re_pipe_filter = ".*\\|.*"

scientists_dir = "./unix-data/computer-scientists/"
experienced_dir = "./unix-data/experienced-programmers/"
non_programmers_dir = "./unix-data/non-programmers/"
novice_dir = "./unix-data/novice-programmers/"

class Parser:
    def __init__(self):

        self.scientists_files = os.listdir(scientists_dir)
        self.experienced_files = os.listdir(experienced_dir)
        self.non_programmers_files = os.listdir(non_programmers_dir)
        self.novice_files = os.listdir(novice_dir)

        for i in range(len(self.scientists_files)):
            self.scientists_files[i] = scientists_dir + self.scientists_files[i]

        for i in range(len(self.experienced_files)):
            self.experienced_files[i] = experienced_dir + self.experienced_files[i]

        for i in range(len(self.non_programmers_files)):
            self.non_programmers_files[i] = non_programmers_dir + self.non_programmers_files[i]

        for i in range(len(self.novice_files)):
            self.novice_files[i] = novice_dir + self.novice_files[i]

        self.scientists_commands = self.parse_commands(self.scientists_files)
        self.experienced_commands = self.parse_commands(self.experienced_files)
        self.non_programmers_commands = self.parse_commands(self.non_programmers_files)
        self.novice_commands = self.parse_commands(self.novice_files)

    def parse_commands_per_session(self, files_list):
        parsed_list = []

        for file_path in tqdm(files_list):
            file = open(file_path, encoding="ISO-8859-1")
            lines = file.readlines()

            parsed_sublist = []

            for line in range(len(lines)):
                if re.match(re_start_filter, lines[line]) is not None:
                    if len(parsed_sublist) != 0:
                        parsed_list.append(copy.deepcopy(parsed_sublist))
                    
                    parsed_sublist = []
                
                if re.match(re_command_filter, lines[line]) is not None:
                    parsed_sublist.append(lines[line][2:-1])

                    # check if valid command
                    try:
                        parts = list(bashlex.split(parsed_sublist[-1]))
                    except Exception as inst:
                        parsed_sublist.pop(-1)
        
        return parsed_list

    def parse_commands(self, files_list):
        parsed_list = []

        for file_path in tqdm(files_list):
            file = open(file_path, encoding="ISO-8859-1")
            lines = file.readlines()

            for line in range(len(lines)):
                if re.match(re_command_filter, lines[line]) is not None:
                    parsed_list.append(lines[line][2:-1])

                    try:
                        list(bashlex.split(parsed_list[-1]))
                    except:
                        parsed_list.pop(-1)
        
        return parsed_list

    def parse_commands_into_subsets(self, parsed_list, subset_size):
        filter_escaped = lambda x: (x and x.isprintable())
        parsed_list = list(filter(filter_escaped, parsed_list))
        
        parsed_subsets = []

        for i in range(0, len(parsed_list), subset_size):
            parsed_subsets.append(parsed_list[i:i+subset_size])

        filter_empty = lambda x: (x is not None)
        parsed_subsets = list(filter(filter_empty, parsed_subsets))
        
        return parsed_subsets

    
    def filter_commands_with_pipe(self, parsed_list):
        pipe_regex = re.compile(re_pipe_filter)

        return list(filter(pipe_regex.match, parsed_list))

    def expand_piped_commands(self, parsed_list):
        parsed_pipe_list = []
        parsed_pipe_sublist = []
        # change from foo b/c foo is used a lot
        output_redirection = " > pipetemp "
        input_redirection = " < pipetemp"
        
        for command in parsed_list:
            split_command = command.split('|')
            
            for i in range(len(split_command)):
                if i % 2 == 0:
                    parsed_pipe_sublist.append(split_command[i].strip() + output_redirection)
                else:
                    substr = '>'

                    if substr in split_command[i]:
                        idx = split_command[i].index(substr)
                        split_command[i] = split_command[i][:idx] + input_redirection + split_command[i][idx:]
                        parsed_pipe_sublist.append(split_command[i].strip())
                    else:
                        parsed_pipe_sublist.append(split_command[i].strip() + input_redirection)

            parsed_pipe_list.append(copy.deepcopy(parsed_pipe_sublist))
            parsed_pipe_sublist = []


        return parsed_pipe_list

    def replace_args(self, parsed_list):
        filter_escaped = lambda x: (x and x.isprintable())
        parsed_list = list(filter(filter_escaped, parsed_list))

        parsed_list = [i for i in parsed_list if not re.compile(re_pipe_filter).match(i)]

        parsed_list_replaced = []
        arg_replacements = ["$" + str(i) for i in range(100)]

        for command in range(len(parsed_list)):
            command_split = parsed_list[command].split()
            arg_counter = 0

            for i in range(1, len(command_split)):
                if not command_split[i].startswith("-"):
                    command_split[i] = arg_replacements[arg_counter]
                    arg_counter += 1
            
            parsed_list_replaced.append(' '.join(command_split))

        return parsed_list_replaced
