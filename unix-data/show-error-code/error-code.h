/*
 * Author: 	(c) Saul Greenberg
 * Place:  	University of Calgary
 * Date:   	November, 1988
 * Use:		cat trace-file | error-code > trace-file.new
 * Purpose:	Replace the error codes in the trace files with its
 *		human-readable textual equivalent
 */

char *error_type[] = {
 "syntax error",			/* S 0 */ 
 "reg expression error",		/* M 1 */ 
 "execution error",			/* N 2 */ 
 "directory error",			/* D 3 */ 
 "alias problem",			/* A 4 */ 
 "redirection problem",			/* R 5 */ 
 "history problem",			/* H 6 */ 
 "expression error",			/* E 7 */ 
 "built in problem",			/* B 8 */ 
 "control error",			/* C 9 */ 
 "job error",				/* J 10 */ 
 "system error",			/* Y 11 */ 
};

/* The error message written on the command line by csh */
char *error_msg[] = {
 "unknown error",			/* 0 */
 "*chdir didn't work",			/* 1 */
 "No other directory",			/* 2 */
 "Directory stack not that deep",	/* 3 */
 "Bad directory",			/* 4 */
 "Directory stack empty",		/* 5 */
 "No home directory",			/* 6 */
 "Can't change to home directory",	/* 7 */
 "Usage: dirs [ -l ]",			/* 8 */
 "No match",				/* 9 */
 "Command not found",			/* 10 */
 "Unmatched (something)",		/* 11 */
 "Word too long",			/* 12 */
 "Variable syntax",			/* 13 */
 "Expansion buf ovflo",			/* 14 */
 "Bad ! form",				/* 15 */
 "No prev sub",				/* 16 */
 "Bad substitute",			/* 17 */
 "No prev lhs",				/* 18 */
 "Rhs too long",			/* 19 */
 "Bad ! modifier",			/* 20 */
 "Modifier failed",			/* 21 */
 "Subst buf ovflo",			/* 22 */
 "Bad ! arg selector",			/* 23 */
 "No prev search",			/* 24 */
 ": Event not found",			/* 25 */
 "Alias loop",				/* 26 */
 "Too many )'s",			/* 27 */
 "Too many ('s",			/* 28 */
 "Badly placed (",			/* 29 */
 "Missing name for redirect",		/* 30 */
 "Ambiguous output redirect",		/* 31 */
 "Can't << within ()'s",		/* 32 */
 "Ambiguous input redirect",		/* 33 */
 "Badly placed ()'s",			/* 34 */
 "Invalid null command",		/* 35 */
 "Ambiguous",				/* 36 */
 "$< line too long",			/* 37 */
 "No file for $0",			/* 38 */
 "Subscript out of range",		/* 39 */
 "Bad : mod in $",			/* 40 */
 "<< terminator not found",		/* 41 */
 "Line overflow",			/* 42 */
 "Divide by 0",				/* 43 */
 "Mod by 0",				/* 44 */
 "Expression syntax",			/* 45 */
 "Missing }",				/* 46 */
 "Missing file name",			/* 47 */
 "Too few arguments",			/* 48 */
 "Too many arguments",			/* 49 */
 "Too dangerous to alias that",		/* 50 */
 "Empty if",				/* 51 */
 "Improper then",			/* 52 */
 "Syntax error",			/* 53 */
 "Not in while/foreach",		/* 54 */
 "Invalid variable",			/* 55 */
 "Words not ()'d",			/* 56 */
 "then/endif not found",		/* 57 */
 "endif not found",			/* 58 */
 "endsw not found",			/* 59 */
 "end not found",			/* 60 */
 "label not found",			/* 61 */
 "Improper mask",			/* 62 */
 "No such limit",			/* 63 */
 "Improper or unknown scale factor",	/* 64 */
 "Bad scaling; did you mean ?",		/* 65 */
 "Can't suspend a login shell (yet)",	/* 66 */
 "Can't from terminal",			/* 67 */
 "Not login shell",			/* 68 */
 "Unknown user:",			/* 69 */
 "Path error",				/* 70 */
 "Missing ]",				/* 71 */
 "Arguments too long",			/* 72 */
 "Pathname too long",			/* 73 */
 "Unmatched `",				/* 74 */
 "Too many words from",			/* 75 */
 "Undefined variable",			/* 76 */
 "Usage: jobs [ -l ]",			/* 77 */
 "Bad signal number",			/* 78 */
 "Unknown signal; kill -l lists signals", 	/* 79 */
 "Arguments should be jobs or process id's", 	/* 80 */
 "There are stopped jobs",		/* 81 */
 "No current job",			/* 82 */
 "No previous job",			/* 83 */
 "No such job",				/* 84 */
 "No job matches pattern",		/* 85 */
 "No job control in this shell",	/* 86 */
 "No job control in subshells",		/* 87 */
 "No such file or directory",		/* 88 */
 "Error 0",				/* 89 - 122 are from sys-err files */
 "Not super-user",			/* 90 */
 "No such file or directory",		/* 91 */
 "No such process",			/* 92 */
 "Interrupted system call",		/* 93 */
 "I/O error",				/* 94 */
 "No such device or address",		/* 95 */
 "Arguments too long",			/* 96 */
 "Exec format error",			/* 97 */
 "Bad file number",			/* 98 */
 "No children",				/* 99 */
 "No more processes",			/* 100 */
 "Not enough core",			/* 101 */
 "Permission denied",			/* 102 */
 "Error 14",				/* 103 */
 "Block device required",		/* 104 */
 "Mount device busy",			/* 105 */
 "File exists",				/* 106 */
 "Cross-device link",			/* 107 */
 "No such device",			/* 108 */
 "Not a directory",			/* 109 */
 "Is a directory",			/* 110 */
 "Invalid argument",			/* 111 */
 "File table overflow",			/* 112 */
 "Too many open files",			/* 113 */
 "Not a typewriter",			/* 114 */
 "Text file busy",			/* 115 */
 "File too large",			/* 116 */
 "No space left on device",		/* 117 */
 "Illegal seek",			/* 118 */
 "Read-only file system",		/* 119 */
 "Too many links",			/* 120 */
 "Broken Pipe",				/* 121 */
 "Disk quota exceeded",			/* 122 */
};

