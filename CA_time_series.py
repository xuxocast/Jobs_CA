## This program provides time series of job demand by sector in the state of CA 
## The correlation with time series of seismic activity will be work to do...

## Example of the output plot in "Jobs_CA.png"

import os
from csv import reader
import collections 
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr

os.getcwd()

file = "temp_datalab_records_job_listings.csv" #1/7 Job Postings data from Thinknum

N = 10000000  # For now only first 10M lines 


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
	     	  data[i].append(0)                     #Fill empty entries with zeros to match lenght
	     	  dl = dl - 1

############################################################################

# 4  title job
# 9 locality state
# 11 number_of_openings
# 14 	 posted_date 
# 3 	 as_of_date 	

match_state = ["CA", "California"]

match_Sofware_data = ["Web","Software","Android","iOS","Developer"]
match_Engineer_Sci = ["Engineer","Analyst","Research","Scientist", "Professor"]
match_Health = ["Health","Medic","Nurse","Nursing"]
match_Sales = ["Sales","Marketing","Market","Merchandise","Business","Product"]
match_Mortuary = ["Funeral","Crematory"]
match_Administration = ["Administrative","Manager","Logistics","Accountant","Operations","Revenue"]
match_Building = ["Architect","Construction"]
match_Services = ["Receptionist","Maintenance","Shift","Cashier"]
match_Customer = ["Customer","Client"]

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
             date = (int(date.split('-')[0]) - 2000 + 1.2/int(date.split('-')[1]))+2000        ## Date by month, best sampling to find later
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
d_j5 = TimeSeries(match_Mortuary)
d_j6 = TimeSeries(match_Administration)
d_j7 = TimeSeries(match_Building)
d_j8 = TimeSeries(match_Services)
d_j9 = TimeSeries(match_Customer)


def listing(dd):
	x,y = list(dd.keys()),list(dd.values())
	return x,y


x1,y1=listing(d_j1)
x2,y2=listing(d_j2)
x3,y3=listing(d_j3)
x4,y4=listing(d_j4)
x5,y5=listing(d_j5)
x6,y6=listing(d_j6)
x7,y7=listing(d_j7)
x8,y8=listing(d_j8)
x9,y9=listing(d_j9)


plt.plot(x1,y1,'-o')
plt.plot(x2,y2,'-o')
plt.plot(x3,y3,'-o')
plt.plot(x4,y4,'-o')
plt.plot(x5,y5,'-o')
plt.plot(x6,y6,'-o')
plt.plot(x7,y7,'-o')
plt.plot(x8,y8,'-o')
plt.plot(x9,y9,'-o')
plt.ylabel('Jobs demand in CA')
plt.xlabel('Year')


plt.legend(['Soft dev', 'Eng&Sci', 'Health', 'Sales', 'Mortuary', 'Admin','Building','Services','Costumer'], loc='upper left')

plt.yscale('log')

plt.show()

del data, CA, d_j1,d_j2,d_j3,d_j4,d_j5  
del x1,x2,x3,x4,y1,y2,y3,y4,x5,y5
