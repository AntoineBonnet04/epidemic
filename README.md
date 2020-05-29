# epidemic
Data parsing for an epidemic simulation

Hello!
This project consists in parsing and cleaning-up a list of raw data produced during an epidemic simulation. 

The raw data is contained in the data.txt file, where each line of your raw file contains the following information:
1. A number representing who recorded the data
2. A number representing the patient — each patient has a unique number. The first patient diagnosed with the flu has the patient number 0, the second patient has the patient number 1, etc. There could be multiple rows for the same patient — for example they could be diagnosed on one day, and then die on another day.
3. The date this entry was made
4. The patient’s date of birth
5. The patient’s sex/gender (some have sex recorded, some gender)
6. The patient’s home postal code
7. The patient’s state: Infected / Recovered / Dead (at the time the entry was made)
8. The patient’s temperature at the time the entry was made
9. How many days the patient has been symptomatic

This program is meant to account for human, syntaxic, writing and formatting errors made during the production of the raw file. 

The process is divided into 4 stages, with one corresponding file each:

Stage 1 (initial_clean.py) : Formatting errors
Stage 2 (initial_clean.py) : Syntaxic errors
Stage 3 (time_series.py): Finds age of each patient, language and translation errors, plots a graph with the number of infected/recovered/dead patients every day
Stage 4 (construct_patients.py): Patient class, plots a graph with fatality rates by age
