import bashlex
import os
import re
import itertools
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
                    if lines[line].startswith("alias"):
                        continue

                    parsed_sublist.append(lines[line][2:-1])

                    # check if valid command
                    try:
                        bashlex.parse(parsed_sublist[-1])
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

                    if parsed_list[-1].startswith("alias"):
                        parsed_list.pop(-1)
                        continue

                    if parsed_list[-1].endswith("&"):
                        parsed_list[-1] = parsed_list[-1][:-1]

                    try:
                        bashlex.parse(parsed_list[-1])
                    except Exception as inst:
                        parsed_list.pop(-1)
        
        return parsed_list

    def parse_commands_into_subsets(self, parsed_list, subset_size):
        filter_escaped = lambda x: (x and x.isprintable())
        parsed_list = list(filter(filter_escaped, parsed_list))
        
        parsed_subsets = []

        for i in range(0, len(parsed_list)):
            if i + subset_size < len(parsed_list):
                parsed_subsets.append(parsed_list[i:i+subset_size])

        filter_empty = lambda x: (x is not None)
        parsed_subsets = list(filter(filter_empty, parsed_subsets))
        
        return parsed_subsets

    def parse_commands_into_subsets_sliding_window(self, parsed_list, subset_size):
        parsed_subsets = []

        for session in parsed_list:
            for i in range(3, subset_size + 1):
                parsed_subsets.append(self.parse_commands_into_subsets(session, i))

        return parsed_subsets

    
    def filter_commands_with_pipe(self, parsed_list):
        pipe_regex = re.compile(re_pipe_filter)

        return list(filter(pipe_regex.match, parsed_list))

    def expand_piped_commands(self, parsed_list):
        parsed_pipe_list = []
        parsed_pipe_sublist = []
        # change from foo b/c foo is used a lot
        output_redirection = " > input_pipetemp"
        input_redirection = " < output_pipetemp"
        substr = '>'
        
        for command in parsed_list:
            split_command = command.split('|')
            
            for i in range(len(split_command)):
                if i == 0: 
                    parsed_pipe_sublist.append(split_command[i].strip() + output_redirection)
                elif i + 1 == len(split_command):
                    parsed_pipe_sublist.append(split_command[i].strip() + input_redirection)
                else:
                    if substr in split_command[i]:
                        idx = split_command[i].index(substr)
                        split_command[i] = split_command[i][:idx] + input_redirection + split_command[i][idx:] + output_redirection
                        parsed_pipe_sublist.append(split_command[i].strip())
                    else:
                        parsed_pipe_sublist.append((split_command[i].strip() + input_redirection + output_redirection).strip())

            parsed_pipe_list.append(copy.deepcopy(parsed_pipe_sublist))
            parsed_pipe_sublist = []


        return parsed_pipe_list

    def replace_args(self, parsed_list, pipes=False):
        filter_escaped = lambda x: (x and x.isprintable())
        parsed_list = list(filter(filter_escaped, parsed_list))

        parsed_list_replaced = []

        arg_replacements = ["$" + str(i) for i in range(100)]
        arg_counter = 0
        arg_dict = {}

        exclude_chars = set(['|', '<', '>'])

        for command in range(len(parsed_list)):
            command_split = parsed_list[command].split()
            if not pipes:
                arg_counter = 0

            for i in range(1, len(command_split)):
                if not command_split[i].startswith("-") and command_split[i] not in exclude_chars:
                    command_split_by_extension = command_split[i].split(".")

                    if arg_dict.get(command_split_by_extension[0]) is None:
                        arg_dict[command_split_by_extension[0]] = arg_replacements[arg_counter]
                        command_split_by_extension[0] = arg_replacements[arg_counter]
                        arg_counter += 1
                    else:
                        command_split_by_extension[0] = arg_dict[command_split_by_extension[0]]
                    
                    command_split[i] = '.'.join(command_split_by_extension)
            
            parsed_list_replaced.append(' '.join(command_split))


        return parsed_list_replaced

    def replace_args_nested(self, parsed_list):
        parsed_list_replaced = []

        for session in parsed_list:
            for command in session:
                parsed_list_replaced.append(self.replace_args(command))

        return parsed_list_replaced

    def replace_arg_pipes(self, parsed_list):

        parsed_list_replaced = []
        arg_replacements = ["$" + str(i) for i in range(100)]

        arg_dict = {}

        for command in range(len(parsed_list)):
            if parsed_list[command].endswith("&"):
                parsed_list[command] = parsed_list[command][:-1]

            command_split = parsed_list[command].split()

            arg_counter = 0

            for i in range(1, len(command_split)):
                if command_split[i] == "|":
                    pass

                elif not command_split[i].startswith("-") and not command_split[i-1] == '|' and not command_split[i] == '&':
                    #replace only file name, not file extension

                    command_split_by_extension = command_split[i].split(".")

                    if arg_dict.get(command_split_by_extension[0]) is None:
                        command_split_by_extension[0] = arg_replacements[arg_counter]
                        arg_dict[command_split_by_extension[0]] = arg_replacements[arg_counter]
                        arg_counter += 1
                    else:
                        command_split_by_extension[0] = arg_dict[command_split_by_extension[0]]
                    
                    command_split[i] = ''.join(command_split_by_extension)

                if command_split[i-1] == '|':
                    arg_counter = 0
            
            parsed_list_replaced.append(' '.join(command_split))

        return parsed_list_replaced

    def replace_arg_expanded_pipe(self, parsed_pipe_list):
        parsed_list_replaced = []

        for parsed_list in parsed_pipe_list:
            parsed_list_replaced.append(self.replace_args(parsed_list, pipes=True))

        return parsed_list_replaced

"""
3/24

adjust fuzzy threshold (lower weight) / play around with frequencies

5th command after 4th should be 90% accurate -> Not possible, path in graph doesn't exist
    look at examples of successes and failures
    incorrect proportion very high, so maybe correct 
        next command not frequent enough

show successes and failures to describe low accuracy

Do this first
if chain of x or more commands the same then delete it 
    or subsequence repeated

need examples of non repeated command examples in paper

print out frequencies when traversing down graph, look at average frequency 
    going down graph

look at why 2 from 1 is ~80% correct in 15 not 5 but ~67 in 5

get data on printing top 3 results
    intuitively doing sequence once, predicting is hard since infrequent
"""

"""
3/21

Predict x+1 for 1..n rather than full command, so predict next command, not just fifth.

Debug why high results, not just for colearning. Play around with fuzzy match score.

Print out graph of one node e.g. `cd` to save to see graph

Print out tree traversed when giving prediction and frequencies -> maybe return top n frequencies
    - ['cd $0' -> freq, 'cd $0' -> freq, 'examples_vax -> freq....]
    - idea how often things repeat to understand user behavior

Leave one out/Colearning method
    - Using 29/30 people's commands to predict 30/30 person's command

992 Paper:
    - Focus paper on this
    - Get stable results out and create PowerPoint with new results and updated algorithm
    - Write down algorithm
"""

"""
3/7

DONE:
If same file name appears multiple places -> give same $arg
    - map arg to $arg in dict  

Don't do anymore - time constraint
Use all command chains from command 1..n and use all those chains to predict
    - Like VisComplete where you can predict entire command chain from first command
    - Think of programmer that doesn't want to type too much and uses predictions mainly

Print out graph of one node e.g. `cd` to save to see graph

Print out tree traversed when giving prediction and frequencies -> maybe return top n frequencies
    - ['cd $0' -> freq, 'cd $0' -> freq, 'examples_vax -> freq....]
    - idea how often things repeat to understand user behavior

Figure out how to deal with repetitions

Leave one out/Colearning method
    - Using 29/30 people's commands to predict 30/30 person's command

Probably won't do unless time -> results + ppt first
    - Refactor accuracy into .py file and do colearning on different .ipynb

992 Paper:
    - Focus paper on this
    - Get stable results out and create PowerPoint with new results and updated algorithm
    - Write down algorithm
"""

"""
3/3

DONE: first 5 first 4 first 3 first 2 then increment position

Sort of Done: if sequence only comes once then remove it

DONE: reduce size by certain amount

DONE: most common by session -> looks meh
    maybe remove sequences that happen only once
    see if things succeeded in same session

DONE (have files): how far command sequence occurs in same user and other users 
    - map reduce command subsets by user and compare 

DONE: check how often correct solution is in top 5 and top 15
    - example of something matching not in top 5 but in top 15

DONE: print out first ~100 correct predictions to see how generous predictions are

figure out what got repeated each time to see what's correct or not
"""

"""
2/28

Too Computationally Expensive/Intractable: subsets of size 2..n
DONE: shuffle subsets -> save test and train sets

which commands repeated and not repeated

DONE: pprint out graph, training, and test set somehow to see where fails are coming from 
look for repetitions 
    - make sure graph consistent with train and test set
    - explainable AI

want to know what didn't work but also what worked
    - DONE: save logs to file

DONE: (i think) fix pipe codes

DONE: fraction of time did not predict
when did have a prediction, what accuracy was - https://en.wikipedia.org/wiki/Sensitivity_and_specificity
"""

"""
2/21

print out when not matching
be able to look up graph -> for pipes -> and trace through not matching

create example of things working and not working

for pipes want to know fraction of time did not have prediction
find and example null predictions

exhaustive algorithm for all combinations 
graph statistics with distributions of counts with command chains

colearning, predicting one person's commands, using one person to predict another person
"""

"""
look for $1s and $2s that span commands

get accuracy with fuzzy match with 90% + 
get rid of '&' in output with pipes
match within top 5 -> get prediction returns 5 commands

change pipetemp to $arg
"""