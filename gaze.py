#ece k.t.
from __future__ import division
import numpy as np
from collections import Counter

#column indices of attributes, check csv file
index = 0
timestamp = 1
question = 2
x = 3
y = 4
user_id = 5
group_size = 6
gaze_cue = 7

def ivt(data, v_threshold):
    
	times = data[:,timestamp]
    
	ts = []
    
	for t in times:
		ts.append(float(t)/1000.0)
     
	times = ts #TOD0: CHECK if times in sec
    
	Xs = data[:,x]
	Ys = data[:,y]

	difX = []
	difY = []
	tdif = []
	

	for i in range(len(data) - 1):
		difX.append(float(Xs[i+1]) - float(Xs[i]))
		difY.append(float(Ys[i+1]) - float(Ys[i]))
		tdif.append(float(times[i+1]) - float(times[i]))
        
	
	print tdif
	dif = np.sqrt(np.power(difX,2) + np.power(difY,2)) #in pix
		
	velocity = dif / tdif
	#print velocity in pix/sec
	#print tdif

	mvmts = [] #length is len(data)-1
    
	for v in velocity:
		if (v < v_threshold):
			#fixation
			mvmts.append(1)
			#print v, v_threshold
		else:
			mvmts.append(0)

	fixations = []
	fs = []

	#print mvmts
    
	for m in range(len(mvmts)):
		if(mvmts[m] == 0):
			if(len(fs) > 0):
				fixations.append(fs)
				fs = []
		else:
			fs.append(m)

	if(len(fs) > 0):
		fixations.append(fs)

	#print fixations
	centroidsX = []
	centroidsY = []
	time0 = []
	time1 = []

	for f in fixations:
		cX = 0
		cY = 0
        
		if(len(f) == 1):
			i = f[0]
			cX = (float(data[i][x]) + float(data[i+1][x]))/2.0
			cY = (float(data[i][y]) + float(data[i+1][y]))/2.0
			t0 = float(data[i][timestamp])
			t1 = float(data[i+1][timestamp])
            
		else:
			t0 = float(data[f[0]][timestamp])
			t1 = float(data[f[len(f)-1]+1][timestamp])
            
			for e in range(len(f)):
                
				cX += float(data[f[e]][x]) 
				cY += float(data[f[e]][y])

			cX += float(data[f[len(f)-1]+1][x]) 
			cY += float(data[f[len(f)-1]+1][y]) 
			
			cX = cX / float(len(f)+1)
			cY = cY / float(len(f)+1)
            
		centroidsX.append(cX)
		centroidsY.append(cY)
		time0.append(t0)
		time1.append(t1)
                
	return centroidsX, centroidsY, time0, time1


def idt(data, dis_threshold, dur_threshold):

	window_range = [0,0]

	current = 0 #pointer to represent the current beginning point of the window
	last = 0
	#final lists for fixation info
	centroidsX = []
	centroidsY = []
	time0 = []
	time1 = []
    
	while (current < len(data)):
        
		t0 = float(data[current][timestamp]) #beginning time
		t1 = t0 + float(dur_threshold)     #time after a min. fix. threshold has been observed

		for r in range(current, len(data)): 
			if(float(data[r][timestamp])>= t0 and float(data[r][timestamp])<= t1):
				#print "if",r
				last = r #this will find the last index still in the duration threshold

		window_range = [current,last]

		#now check the dispersion in this window
		#print "window", current, last
		dispersion = get_dispersion(data[current:last+1])
		#a[2:5] gives 2,3,4. To include last one, [2:6]
        
		if (dispersion <= dis_threshold):

			#add new points
			while(dispersion <= dis_threshold and last + 1 < len(data)):

				last += 1
				window_range = [current,last]
				#print current, last, "*"
				#print "*"
				dispersion = get_dispersion(data[current:last+1])
       
			#dispersion threshold is exceeded
			#fixation at the centroid [current,last]

			cX = 0
			cY = 0
            
			for f in range(current, last + 1):
				cX += float(data[f][x])
				cY += float(data[f][y])

			cX = cX / float(last - current + 1)
			cY = cY / float(last - current + 1)
                
			t0 = float(data[current][timestamp])
			t1 = float(data[last][timestamp])
            
			centroidsX.append(cX)
			centroidsY.append(cY)
			time0.append(t0)
			time1.append(t1)
            
			current = last + 1 #this will move the pointer to a novel window

		else:
			current += 1 #this will remove the first point
			last = current #this is not necessary
            
	return centroidsX, centroidsY, time0, time1

def get_dispersion(points):

	dispersion = 0
    
	argxmin = np.min(points[:,x].astype(np.float))
	argxmax = np.max(points[:,x].astype(np.float))
    
	argymin = np.min(points[:,y].astype(np.float))
	argymax = np.max(points[:,y].astype(np.float))

	dispersion = ((argxmax - argxmin) + (argymax - argymin))/2
	#TODO: look for other ways of calculating dispersion
    
	return dispersion

def get_distance(x1, y1, x2, y2):
	
	#distance between two points
	
	return np.sqrt(np.power(x1-x2,2) + np.power(y1-y2,2))
	
	
def find_user_closest_to_centroid(centroidX, centroidY, group_size, user_coordinates):
	
	distances = []
	
	for u in range(group_size):
	
		uX = user_coordinates[u*2]
		uY = user_coordinates[u*2 + 1]
		distances.append(get_distance(centroidX, centroidY, uX, uY))
		
	#returns the index of the first occurrence of minimum value
	return np.argmin(distances)
		

def get_subset(data, questionno, user):

	subset = []

	for i in range(len(data)):
		if(data[i][user_id] == user and data[i][question] == str(questionno)):
			subset.append(data[i])
            
	#print len(subset),q,u
	return subset

def get_length_of_subset(data, questionno, user):

	subset = []

	for i in range(len(data)):
		if(data[i][user_id] == user and data[i][question] == str(questionno)):
			subset.append(data[i])
            
	return len(subset)
	
def get_users_and_groups_and_questions(data):
	groups = []
	number_of_questions = []
	group_size = []
	
	users = list(set(data[:,user_id]))
	temp_users = []
	
	#remove ids from single user experiments
	for u in range(len(users)):
		if(len(users[u]) < 7):
			temp_users.append(users[u]) 
			
	users = np.sort([x for x in users if x not in temp_users])
	
	#all the group ids with repetition
	temp_groups = []
	
	for u in users:
		temp_groups.append(u[:len(u) - 2])
	
	#unique group ids without repetition
	groups = np.unique(temp_groups)
	
	for gr in groups:
		
		#group sizes
		all = [gp for gp in temp_groups if gp == gr]
		group_size.append(len(all))
		
		#number of questions per group
		
		#find one user from each group
		selected_user_ids = [d for d in data if d[user_id][:len(u) - 2] == gr][0][user_id]
		#print selected_user_ids
		subset = [e for e in data if e[user_id] == u]
		
		#get the question number from the last data point for a selected user
		number_of_questions.append(int (subset[len(subset)-1][2]))
	
	return users, groups, group_size, number_of_questions
	
def get_users_in_a_group(users, group):
	
	#returns the ids of users belonging to a given group id
	users_in_a_group = []
	
	for u in users:
		if u[:len(u)-2] == group:
			users_in_a_group.append(u)
	
	return users_in_a_group
	
def calculate_group_dispersion(coordinates, group_size, users, length_of_data, data_points_in_window, group_users):

	#parameters for the whole dataset
	dispersions = []
	average_dispersion = 0
	centroidsX = []
	average_centroidX = 0
	centroidsY = []
	average_centroidY = 0
	focus_users = []
	overall_focus_user = ''
	
	for w in xrange(length_of_data):
		
		#parameters for the window starting at w 
		window_dispersions = []
		window_average_dispersion = 0
		window_centroidsX = []
		window_average_centroidX = 0
		window_centroidsY = []
		window_average_centroidY = 0
		window_focus_users = []
		window_overall_focus_user = ''
			
		subdata = coordinates[w:w + data_points_in_window] #window data points
		#print subdata
				
		for l in range(len(subdata)):
			
			disp = 0
		
			#for one frame in a window
			Xs = []
			Ys = []
		
			cX = 0
			cY = 0
			
			for s in range(group_size*2):
				
				#even indices X
				#odd indices Y
				
				if(s%2 == 0):
					Xs.append(subdata[l][s])
					cX += subdata[l][s]
				else:
					Ys.append(subdata[l][s])
					cY += subdata[l][s]
				
			cX = cX / group_size
			cY = cY / group_size
					
			#print group_size, subdata[l], cX, cY
			
			cUser = find_user_closest_to_centroid(cX, cY, group_size, subdata[l]) #in one frame
			
			window_focus_users.append(group_users[cUser])
	
			window_centroidsX.append(cX)
			window_centroidsY.append(cY)
		
			argxmin = np.min(Xs)
			argxmax = np.max(Xs)
			
			argymin = np.min(Ys)
			argymax = np.max(Ys)

			#print argxmax, argxmin, argymax, argymin
		
			disp = ((argxmax - argxmin) + (argymax - argymin))/2
			#TODO: look for other ways of calculating dispersion
		
			window_dispersions.append(disp)
			
		
		window_average_dispersion = sum(window_dispersions) / len(window_dispersions)
		window_average_centroidX = sum(window_centroidsX) / len(window_centroidsX)
		window_average_centroidY = sum(window_centroidsY) / len(window_centroidsY)
		
		dispersions.append(window_average_dispersion)
		centroidsX.append(window_average_centroidX)
		centroidsY.append(window_average_centroidY)
		
		most_frequent_focus_user_in_the_window = [user for user, user_count in Counter(window_focus_users).most_common(1)]
		
		focus_users.extend(most_frequent_focus_user_in_the_window) 
	
	average_dispersion = sum(dispersions) / len(dispersions)
	average_centroidX = sum(centroidsX) / len(centroidsX)
	average_centroidY = sum(centroidsY) / len(centroidsY)
	
	most_frequent_focus_user_overall = [user for user, user_count in Counter(focus_users).most_common(1)][0] #index [0] added so that the variable is int not list
		
	return dispersions, average_dispersion, centroidsX, average_centroidX, centroidsY, average_centroidY, focus_users, most_frequent_focus_user_overall	
	
def get_group_dispersion_results(data, users, groups, group_sizes, numbers_of_questions, data_points_in_window):

	#dispersion in windows
	#sliding/moving windows (like a queue of data points) 1-5 2-6 3-7 etc.
	#centroid in windows
	#user closest to the centroid
	
	#average values over all the windows
	
	results = ''
	
	for i in range(len(groups)):
		#print groups[i], " ", numbers_of_questions[i]	
		
		#get the users belonging to a given group
		group_users = get_users_in_a_group(users, groups[i])
		group_size = group_sizes[i]
		
		for n in range(1,(numbers_of_questions[i]) + 1):
		
			resultsToString = '\n'
		
			#in the real data length sometimes differs across users
			#ASSUMPTION: same-sized data for all the users belonging to a group and answering the same question
					
			length_of_data = get_length_of_subset(data, n, group_users[0]) #just one user in that group 
			
			group_coordinate_data = np.zeros((length_of_data,group_size*2))
			
			for u in range(group_size):
				
				subset = get_subset(data, n, group_users[u])
				
				for l in range(length_of_data):
				
					# u 0 -> 0 and 1
					# u 1 -> 2 and 3
					# u 2 -> 4 and 5
					# and so on
					# places x and y coordinates into the 2d numpy array
					group_coordinate_data[l][u*2] = subset[l][x]
					group_coordinate_data[l][u*2 + 1] = subset[l][y]
					
								
			dispersions, average_dispersion, centroidsX, average_centroidX, centroidsY, average_centroidY, focus_users, overall_focus_user = calculate_group_dispersion(group_coordinate_data, group_size, group_users, length_of_data, data_points_in_window, group_users)
				

			resultsToString += "Group " + groups[i] + " Question " + str(n) + "\n" 
			resultsToString += "Average dispersion " + str(average_dispersion) + " Average X " + str(average_centroidX) + " Average Y " + str(average_centroidY) + "\n"
			resultsToString += "User closest to centroid " + overall_focus_user + "\n"
		
			resultsToString += "\nDispersions per window \n"
			
			for s in range(len(dispersions)):
			
				resultsToString += str(dispersions[s]) + "\n"
			
			resultsToString += "\nX-Y coordinates of centroids per window \n"
			
			for s in range(len(centroidsX)):
			
				resultsToString += str(centroidsX[s]) + " " + str(centroidsY[s]) + "\n"
				
			resultsToString += "\nUsers closest to the centroid per window\n"
			
			for s in range(len(focus_users)):
			
				resultsToString += focus_users[s] + "\n"
				
			results += resultsToString + "\n"		
						
			
	return results