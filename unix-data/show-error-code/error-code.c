/*
 * Author: 	(c) Saul Greenberg
 * Place:  	University of Calgary
 * Date:   	November, 1988
 * Use:		cat trace-file | error-code > trace-file.new
 * Purpose:	Replace the error codes in the trace files with its
 *		human-readable textual equivalent
 */

#include <stdio.h>
#include "error-code.h"

main ()
{
    char line[1024];
    int msg;
    char type[2];

    while (  gets (line)  != NULL ) {	    /* Read every line 		*/
	if (*line != 'X') { 		    /* If its not an error line */	
	    printf ("%s\n", line);	    /*  write it out		*/	
	    continue;
	}
	

        if (*(line+2) == 'N' && 	    /* Error line, but NIL	*/
	    *(line+3) == 'I') {	    	    /*  value			*/
	    printf ("%s\n", line);	    /*  write it out		*/	
	    continue;
	}

	/* Only error lines with error codes are now possible */
	sscanf (line, "%*c%1S%d", type, &msg);
	printf ("X "); 	    
	switch (*type) { 
	  case 'S':	printf ("%s: ", error_type[0]); break;
	  case 'M':	printf ("%s: ", error_type[1]); break;
	  case 'N':	printf ("%s: ", error_type[2]); break;
	  case 'D':	printf ("%s: ", error_type[3]); break;
	  case 'A':	printf ("%s: ", error_type[5]); break;
	  case 'R':	printf ("%s: ", error_type[5]); break;
	  case 'H':	printf ("%s: ", error_type[6]); break;
	  case 'E':	printf ("%s: ", error_type[7]); break;
	  case 'B':	printf ("%s: ", error_type[8]); break;
	  case 'C':	printf ("%s: ", error_type[9]); break;
	  case 'J':	printf ("%s: ", error_type[10]); break;
	  case 'Y':	printf ("%s: ", error_type[11]); break;
 	  default: 	printf ("SHOULD NEVER SEE THIS!\n"); break;
	}
        printf ("%s\n", error_msg[msg]);
    }
}

