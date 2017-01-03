#ece kamer takmaz
#ecekt028@gmail.com
import numpy as np
import sys
import gaze as g
import csv

text = sys.argv[1] #csv
v_threshold = float(sys.argv[2])
dis_threshold = float(sys.argv[3])
dur_threshold = float(sys.argv[4])
fixations = sys.argv[5]
grouptext= sys.argv[6]

def get_subset(data, question, user):

    subset = []

    for i in range(len(data)):
        if(data[i][g.user_id] == u and data[i][g.question] == str(q)):
            subset.append(data[i])
            
    #print len(data),q,u
    return subset


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
            #print count
            #print ', '.join(row)
            sub.append(row)
        count += 1   

data = np.array(sub)
user_ids = np.unique(data[:,g.user_id])

#TODO: number of questions = 10

textW_file = open(fixations, "w")
textW_file.write("%s" % ("x,y,start_time,finish_time,question,id,group_size,gaze_cue\n"))


for u in user_ids:
    for q in range(1,11): #starts from 1 up to 10, both inclusive
        
        sub_data = get_subset(data, q, u) #this is a list
        sub2d = np.asarray(sub_data).reshape(len(sub_data),no_of_columns) #this is a np array

        print len(sub2d)
                
        #CHANGE HERE FOR THE ALGORITHM
        centroidsX, centroidsY, time0, time1 = g.ivt(sub2d,v_threshold)
        #centroidsX, centroidsY, time0, time1 = g.idt(sub2d,dis_threshold,dur_threshold)

        print len(centroidsX), len(centroidsY), len(time0),len(time1)

        cue = q%2 #gaze cue 1 in odd-numbered questions, 0 otherwise
        
        group = sub2d[0][g.group_size] #TODO: might change this later
        
        for r in range(len(centroidsX)):
            textW_file.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (str(centroidsX[r]), str(centroidsY[r]), str(time0[r]), str(time1[r]), str(q), str(u), str(group), str(cue)))
            
