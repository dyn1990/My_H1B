# Problem
The goal of this repo is to extract a few statistics of H1B visas, from immigration data on H1B(H-1B, H-1B1, E-3) visa application processing over the past years. The statistics to calculate are: Top 10 Occupations and Top 10 States for certified visa applications.
Finally, The codes in the repo should be able to generalize to the same dataset for different time windows.

# Input dataset
Raw data could be found here under the Disclosure Data tab (i.e., files listed in the Disclosure File column with ".xlsx" extension). For years 2014~2016, the dat was acquired from Insight Google Drive, while for years 2017 and 2018, data were scraped from the official website.

# Output statistics
* `top_10_occupations.txt`: Top 10 occupations for certified visa applications.
* `top_10_states.txt`: Top 10 states for certified visa applications.

Each line of the `top_10_occupations.txt` contains the following:
1. __`TOP_OCCUPATIONS`__: the occupation name associated with an application's Standard Occupational Classification (SOC) code.
2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for that occupation. An application is considered certified if it has a case status of `Certified`.
3. __`PERCENTAGE`__: % of applications that have been certified for that occupation compared to total number of certified applications regardless of occupation, rounded off to 1 decimal place.

The records ise sorted by __`NUMBER_CERTIFIED_APPLICATIONS`__, and in case of a tie, alphabetically by __`TOP_OCCUPATIONS`__.

Each line of the `top_10_states.txt` contains the following:
1. __`TOP_STATES`__: State where the work will take place.
2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for work in that state. An application is considered certified if it has a case status of `Certified`.
3. __`PERCENTAGE`__: % of applications that have been certified in that state compared to total number of certified applications regardless of state, rounded off to 1 decimal place.

# Approach
The number of the records in the dataset for each year is more large, therefore the code uses a dynamical reading and extraction to gather the statistics needed. Specifically:
* Construct a H1B class, where all the statistics needed are initialized. We maintain the statistics through out the main program.
* Read headers, locate the columns that contain relative information.
* Read line by line from the dataset, extract information about the occupation and states in that record, and dynamically update the statistics.
* Sort the statistics, then output to .txt files.

# How to run it
* An input file named `h1b_input.csv` is needed, with proper format as from the official website, or at least contains relative information about the statistics calculated. 
* Run `run.sh` will output the expected statistics.
