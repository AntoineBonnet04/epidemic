# PART 1
# Author: Antoine Bonnet

import doctest

##############################################################################
#1.1 Which Delimiter

def which_delimiter(entry):
    """ (str) -> str
    A delimiter is the name for a string used to separate
    columns of data on a single line. Takes as input a string and
    returns the most commonly used delimiter in the input string.
    Delimiter may be a space, comma or tab. No ties.
    
    >>> which_delimiter('0 1 2,3')
     ' '
    >>> which_delimiter('1ja920.ww')
    Traceback (most recent call last):
    AssertionError: Should have at least one delimiter
    >>> which_delimiter('cat\\tdog\\trat')
    '\\t'
    """
    count = {' ' : 0, ',' : 0, '\t': 0} #initialize count 
    
    for character in entry:
        if character == ' ':
            count[' '] += 1
        elif character == ',':
            count[','] += 1
        elif character == '\t':
            count['\t'] += 1
            
    #if there is no space, comma or tab, raise Assertion Error
    if count[' '] == 0 and count[','] == 0 and count['\t'] == 0: 
        raise AssertionError('Should have at least one delimiter')
    else:
        #return the key with maximal value in dictionary 
        return max(count, key = count.get)

#1.2 Stage 1: Delimiting and Capitals
    
def stage_one(input_filename, output_filename):
    """(file, file) -> int
    Will open the file with the name input_filename, and read
    the file line by line. Will make changes to each line and then
    writing the new version of the line to a new file named output_filename

    Changes to make to data:
    1. Change the most common delimiter to tab (if not already tab-delimited)
    2. Change all text to be upper case
    3. Change any / or . in the dates to hyphens

    Returns how many lines were written to output_filename

    >>> stage_one('1111111.txt', 'stage1.tsv')
    4
    """
    #open input and output files
    input_file = open(input_filename, 'r', encoding = 'utf-8')
    output_file  = open(output_filename, 'w', encoding = 'utf-8')

    #read input file line by line, returns a list of each line
    content = input_file.readlines()
    
    for entry in content:
        delimiter = which_delimiter(entry)
        # Change most common delimiter to tab:
        if delimiter != '\t':
            entry = entry.replace(delimiter, '\t')
        #all uppercase
        entry = entry.upper()
        #replace any / or . in the dates to hyphens
        entry = entry.replace('/', '-')
        entry = entry.replace('.', '-')
        output_file.write(entry)
      
    return len(content)

#1.3 Stage 2: Consistent Columns

def stage_two(input_filename, output_filename):
    """(file, file) -> int
    Will open the file with the name input_filename, and read
    the file line by line. Will make changes to each line and then
    writing the new version of the line to a new file named output_filename

    Changes to make to data:
    1. All lines should have 9 columns
    2. Any line with more than 9 columns should be cleaned so the line
    is now 9 columns. For example, in French the comma is used for decimal
    points, so the temperature ’39,2’ could have been broken into 39 and 2.
    
    Returns how many lines were written to output_filename

    >>> stage_one('stage1.tsv', 'stage2.tsv') 
    4
    """
    #open input and output files
    input_file = open(input_filename, 'r', encoding = 'utf-8')
    output_file  = open(output_filename, 'w', encoding = 'utf-8')
    
    #read input file line by line, returns a list of each line
    content = input_file.readlines()
    
    for line in content:
        #list of entries in each line 
        list_entry = line.split('\t')

        #record length of entries in line
        length = len(list_entry) 
        
        #if there are less than 9 columns, deletes the entry
        if length < 9: 
            continue
        
        #if there are more than 9 columns:
        elif length > 9:
            #edge case: Not applicable separated into two columns
            if list_entry[7][0].upper() == 'N' and list_entry[8][0].upper() == 'A':
                list_entry[7] += ' ' + list_entry[8]
                del list_entry[8]
            elif list_entry[5][0].upper() == 'N' and list_entry[6][0].upper() == 'A':
                list_entry[5] += ' ' + list_entry[6]
                del list_entry[6]
            
              #If postal code was input as "X1X 1X1"
            postal1 = list_entry[5]
            postal2 = list_entry[6]

            if len(postal1) == 3 and len(postal2) == 3 and postal2[0].isdigit():
                list_entry[5] += list_entry[6]
                del list_entry[6]
                new_entry = '\t'.join(list_entry)
                
            if len(list_entry) > 9:
                #Fix temperature:
                list_entry[7] += '.'
                list_entry[7] += list_entry[8]
                del list_entry [8]

            
            new_entry = '\t'.join(list_entry)
            
        #if there are 9 columns:               
        else:
            new_entry = line
       
        output_file.write(new_entry)
   
        
    return len(content)

if __name__ == "__main__":
    doctest.testmod()
    #stage_one('data.txt', 'stage1_data.tsv')
    #stage_two('stage1_data.tsv', 'stage2_data.tsv')
    
