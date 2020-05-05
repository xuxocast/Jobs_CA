## This program show the most demanded jobs per location (independent of date)
## Also provides time series of job demand by sector in the state of CA 

import os
from csv import reader
import matplotlib.pyplot as plt
import statistics as st
import collections 
from scipy.stats.stats import pearsonr

os.getcwd()

file = "temp_datalab_records_job_listings.csv"

N = 100000  # Only first 100k cases


def num(a):
	 if a == '':
	 	return 1
	 else:
	 	return float(a)

def Read(FILE,I): 
	i=0 
	L=[] 
	with open(FILE) as FF: 
	    while i < I: 
	        line = FF.readline()
	        a = [line]
	        for l in reader(a):
    	             L.append(l) 
	        i+=1 
	return L

data = Read(file,N)

for i in range(1,N):  
	   dl = len(data[0]) - len(data[i])
	   while dl > 0:
	     	  data[i].append(0)                     #Fill with zeros to match lenght
	     	  dl = dl - 1



############################################################################

# 4  title job
# 9 locality state
# 11 number_of_openings
# 14 	 posted_date 
# 3 	 as_of_date 	

match_state = ["CA", "California"]

match_Sofware_data = ["Web","Software","Android","iOS"]
match_Engineer_Sci = ["Engineer","Analyst","Research","Scientist"]
match_Health = ["Health","Medic","Nurse","Nursing"]
match_Sales = ["Sales","Marketing","Merchandise","Business","Manager"]
match_deaths = ["Funeral","Crematory"]


CA = []

for i in range(1,N):
	if isinstance(data[i][9], str)  and  any(x in data[i][9] for x in match_state) :   #ignore data without location
	    CA.append([data[i][4],data[i][14],data[i][11]])



def TimeSeries(match):
    JJ=[]
    for i in range(len(CA)):
	    nn = num(CA[i][2])
	    if any(x in CA[i][0] for x in match) and CA[i][1] != '':   #ignore data without location
             nn = num(CA[i][2])
             date = CA[i][1]
             date = int(date.split('-')[0]) - 2000 + 1.2/int(date.split('-')[1])        ## Date by month,  may change
             JJ.append( {date:nn} )
    count_jj = collections.Counter()
    for d in JJ: 
         count_jj.update(d)
    d_jj = dict(count_jj) 
    d_jj = dict(sorted(d_jj.items(), key=lambda t: t[0]))
    return d_jj




d_j1 = TimeSeries(match_Sofware_data)
d_j2 = TimeSeries(match_Engineer_Sci)
d_j3 = TimeSeries(match_Health)
d_j4 = TimeSeries(match_Sales)
d_j5 = TimeSeries(match_deaths)


x1,y1 = list(d_j1.keys()),list(d_j1.values())
x2,y2 = list(d_j2.keys()), list(d_j2.values())
x3,y3 = list(d_j3.keys()),list(d_j3.values())
x4,y4 = list(d_j4.keys()), list(d_j4.values())
x5,y5 = list(d_j5.keys()),list(d_j5.values())


plt.plot(x1,y1,'-o')
plt.plot(x2,y2,'-o')
plt.plot(x3,y3,'-o')
plt.plot(x4,y4,'-o')
plt.plot(x5,y5,'-o')
plt.ylabel('Job demand in CA')
plt.xlabel('Date [y]')


plt.legend(['Soft dev', 'Eng&Sci', 'Health', 'Sales', 'Defunction'], loc='upper left')

plt.show()


