import utilities as ut
import numpy as np
#import sys

#np.set_printoptions(threshold=sys.maxsize)
dataFilePath="2000_01_01 00_00_00 CARDINO.csv"

#load the ringdown time constants "Taus" in microseconds
tau_Data=ut.loadCardinoData(dataFilePath,columns="Taus")
#load the time stamp data
time_Data=ut.loadCardinoData(dataFilePath,columns="TimeStamp")
#format the time into a suitable timeseries array in units of seconds
time_Series=ut.formatTime(time_Data)


#The red ringdown times are in the first two columns of tau_Data
redTau_Data=tau_Data[:,0:2]
#load the flags for zeroing th red channels
redState=ut.loadCardinoData(dataFilePath,columns="Red State")
#get the median values for each zeroing event on the red channels
redZeros=ut.getZeroingAvg(redTau_Data, redState)
#Use the red zeroing flags to determine which zeroing we should use for each time point.
redZero_Array=ut.performZeroing(redZeros,redState)
#Calcuate epsilon for the two red channels in units of M
epRed=ut.calculateEpsilon(redTau_Data,redZero_Array)
#discard all the data that isn't "normal" state by converting it to np.nan.
epRed_norm=ut.selectZeroState(epRed,redState)
#Could plot this data as follows
#ut.plotCardino(time_Series,epRed_norm,ylabel="Epsilon (m)",title="Attenuation Coefficients",customLabel=['Ep N2O5','Ep NO3'],xlim=[195,560],ylim=[-1,1])


#The blue ringdown times are in the second two columns of tau_Data
blueTau_Data=tau_Data[:,2:4]
#load the flags for zeroing th blue channels
blueState=ut.loadCardinoData(dataFilePath,columns="Blue State")
#get the median values for each zeroing event on the blue channels in units of meters
blueZeros=ut.getZeroingAvg(blueTau_Data, blueState)
#Use the red zeroing flags to determine which zeroing we should use for each time point.
blueZero_Array=ut.performZeroing(blueZeros,blueState)
#Calcuate epsilon for the two red channels
epBlue=ut.calculateEpsilon(blueTau_Data,blueZero_Array)
#discard all the data that isn't "normal" state by converting it to np.nan.
epBlue_norm=ut.selectZeroState(epBlue,blueState)
#Could plot this data as follows
#ut.plotCardino(time_Series,epBlue_norm,ylabel="Epsilon (m)",title="Attenuation Coefficients",customLabel=['Ep NO2','Ep O3'],xlim=[195,560],ylim=[-1,1])

#join all the data into one array
epPurpleData=np.hstack((epRed_norm,epBlue_norm))
#create headings for the file to be exported
joined_labels= ut.joinLabels(['Time (s)','Ep N2O5','Ep NO3','Ep NO2','Ep O3'])
#Could plot the combined data as follows
#ut.plotCardino(time_Series,epPurpleData,ylabel="Epsilon (m)",title="Attenuation Coefficients",customLabel=['Ep N2O5','Ep NO3','Ep NO2','Ep O3'],xlim=[195,560],ylim=[-1,1])
ut.exportCardinoData("2000_01_01 00_00_00 Epsilon.csv",time_Series,epPurpleData[:,0],epPurpleData[:,1],epPurpleData[:,2],epPurpleData[:,3],header=joined_labels)