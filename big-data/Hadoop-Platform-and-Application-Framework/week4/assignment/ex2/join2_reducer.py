#!/usr/bin/python
import sys

# --------------------------------------------------------------------------
#This reducer code will input a <word, value> input file, and join words together
# Note the input will come as a group of lines with same word (ie the key)
# As it reads words it will hold on to the value field
#
# It will keep track of current word and previous word, if word changes
#   then it will perform the 'join' on the set of held values by merely printing out 
#   the word and values.  In other words, there is no need to explicitly match keys b/c
#   Hadoop has already put them sequentially in the input 
#   
# At the end it will perform the last join
#
#
#  Note, there is NO error checking of the input, it is assumed to be correct, meaning
#   it has word with correct and matching entries, no extra spaces, etc.
#
#  see https://docs.python.org/2/tutorial/index.html for python tutorials
#
#  San Diego Supercomputer Center copyright
# --------------------------------------------------------------------------
curr_tv_show_in_channel = False
curr_tv_show_total_cnt = 0
prev_tv_show = None

for line in sys.stdin:
    line       = line.strip()       #strip out carriage return
    key_value  = line.split('\t')   #split line, into key and value, returns a list     

    #note: for simple debugging use print statements, ie: 
    count = None 
    curr_tv_show  = key_value[0].strip()         #key is first item in list, indexed by 0
    if len(key_value) == 2:
        value_in = key_value[1].strip()         #value is 2nd item
        count = int(value_in)
        if curr_tv_show == prev_tv_show:
            curr_tv_show_total_cnt += count
            continue
        else:
            if curr_tv_show_in_channel:
                print('{0} {1}'.format(prev_tv_show,curr_tv_show_total_cnt))
            curr_tv_show_in_channel = False
            curr_tv_show_total_cnt = count
            prev_tv_show = curr_tv_show

    elif len(key_value) == 1:
        if curr_tv_show == prev_tv_show:
            curr_tv_show_in_channel = True
        else:
            if curr_tv_show_in_channel:
                print('{0} {1}'.format(prev_tv_show,curr_tv_show_total_cnt))
            curr_tv_show_in_channel = True
            curr_tv_show_total_cnt = 0
            prev_tv_show = curr_tv_show
    else:
        continue        

# ---------------------------------------------------------------
#now write out the LAST join result
# ---------------------------------------------------------------
if curr_tv_show_in_channel and curr_tv_show_total_cnt > 0:
    print('{0} {1}'.format(prev_tv_show,curr_tv_show_total_cnt))
