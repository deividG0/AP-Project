# create a program to generate the random string of given letters.
import random
import string

def specific_string(length):
    sample_string = 'ab'  # define the specific string
    # define the condition for random string
    result = ''.join((random.choice(sample_string)) for x in range(length))
    print(" Randomly generated string is: ", result)

specific_string(8)  # define the length
specific_string(10)