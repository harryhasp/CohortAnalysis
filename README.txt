This project executes cohort analysis


Required dependencies:

1. Implemented in python3
	installation of python3 in linux-type OS:
		$ sudo apt-get update
		$ sudo apt-get install python3.6
	installation of python3 in windows OS:
		https://www.python.org/downloads/

2. Need of pytz library
	since you have already installed python3, then you just need to execute:
		python -m pip install pytz



Possible configuration:

1.	By default, the cohort analysis is being made by grouping timezone to be PDT.
	If another grouping timezone is needed, then it can be changed by inserting the preferable timezone at line 8 of the code



How to execute the program:

	python3 cohort.py [-h] cohorts buckets costumers_file_name orders_file_name result_file_name
	
	cohorts: number of cohorts that the user wants for the analysis
	buckets: number of buckets that the user wants for the analysis
	costumers_file_name: the name of the file that contains the costumers details, ex. costumers.csv (it should be csv type)
	orders_file_name: the name of the file that contains the orders details, ex. orders.csv (it should be csv type)
	result_file_name: the name of the file that contains the final result will be written, ex. output.csv (it should be csv type)