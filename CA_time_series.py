## This program provides time series of job demand by sector in the state of CA 
## The correlation with time series of seismic activity will be work to do...

## Example of the output plot in "Jobs_CA.png"

import os
from csv import reader
import collections 
import urllib.request
from datetime import datetime, timedelta
import sys

os.getcwd()

file1 = "temp_datalab_records_job_listings.csv" # Job Postings data from Thinknum
file2 = "temp_datalab_records_job_listings2.csv" 
file3 = "temp_datalab_records_job_listings3.csv" 
file4 = "temp_datalab_records_job_listings4.csv" 

MM = 3  #Magnitude of seismic events

#Function create string to call the usgs server
def UrlData(sdate,fdate,Mag):
    asd = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=text&starttime={}&endtime={}&minmagnitude={}"
    return asd.format(sdate,fdate,Mag)

#Read URL file 
def ReadU(link):
    L = []
    UF = urllib.request.urlopen(link)
    FF = UF.read().splitlines()
    for i in range(len(FF)):
        l = FF[i].decode("utf-8").strip()
        L.append(l)
    return L


#Converts '' to float zero
def fnum(stri):
	if stri == '':
		return 0
	else:
		return float(stri)

#Converts '' to 1 (job openings)
def num(a):
	 if a == '' :
	 	return 1
	 else:
	 	return float(a)


############################################################################
# DATA
# 4  title job
# 9 locality state
# 11 number_of_openings
# 14 	 posted_date 
# 3 	 as_of_date 	

# Creates key-word strings to match services and state
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


# Saves the jobs in CA
CA = []

#Get N lines
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


#N = file_len(file)
###################################################################################
# Read N lines from file
def Read(FILE,I): 
	i=0 
	L=[] 
	with open(FILE) as FF: 
		while i < I: 
			line = FF.readline()
			a = [line]
			LL = []
			for l in reader(a):
				LL.append(l)
			if any(x in LL[0] for x in match_state):
				L.append(LL[0])
			i+=1
	return L 



def fixlen(arr):
	for i in range(len(arr)):  
		dl = 24 - len(arr[i])
		while dl > 0:
			arr[i].append(0)                     #Fill empty entries with zeros to match lenght
			dl = dl - 1
	return arr






############################################################################
N=65000000

print(N)
data = Read(file1,N)
data=fixlen(data)


for i in range(len(data)):
	if isinstance(data[i][9], str) and  data[i][14] != '':   #ignore data without location or date and filter bad format
		CA.append([data[i][4],data[i][14],data[i][11]])

del data



print(N)
data = Read(file2,N)
data=fixlen(data)


for i in range(len(data)):
	if isinstance(data[i][9], str) and  data[i][14] != '':   #ignore data without location or date and filter bad format
		CA.append([data[i][4],data[i][14],data[i][11]])

del data


print(N)
data = Read(file3,N)
data=fixlen(data)


for i in range(len(data)):
	if isinstance(data[i][9], str) and  data[i][14] != '':   #ignore data without location or date and filter bad format
		CA.append([data[i][4],data[i][14],data[i][11]])

del data


print(N)
data = Read(file4,N)
data=fixlen(data)


for i in range(len(data)):
	if isinstance(data[i][9], str) and  data[i][14] != '':   #ignore data without location or date and filter bad format
		CA.append([data[i][4],data[i][14],data[i][11]])

del data

# CA
# 0 title job
# 1 date
# 2 n opennings

# DATA
# 4  title job
# 9 locality state
# 11 number_of_openings
# 14 	 posted_date 
# 3 	 as_of_date 	

#############################################################################


#Creates directory "time series" of jobs per sector
def Time_Jobs(match):
    JJ=[]
    for i in range(len(CA)):
	    nn = num(CA[i][2])
	    if any(x in CA[i][0] for x in match) and CA[i][1] != '':   #ignore data without location
             nn = num(CA[i][2])
             date = CA[i][1]
             JJ.append( {date:nn} )
    count_jj = collections.Counter()
    for d in JJ: 
         count_jj.update(d)
    d_jj = dict(count_jj) 
    d_jj = dict(sorted(d_jj.items(), key=lambda t: t[0]))
    return d_jj



d_j1 = Time_Jobs(match_Sofware_data)
d_j2 = Time_Jobs(match_Engineer_Sci)
d_j3 = Time_Jobs(match_Health)
d_j4 = Time_Jobs(match_Sales)
d_j5 = Time_Jobs(match_Mortuary)
d_j6 = Time_Jobs(match_Administration)
d_j7 = Time_Jobs(match_Building)
d_j8 = Time_Jobs(match_Services)
d_j9 = Time_Jobs(match_Customer)



## Function to manipulate dates

def string_to_date(string):
	ini = string.split('-')
	ini = datetime(int(ini[0]),int(ini[1]),int(ini[2]))
	return ini

def date_to_string(datei):
	dd =  datei.isoformat(' ').split()[0]
	return dd

## Creates list of dates, for request to URL server (server only allows 20k lines/call, multiple calls are needed)




dates=[]
def DATES(delta):
	ini = datetime(2015,1,1)
	for i in range(60):
		ifi = ini + timedelta(days=delta)  
		dates.append([ini.isoformat(' ').split()[0],ifi.isoformat(' ').split()[0]])
		ini = ini + timedelta(days=delta+1)

DATES(30)

datei=dates[0][0]
datef=dates[len(dates)-1][1]
print(datei,datef)
print()



# Call the server to obtain the data of seismic events in CA (Match) in the dates defined by 'DATES'
# and with a magnitud bigger than 'Mag' and saves it in CA_Seismic
CA_Seismic=[]
def Seismic_match(Match,Mag):
	for j in range(len(dates)):
		ini = dates[j][0]
		ifi = dates[j][1]
		url = UrlData(ini,ifi,Mag)
		data = ReadU(url)
		N = len(data)
		field = [data[k].split("|") for k in range(N)]
		for i in range(1,N):
			if isinstance(field[i][12], str)  and  any(x in field[i][12] for x in Match) :   #ignore data without location
				a = field[i][1].split('-')
				d = [a[0],a[1],a[2].split('T')[0]]
				d =  '-'.join(d)
				CA_Seismic.append([d,fnum(field[i][10])])
		del field, data, url

Seismic_match(match_state,MM)


#Count the number of events per date and creates dictionary 
def N_Events(CA_S):
    NN = []
    for i in range(len(CA_S)):
         NN.append({CA_S[i][0]:1})
    count_nn = collections.Counter()
    for d in NN: 
        count_nn.update(d)
    d_nn = dict(count_nn) 
    d_nn = dict(sorted(d_nn.items(), key=lambda t: t[0]))
    return d_nn

dn = N_Events(CA_Seismic)



# Creates Time series list per day, starting at dateini and ending (not including) detefi
def Time_Series(str_dateini,str_datefi, d_JJ_in):
	ini = string_to_date(str_dateini)
	fi = string_to_date(str_datefi)
	
	day = ini
	d_JJ_out = []

	while day < fi:
		sday = date_to_string(day)
		if any(x == sday for x in d_JJ_in.keys() ):
			d_JJ_out.append(d_JJ_in[sday])
		else:
			d_JJ_out.append(0)
		day = day + timedelta(days=1)
	return d_JJ_out

def DAYS(str_dateini,str_datefi):
	ini = string_to_date(str_dateini)
	fi = string_to_date(str_datefi)
	
	day = ini
	JJ=[]
	while day < fi:
		sday = date_to_string(day)
		sday = sday.split('-')
		sday = [int(x) for x in sday]
		sday = sday[0] + (sday[1]-1)/12. + sday[2]/365
		JJ.append(sday)
		day = day + timedelta(days=1)
	return JJ

n_day = DAYS(datei,datef)


D_J1 = Time_Series(datei,datef,d_j1)
D_J2 = Time_Series(datei,datef,d_j2)
D_J3 = Time_Series(datei,datef,d_j3)
D_J4 = Time_Series(datei,datef,d_j4)
D_J5 = Time_Series(datei,datef,d_j5)
D_J6 = Time_Series(datei,datef,d_j6)
D_J7 = Time_Series(datei,datef,d_j7)
D_J8 = Time_Series(datei,datef,d_j8)
D_J9 = Time_Series(datei,datef,d_j9)

D_NN = Time_Series(datei,datef,dn)



original = sys.stdout

with open("TimeSeries.dat", 'w') as filehandle:
	# set the new output channel
	sys.stdout = filehandle
	
	print(datei,datef)
	print()

	print("day",',',"N_events",',',"N_sec1",',',"N_sec2",',',"N_sec3",',',"N_sec4",',',"N_sec5",',',"N_sec6",',',"N_sec7",',',"N_sec8",',',"N_sec9")
	for i in range(len(D_J1)):
		print(n_day[i],',',D_NN[i],',',D_J1[i],',',D_J2[i],',',D_J3[i],',',D_J4[i],',',D_J5[i],',',D_J6[i],',',D_J7[i],',',D_J8[i],',',D_J9[i])
     
	# restore the old output channel
	sys.stdout = original




