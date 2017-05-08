# eyegaze

*Added group dispersion analysis*

**GAZE IDENTIFICATION**
maingaze.py is the main file to call.
gaze.py includes implementations for the I-DT and I-VT algorithms, as given in http://dl.acm.org/citation.cfm?id=355028.

Data can be downloaded from this link: https://github.com/mani-tajaddini/The-Group-Eye-Tracking-Project/tree/master/Lottary%20Experiment-raw

Example command:
python maingaze.py "raw_decision.csv" 20 20 100 "fix.txt" "ivt"

Arguments:
python maingaze.py [data file] [velocity threshold] [dispersion threshold] [fixation duration threshold] [file to write fixation info] [algorithm]

Now, it is possible to select the algorithm to use through command line. (Select either "ivt" or "idt")

python maingaze.py "raw_decision.csv" 20 20 100 "fix.txt" 10 "ivt"

**GROUP DISPERSION**
Utilizing an artificial data set composed of some parts of the data used in gaze identification, this code implements an analysis of group behaviour in multi-user eye-tracking studies. 

Based on the I-DT algorithm, it is possible to detect the dispersion of users in the same frame or a window of several frames, via indicating the number of data points in a window. 

Dispersion values for each window for each group per question, are written into the file. In addition, overall dispersion values are also listed.

The output includes the coordinates of the centroids for each window and overall mean values of the X and Y coordinates of the overall centroid. 

It is also possible to observe which user was closest to the centroid in each window, as well as the user who was closest to the overall centroid.

maingroup.py is the file to call.

Example command:
python maingroup.py "artificial_group.csv" "group.txt" 5

Arguments:
python maingaze.py [data file] [file to write group info] [window size in data points]

Velocity threshold in pix/sec <br />
Dispersion threshold in pixels <br />
Fixation duration threshold in pix/msec <br />

**TODO:**
* Unit conversions
* Check precision loss, 0.0 velocity cases
* Remove redundant type-casting
* Dispersion calculation methods
* Find out meaningful thresholds
