#ece k.t.
import numpy as np
import sys
import gaze as g
import csv

text = sys.argv[1] #csv to read from 
group_text = sys.argv[2] #group-related output will be written to this file
group_window = int(sys.argv[3]) #temporal duration of the window that we will check the group dispersion
								  #every 5 data points for instance
								  #NOTE: NOT DURATION IN MILLISECONDS OR SECONDS
								  
with open(text, 'rb') as cf:
	reader = csv.reader(cf, delimiter=',')
	count = 0
	no_of_columns = len(next(reader)) 
	cf.seek(0)              
	sub = []
    
	for row in reader:
		if(count == 0):
			header = row
		else:
			sub.append(row)
		count += 1   

data = np.array(sub)

us, gr, gs, qs = g.get_users_and_groups_and_questions(data)

results_to_text = g.get_group_dispersion_results(data, us, gr, gs, qs, group_window)

print us,"\n", gr, "\n", gs, "\n", qs

textW_file = open(group_text, "w")

textW_file.write("%s" % ("Users\n"))

for users in us:	
	textW_file.write("%s\n" % (users))

textW_file.write("\n%s\n" % ("Groups\tGroup Size\tNumber of Questions"))
	
for i in (range(len(gr))):	
	textW_file.write("%s\t%s\t\t\t%s\n" % (gr[i], gs[i], qs[i]))
	
textW_file.write("%s" % (results_to_text))

print "Results have been written to \"" + group_text + "\"."