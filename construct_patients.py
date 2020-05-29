# PART 3
# Author : Antoine Bonnet

import doctest
import datetime
import numpy as np
import matplotlib.pyplot as plt

###############################################################################

# 3.1 Patient Class

class Patient:
    """ Represents a patient
    Attributes = num, day_diagnosed, age, sex_gender, postal, state,\
                 temps, days_symptomatic
    """
    
    def __init__(self, num, day_diagnosed, age, sex_gender, postal, state,\
                 temps, days_symptomatic):
        """ (str, str, str, str, str, str, str, str) -> Patient
        Initialize Patient attributes with types
        Patient = (int, int, int, str, str, str, list, int)
        """
        
        #initialize attributes:
        # Patient number (int)
        self.num = int(num)
        
        # Which day into the pandemic they were diagnosed (int)
        self.day_diagnosed = int(day_diagnosed)
        
        # Age of patient (int)
        self.age = int(age)
        
        # sex/gender patient (str) either M, F or X
        if sex_gender[0] == 'M' or sex_gender[0] == 'H' or sex_gender.upper() == 'BOY' :
            self.sex_gender = 'M'
        elif sex_gender[0] == 'F' or sex_gender[0] == 'W' or sex_gender.upper() == 'GIRL':
            self.sex_gender = 'F'
        else:   
            self.sex_gender = 'X'
        
        # First three characters of patient's postal code (str), if N.A.
        #(not valid), use '000'. Valid MTL postal code is H, int, letter
        if postal[0] == 'H' and postal[1].isdigit() and postal[2].isalpha():
            self.postal = postal[0:3] 
        else:
            self.postal = '000'
         
        # State of the patient (str) either I, R or D
        self.state = state
        
        # (List of floats), recording all temperatures of patient in Celsius
        # If receive a string which does not contain any number (eg 'N.A.',
        #the patient died), then recorded as 0

        #initialize variables
        contains_number = False
        digit = ''
        temperatures = []
        
        #If patient is dead, temperature is 0
        if state == 'D':
            temperatures.append(0)
        else:
            # temps is a string
            for index in range(len(temps)):
                character = temps[index]
                #if index == len(temps)-1 and character == '.':
                     #break
                 
            #If character is a number or comma, append to digit
                if character.isdigit():
                    contains_number = True
                    digit += character
                    
            #Note: in French, the comma is used for decimal points    
                elif character  == ',':
                    digit += '.'
                #edge case from dividing columns, getting . at the end of temps
                elif character == '.' and index != len(temps)-2:
                    digit += '.'
                elif character == '-':
                    digit += '.'
                
                    
            if contains_number: #if there is any number in entry
                temperature = float(digit)
                
     # Convert any temperature above 45 degrees to Celsius, round to 2 dec.
                if temperature > 45:
                    new_temps = round((temperature - 32)*5/9, 2)
                else:
                    new_temps = temperature
                temperatures.append(new_temps)
    #if no digit, temps = [0]
            else:
                temperatures.append(0)
                
        self.temps = temperatures
            
        # How many days the patient has been symptomatic (int)
        self.days_symptomatic = int(days_symptomatic)

    def __str__(self):
        """(Patient) -> str

        Returns a string of the following attributes, separated by tabs:
        self.num, self.age, self.sex gender, self.postal, self.day diagnosed,
        self.state, self.days symptomatic,and then all the temperatures
        observed separated by semi-colons
        
        >>> print(str(Patient('0', '0', '42','Woman','H3Z2B5','I','102.2','12')))
        0\t42\tF\tH3Z\t0\tI\t12\t39.0
        """
        temp_list = []
        for temp in self.temps: #self.temps is list of floats
            #string of temperatures separated by semi-colons:
            temp_list.append(str(temp))
        temperatures = ';'.join(temp_list)

        attributes = [str(self.num), str(self.age), self.sex_gender, self.postal, \
        str(self.day_diagnosed), self.state,str(self.days_symptomatic),temperatures]
        return '\t'.join(attributes)

    def update(self, p1):
        """(Patient, Patient) -> None

        Takes as input another Patient object. Assume this object is based
        on an entry that was made after the one the current Patient is based on.
        If this other object's number, sex/gender, and postal code are all the
        as the current patient:
        - Update the days the patient is symptomatic to the newer one
        - Update the state of the patient to the newer one
        - Append the new temperature observed about the patient. You can assume
        the other Patient has only one temperature stored in their temps.
        >>> p0 = Patient('0', '0', '42', 'Woman', 'H3Z2B5', 'I', '102.2', '12')
        >>> p1 = Patient('0', '1', '42', 'F', 'H3Z', 'I', '40,0 C', '13')
        >>> p0.update(p1)
        >>> print(str(p0))
        0   4   F   H3Z   0   I   13   39.0;40.0
        """
        #Raises an AssertionError exception if num/sex_gender/postal are different
        if self.num != p1.num or self.sex_gender != p1.sex_gender \
           or self.postal != p1.postal:
            raise AssertionError("Num/sex_gender/postal codes are different")
        else:
            # Update the days the patient is symptomatic to the newer one
            self.days_symptomatic = p1.days_symptomatic
            
            # Update the state of the patient to the newer one
            self.state = p1.state

            # Append the new temperature observed about the patient
            for temp in p1.temps:
                self.temps.append(temp)
                             

# 3.2 Stage Four

def stage_four(input_filename, output_filename):
    """ (file, file) -> dict

    Takes as input input_filename and output_filename.
    Opens the input file and reads the file line by line.
    Creates a new Patient object for each line.
    Keep and return a dictionary of all the patients:
    - Use the patient's number (int) for the key, and the Patient objects as values
    - Whenever there is a new entry for an existing patient, updates the existing
    Patient object rather than overwrite it
    Writes to output file every Patient converted to a string, sorted by
    patient number (Separated by new lines)
    """
    # Opens the input file and reads the file line by line:
    input_file = open(input_filename, 'r', encoding = 'utf-8')
    output_file = open(output_filename, 'w', encoding = 'utf-8')

    content = input_file.readlines()
    
    # Keep and return a dictionary of all the patients:
    patient_file = {} 
    
    for line in content:
        #separate entries in each list:
        list2 = line.split('\t')
        
        #patient number as key in patient_file (int)
        p_num = int(list2[1])
        
        # Creates a new Patient object for each line:
        patient1 = Patient(list2[1], list2[2], list2[3], list2[4], list2[5],\
                          list2[6], list2[7], list2[8])
# Use the patient's number (int) for the key, and the Patient objects as values
# Whenever there is a new entry for an existing patient, updates the existing
# Patient object rather than overwrite it
        if p_num in patient_file:
            patient_file[p_num].update(patient1)
            #update the pre-existing patient (Patient object):
            
        else:
            #create new patient in file
            patient_file[p_num] = patient1

    #Writes to output file every Patient converted to a string, sorted by
    #patient number (Separated by new lines)
    for p_num in sorted(patient_file):
        patient = patient_file[p_num] 
        output_file.write(str(patient) + '\n')
      
    return patient_file

def fatality_by_age(patient_dict):
    """ (dict) -> list
    Takes as input a dictionary of Patient objects.
    Plots the probability of fatality versus age.
    Rounds patient's ages to the nearest 5 (e.g. 23 -> 25)
    Probability of fatality =
    how many people died/(how many people died + how many people recovered)
    Returns a list of probabilities of death by age group
    >>> p1 = Patient('0', '0', '42', 'W', 'H3Z', 'R', '34.0', '12')
    >>> p2 = Patient('1', '0', '38', 'M', 'H3Z', 'R', '34.0', '12')
    >>> p3 = Patient('2', '0', '42', 'W', 'H3Z', 'D', '34.0', '12')
    >>> p4 = Patient('3', '0', '41', 'M', 'H3Z', 'R', '34.0', '12')
    >>> p5 = Patient('4', '0', '39', 'W', 'H3Z', 'D', '34.0', '12')
    >>> p = {'0' : p1, '1' : p2, '2' : p3, '3' : p4, '4' : p5}
    >>> fatality_by_age(p)
    [0, 0, 0, 0, 0, 0, 0, 0, 0.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    """
    #Set up an age group dictionary with age group as key and list
    #comprising [people having died, people having recovered]
    age_group = []
    for age in range(0, 100, 5):
        age_group.append(age)
        #Values are strings since immutable
    age_dict = dict.fromkeys(age_group, '')

    #iterate through all Patient objects:
    for p_num in patient_dict:
        patient = patient_dict[p_num]
        state = patient.state
        age = patient.age
        age_5 = 5*round(age/5) #round to nearest 5
        
        if state == 'D':
            age_dict[age_5] += 'D'
        elif state == 'R':
            age_dict[age_5] += 'R'
        
    #Create a list of fatality probability
    list_probability = []
    
    
    for age_group in age_dict:
        state = age_dict[age_group]
        
    #number of people having died/recovered for each age
        dead = state.count('D')
        recovered = state.count('R')
        if dead == 0 and recovered == 0: #avoid zero division
            fatality_by_age = 0
        else:
            fatality_by_age = dead/(dead + recovered)
            
        list_probability.append(fatality_by_age)  

    #reinitialize list of age groups
    age_group = []
    for age in range(0, 100, 5):
        age_group.append(age)
        
    #plot graph:
    plt.ylim((0, 1.2)) #y axis range from 0 to 1.2
    plt.plot(age_group, list_probability, 'b')
    
    plt.title('Probability of death by age, by Antoine Bonnet')
    plt.ylabel('Deaths / (Deaths+Recoveries)')
    plt.xlabel('Age (to nearest 5)')
    plt.savefig('fatality_by_age.png')

    return list_probability

############################################################################

if __name__ == '__main__':
    doctest.testmod()
    #p = stage_four('stage3_data.tsv', 'stage4_data.tsv')
    #fatality_by_age(p)
    
   
   
    
