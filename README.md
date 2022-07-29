Thank you to Saul Greenberg for trace data of Unix users. Citation below.

   Greenberg, S. (1988). "Using Unix: collected traces 
      of 168 users".   Research Report 88/333/45, 
      includes tar-format cartridge tape. Department
      of Computer Science, University of Calgary, Alberta.

The graph node structure is contained in `graph.py`.
Parsing functions are defiend in `parse.py`.

Paper describing methods is located in docs folder. 

You may contact patelvap@gmail.com with questions.

### Workflow

The file named `predict_n+1_v3 (final).ipynb` is the final notebook used for collecting data. 
You can run this notebook cell by cell to replicate the results. The last run results should be present in the notebook.

The `parse.py` file will have the relative path of the Unix data as well for parsing and calculating accuracy.

The parser object parses the different user datas with different parsing functions that are named.
Terminologies should be defined in the paper. 

The cells with print statements are the ones that calculate prediction accuracy and take the most time to run.