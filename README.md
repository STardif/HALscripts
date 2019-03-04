# HALscripts
Several python scripts to extract data from HAL (the French open archive).
All scripts are released without any warranty !

It uses the requests to haltools to get the data (essentially lists of publications).

## doublons_hal_check.py 
This script will try to identify the doubles in a list of references 

**Usage** 

1- edit the doublons_hal_check.py file to change the search parameters used to get the reference list, *i.e.* the first and last year of publication, as well as the research structure number. Additional parameters should work (not tested)

2- run the following line in a terminal : python doublons_hal_check.py 

3- the result of the analysis is shown in the terminal

## lab_connections.py
This script will plot the "connections" (common publications) between different research structures

**Usage** 

1- edit the lab_connections.py file to include the research structures of interest in the dictionnary.  

2- run the following line in a terminal : python lab_connections.py

3- the plot should be displayed in a new window
