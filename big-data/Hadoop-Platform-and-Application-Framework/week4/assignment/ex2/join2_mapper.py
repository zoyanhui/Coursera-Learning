#!/usr/bin/python
import sys

# --------------------------------------------------------------------------
#This mapper code will input a <date word, value> input file, and move date into 
#  the value field for output
#  
#  Note, this program is written in a simple style and does not full advantage of Python 
#     data structures,but I believe it is more readable
#
#  Note, there is NO error checking of the input, it is assumed to be correct
#     meaning no extra spaces, missing inputs or counts,etc..
#
# See #  see https://docs.python.org/2/tutorial/index.html for details  and python  tutorials
#
# --------------------------------------------------------------------------



for line in sys.stdin:
    line       = line.strip()   #strip out carriage return
    key_value  = line.split(",")   #split line, into key and value, returns a list
    key_in     = key_value[0]
    value_in   = key_value[1]   #value is 2nd item
    count = None
    try:
        count = int(value_in)
    except:
        pass
    if count:
        print( '%s\t%s' % (key_in, value_in) )  #print a string tab and string
    elif value_in == 'ABC':
        print( '%s' % (key_in,) )  #print a string tab and string


#Note that Hadoop expects a tab to separate key value
#but this program assumes the input file has a ',' separating key value