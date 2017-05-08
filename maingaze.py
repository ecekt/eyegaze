#ece k.t.
import numpy as np
import sys
import gaze as g
import csv

text = sys.argv[1] #csv to read from 
v_threshold = float(sys.argv[2]) #velocity threshold
dis_threshold = float(sys.argv[3]) #dispersion threshold
dur_threshold = float(sys.argv[4]) #fixation duration threshold
fixations = sys.argv[5] #fixations will be written to this file
number_of_questions = int(sys.argv[6]) #number of questions asked in the experiment
algorithm = sys.argv[7] #either ivt or idt, fixation classification algorithm
								   
								   
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
user_ids = np.unique(data[:,g.user_id])

textW_file = open(fixations, "w")
textW_file.write("%s" % ("x,y,start_time,finish_time,question,id,group_size,gaze_cue\n"))


for u in user_ids:
	for q in range(1,number_of_questions + 1): #starts from 1 up to number_of_questions, both inclusive
        
		sub_data = g.get_subset(data, q, u) #this is a list
		sub2d = np.asarray(sub_data).reshape(len(sub_data),no_of_columns) #this is a numpy array

		#print len(sub2d)

		group = sub2d[0][g.group_size]
	
		if(algorithm == "ivt"):
			centroidsX, centroidsY, time0, time1 = g.ivt(sub2d,v_threshold)
		elif(algorithm == "idt"):
			centroidsX, centroidsY, time0, time1 = g.idt(sub2d,dis_threshold,dur_threshold)

		#print len(centroidsX), len(centroidsY), len(time0),len(time1)
		cue = q%2 #gaze cue 1 in odd-numbered questions, 0 otherwise		
        
		for r in range(len(centroidsX)):
			textW_file.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (str(centroidsX[r]), str(centroidsY[r]), str(time0[r]), str(time1[r]), str(q), str(u), str(group), str(cue)))
