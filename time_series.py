# PART 2
# Author: Antoine Bonnet

import doctest
import datetime
import matplotlib.pyplot as plt
##############################################################################

#2.1 Date diff

def date_diff(date1, date2):
    """ (str, str) -> int
    Takes as input two strings representing dates in ISO format (eg. 2019-11-29)
    Returns how many days apart the two dates are, as an integer
    If the first date is earlier than the second date, returns positive integer
    else, returns negative integer
    >>> date_diff('2019-10-31', '2019-11-2')
    2
    >>> date_diff('2019-11-2', '2019-10-31')
    -2
    >>> date_diff('2019-1-1', '2018-12-31')
    -1
    """
    date1_list = date1.split('-')
    date2_list = date2.split('-')

    year1 = int(date1_list[0])
    year2 = int(date2_list[0])
    
    month1 = int(date1_list[1])
    month2 = int(date2_list[1])
                 
    day1 = int(date1_list[2])
    day2 = int(date2_list[2])
                 
    #create datetime objects:
    date_1 = datetime.date(year1, month1, day1)
    date_2 = datetime.date(year2, month2, day2)
    diff = date_1 - date_2 #returns timedelta object with attribute days
    return -int(diff.days)

#2.2 Get Age

def get_age(date1, date2):
    """ (str, str) -> int
    Takes as input two strings representing dates in ISO format
    and returns how many complete years apart the two dates are, as an integer
    If the first date is earlier than the second date, returns positive integer
    else, returns negative integer. 1 year = 365.2425 days
    >>> get_age('2018-10-31', '2019-11-2')
    1
    >>> get_age('2018-10-31', '2000-11-2')
    -17
    """

    day_diff = date_diff(date1, date2)
    year_diff = day_diff/365.2425
    if year_diff < 0:
        return -int(-year_diff)
    else:
        return int(year_diff)
    return (diff/365.2425)

# Stage Three

def stage_three(input_filename, output_filename):
    """(str, str) -> dict
    Takes as input input_filename and output_filename.
    Will open the file input_filename, and read the file line by line.
    Will make changes to each line and then writing the new version of the line
    to the file named output_filename. Index date : first date in the first line
    of the file. Will make the following changes to the data:
    
    1. Replace the date of each record with the date_diff of that date
    and the index date
    2. Replace the date of birth with age at the time of the index date
    3. Replace the status with one of I, R or D (Infected, Recovered, Dead)
    French equivalents are infecté(e), récupéré(e) and mort(e)
    
    Returns a dictionary. The keys are each day of the pandemic (integer),the
    values are a dictionary, with how many people are in each state on that day
    >>> stage_three('stage2.tsv', 'stage3.tsv')
    {0: {’I’: 1, ’D’: 0, ’R’: 0}, 1: {’I’: 2, ’D’: 1, ’R’: 0}}
    """
    #open input and output files
    input_file = open(input_filename, 'r', encoding = 'utf-8')
    output_file = open(output_filename, 'w', encoding = 'utf-8')

    #read input file line by line, returns a list of each line
    content = input_file.readlines()

    #Index date is the second entry in the first line of content
    index_date = (content[0].split('\t'))[2] 
    list_status = ['I', 'D', 'R']
    pandemic = {}
    
    for line in content:
        list_line = line.split('\t')
        
        #replace the date of birth with age at the time of that date
        list_line[3] = get_age(list_line[3], index_date)

        #replace the date of each record with the date_diff with index date
        list_line[2] = date_diff(index_date, list_line[2])
        date = list_line[2]

        #replace French commas and hyphens to dots in temperature entry
        list_line[7] = list_line[7].replace('-','.')
        list_line[7] = list_line[7].replace(',', '.')

        #Initialize pandemic dictionary with all days
        if date not in pandemic:
            pandemic[date] = dict.fromkeys(list_status, 0)

        #replace the status with I, R or D
        status = list_line[6][0] #first letter of status
        if status == 'I': #infected patient
            list_line[6] = 'I'
            pandemic[date]['I'] += 1 
        elif status == 'R': #recovered patient
            list_line[6] = 'R'
            pandemic[date]['R'] += 1  
        elif status == 'D' or status == 'M': #dead or mort(e)
            list_line[6] = 'D'
            pandemic[date]['D'] += 1
        
        
        #group back modified line and write in output file
        line_modified = '\t'.join(str(entry) for entry in list_line)
        output_file.write(line_modified)
        
    return pandemic
    
def plot_time_series(time_dict):
    """ (dict) -> list
    Takes as input a dictionary of dictionaries, formatted as the return value
    of stage three. Returns a list of lists, where each sublist represents
    each day of the pandemic. Each sublist of the form:
    [how many people infected, how many people recovered, how many people dead]
    >>> d = stage_three('stage2.tsv', 'stage3.tsv')
    >>> plot_time_series(d)
    [[1, 0, 0], [2, 0, 1]]
    """
    time_list = []
    infected_list = []
    recovered_list = []
    dead_list = []
    
    for day in time_dict:
        day_list = []
        #dictionary for each day
        day_dict = time_dict[day]
 
        #add corresponding values for each status in corresponding list
        day_list.append(day_dict['I'])
        infected_list.append(day_dict['I'])
        
        day_list.append(day_dict['R'])
        recovered_list.append(day_dict['R'])
        
        day_list.append(day_dict['D'])
        dead_list.append(day_dict['D'])
            
        time_list.append(day_list)


    # Fill with zeroes if no data for 11 days:
    infected_list += [0*index for index in range(12 - len(infected_list))]
    recovered_list += [0*index for index in range(12 - len(recovered_list))]
    dead_list += [0*index for index in range(12  - len(dead_list))]
    
    time_axis = []
    
    for index in range(12): #11 days in total
        
        #List of days for x axis in plot    
        time_axis.append(index)
        
         #for each entry in dead/recovered/infected list, add
        #number of preceding d/r/i entries -> cumulative
        if index > 0:
            dead_list[index] += dead_list[index-1]
            recovered_list[index] += recovered_list[index-1]
            infected_list[index] += infected_list[index-1]
    
    # Plot graph:
    plt.plot(time_axis, infected_list, 'b')
    plt.plot(time_axis, recovered_list, 'orange')
    plt.plot(time_axis, dead_list, 'g')
    
    plt.title("Time series of early pandemic, by Antoine Bonnet")
    plt.ylabel('Number of People')
    plt.xlabel('Days into Pandemic')
    plt.legend(['Infected', 'Recovered', 'Dead'])
    plt.savefig("time_series.png")

    return time_list      
    
if __name__ == "__main__":
    doctest.testmod()
    #d = stage_three('stage2_data.tsv', 'stage3_data.tsv')
    #plot_time_series(d)
    
    
