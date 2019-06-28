import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)

def loadCardinoData(filename,columns="all",**keyword_parameters):
	"""
	A module for loading the Cardino data. The dictionary allows for rapid idexing of the desired data type.
	The timestamp data can be easily acquired too through use of the keyword parameters
	
	filename- string - the path to the desired data file.

	columns - string - the name of the data you want to read. To be looked up in the dictionary colDict.
	"all" returns all the data
	"timestamp" returns the time data.

	colDict={"all":range(78),
	"TimeStamp":(0),
	"Taus":(1,2),#NOTE!!! The O3 and NO2 ringdown times (Tau_O3) are not being written as of June 27 2019!!!!
	"Pressures":range(14,24),
	"Cavity Pressures":range(21,24),
	"Line Pressures":(14,16),
	"Tank Pressures":(15,17),
	"Temperatures":range(8,12),
	"Cavity Temperatures":range(8,11),
	"States":range(3,5),
	"Laser Currents":(6,7),
	"MFC":range(34,61),
	"MFC A":range(34,37),
	"Valves":range(25,33),
	"Setpoints":range(61,68),
	"Heaters":range(70,72),
	"Dongle":range(73,75),
	"TC4 O3 Cavity (°C)":(11)
	
	Keyword_parameters - includeTime - Optional parameter for getting the timeStamp in addition to a
	Keyword_parameters - manualCol - Optional parameter for manually selecting which columns you want.
	Keyword_parameters - skipHead - Optional parameter for skipping the initial rows of the data file


	Examples:
	******************
	o3cav_data=loadCardinoData("2019_06_26 14_30_56 CARDINO.csv",columns="TC4 O3 Cavity (°C)")
	all_data=loadCardinoData("2019_06_26 14_30_56 CARDINO.csv")
	time_Data,allTemperature_data=loadCardinoData("2019_06_26 14_30_56 CARDINO.csv",columns="Temperatures",includeTime=True)
	time_Data,humidity_Data=loadCardinoData("2019_06_26 14_30_56 CARDINO.csv",manualCol=(13),includeTime=True)
	time_Data=loadCardinoData("2019_06_26 14_30_56 CARDINO.csv",columns="TimeStamp")
	"""
	#makes sure your formatted your file name correctly
	if(filename[-4:]!=".csv"):
		filename+=".csv"
		print("File must be a .csv. Searching for :"+filename+"...")

	#The indicies of this dictionary will fail whenever you change the format of the .csv data file.
	#What follows is only an example of how a the data can groups easily.
	#These column indicies can be referenced manually outside this module by using a keyword parameter. 
	#deal with optional parameters.
	dataType="float"
	tpls=False
	if ('includeTime' in keyword_parameters):
		tpls=True
	elif (columns=="TimeStamp"):
		dataType="str"

	colDict={"all":range(78),
	"TimeStamp":(0),
	"Taus":(1,2),#NOTE!!! The O3 and NO2 ringdown times (Tau_O3) are not being written as of June 27 2019!!!!
	"Pressures":range(14,24),
	"Cavity Pressures":range(21,25),
	"Line Pressures":(14,16),
	"Tank Pressures":(15,17),
	"Temperatures":range(8,12),
	"Cavity Temperatures":range(8,11),
	"States":range(3,5),
	"Laser Currents":(6,7),
	"MFC":range(34,61),
	"MFC A":range(34,37),
	"Valves":range(25,33),
	"Setpoints":range(61,68),
	"Heaters":range(70,72),
	"Dongle":range(73,75),
	"TC4 O3 Cavity (°C)":(11),
	"ZeroData":range(4,5)
	}

	#You can overide the dictonary indicies by using manualCol Keyword.
	if ('manualCol' in keyword_parameters):
		colRange=keyword_parameters['manualCol']
	else:
		colRange=colDict[columns]

	#We want to skip the header when extracting the data.
	#Note on ocassion he first 3 row of the .csv file were missing columns. If this is detected skipHead=5 is advisable.
	if ('skipHead' not in keyword_parameters):
		skipHead=1
	if 1:
		#let's start not reading whole file
		max_rows=20

	d=np.genfromtxt(filename ,dtype=dataType,skip_header=skipHead,delimiter=",",missing_values=np.nan,usecols=(colRange),autostrip=True)
	if (tpls):
		t= np.genfromtxt(filename ,dtype="str",skip_header=skipHead,delimiter=",",missing_values=np.nan,usecols=0,autostrip=True)
		return t,d
	else:
		return d


def formatTime(timeStamp):
	#seconds in months + seconds in days +seconds in hours + seconds in minutes + seconds
	#sample TimeStamp:    2019.06.26 14:56:14.08
	tz=float(timeStamp[0][5:7])*365.25/12*24*60*60+float(timeStamp[0][8:10])*24*60*60+float(timeStamp[0][11:13])*60*60+float(timeStamp[0][14:16])*60+float(timeStamp[0][17:19])+float(timeStamp[0][20:22])/100
	ty=np.zeros(len(timeStamp))
	for i in range(len(timeStamp)):
		ty[i]=float(timeStamp[i][5:7])*365.25/12*24*60*60+float(timeStamp[i][8:10])*24*60*60+float(timeStamp[i][11:13])*60*60+float(timeStamp[i][14:16])*60+float(timeStamp[i][17:19])+float(timeStamp[i][20:22])/100
	ts=np.subtract(ty,tz)
	return ts


def plotCardino(timepoints,data,ylabel="Parameter (Unspecified Units)",title="Cardino Data",saveloc="",dataLabels=""):
	"""
	Example:
	-----------------------------------
	plotCardino(time_Series,humidity_Data,title="Humidity Sensor", ylabel="% Humidity")
	plotCardino(time_Series,cavityPressure_Data,title="Cavity Pressure", ylabel="Pressure (mbar)",dataLabels=["N2O5","NO3","NO2","O3"])
	plotCardino(time_Series,allTemperature_data,saveloc="plotAllTemperatures.png")


	
	"""
	fig, (ax) = plt.subplots(1, 1, sharex=True,constrained_layout=True)
	fig.suptitle(title)
	print(len(dataLabels))
	if (len(dataLabels)!=0 and len(dataLabels)!=np.shape(data)[1]):
		print("Your data label must be a list of strings with the same length as data")
	elif (len(dataLabels)==np.shape(data)[1]):
		for i in range(np.shape(data)[1]):
			ax.plot(timepoints,data[:,i],label=dataLabels[i])
	else:
		for i in range(np.shape(data)[1]):
			ax.plot(timepoints,data[:,i],label='parameter '+str(i))
	ax.set_xlabel('Time (s)')
	ax.set_ylabel(ylabel)
	ax.legend()
	if (saveloc!=""):
		plt.savefig(saveloc)
	else:
		plt.show()