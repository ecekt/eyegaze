# eyegaze

maingaze.py is the main file to call.
gaze.py includes implementations for the I-DT and I-VT algorithms. 

Data can be downloaded from this link: https://github.com/mani-tajaddini/The-Group-Eye-Tracking-Project/tree/master/Lottary%20Experiment-raw

Example command:
python maingaze.py "raw_decision.csv" 100 20 300 "fix.txt" "group.txt"

Arguments:
python maingaze.py [data file] [velocity threshold] [dispersion threshold] [fixation duration threshold] [file to write fixation info] [file to write group info]

 Velocity threshold in pix/sec <br />
 Dispersion threshold in pixels <br />
 Fixation duration threshold in pix/msec <br />

**TODO:**
* Unit conversions
* Check precision loss, 0.0 velocity cases
* Remove redundant type-casting
* Dispersion calculation methods
* Find out meaningful thresholds
