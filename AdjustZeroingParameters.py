import numpy as np
import matplotlib.pyplot as plt

#zeroing times (durations)
startRedZero=3.0
redZero=10.0
stopRedZero=7.0

startBlueZero=10.0
blueZero=10.0
stopBlueZero=15.0

#cycle times (periods)
redCycleTime=111.0
blueCycleTime=62.0

#delays (phases) 
redStartDelay=13.0
blueStartDelay=0.0

#Consider the sum of the zeroing times.
rzd=startRedZero+redZero+stopRedZero
bzd=startBlueZero+blueZero+stopBlueZero
netzd=rzd+bzd

#Apply restrictions to input parameters
def restrictParameters(startRedZero,startBlueZero,redZero,blueZero,stopRedZero,stopBlueZero,redCycleTime,blueCycleTime,redStartDelay,blueStartDelay):
	#total zeroing times for red andd blue channels
	adjRedCycleTime=redCycleTime
	adjBlueCycleTime=blueCycleTime

	adjRedStartDelay=redStartDelay
	adjBlueStartDelay=blueStartDelay

	tzr=startRedZero+redZero+stopRedZero
	tzb=startBlueZero+blueZero+stopBlueZero

	tznet=tzr+tzb
	#harmonic ratios to be set later
	P=0
	Q=0
	#Make sure zeroing can fit into cycle times
	if(redCycleTime<tznet):
		adjRedCycleTime=tzr+tzb+2
		print("'Red Cycle Time' increased from "+str(redCycleTime)+" (s) to "+str(adjRedCycleTime)+" fit zeroing.")
	else:
		adjRedCycleTime=redCycleTime
	if(blueCycleTime<tznet):
		adjBlueCycleTime=tzr+tzb+2
		print("'Blue Cycle Time' increased from "+str(blueCycleTime)+" (s) to "+str(adjBlueCycleTime)+" fit zeroing.")
	else:
		adjBlueCycleTime=blueCycleTime
	#Make the cycle times have harmonic periods. There should be no remainder if ratio is natural number.
	if(adjBlueCycleTime%adjRedCycleTime ==0 or adjRedCycleTime%adjBlueCycleTime ==0):
		print("No adjustment needed for harmonic periodicity.")
		if(adjBlueCycleTime/adjRedCycleTime>1):
			P= adjBlueCycleTime/adjRedCycleTime
			Q=1.0
		else:
			P=1.0
			Q=adjRedCycleTime/adjBlueCycleTime
	#Scale the bigger of the two cycle times such that they are have harmonic periods.
	elif(adjBlueCycleTime%adjRedCycleTime !=0 and adjBlueCycleTime/adjRedCycleTime>=1):
		P=np.ceil(adjBlueCycleTime/adjRedCycleTime)
		Q=1.0
		adjBlueCycleTime=P*adjRedCycleTime
		print("Blue Cycle Time was increased from " +str(blueCycleTime)+" s to "+str(adjBlueCycleTime)+" s achieve harmonic periodicity.")
	#Scale the bigger of the two cycle times such that they are have harmonic periods.
	elif(adjRedCycleTime%adjBlueCycleTime !=0 and adjRedCycleTime/adjBlueCycleTime>=1):
		P=1.0
		Q=np.ceil(adjRedCycleTime/adjBlueCycleTime)
		adjRedCycleTime=Q*adjBlueCycleTime
		print("Red Cycle Time was increased from " +str(redCycleTime)+" s to "+str(adjRedCycleTime)+" s achieve harmonic periodicity.")
	#Check if redStartPhase needs to be shifted because zeroing occurs at the same time. red Start Phase should occur after Blue Zeroing has finished.
	if(P/Q>1):
		#need to check every short period as it overlaps with the long period zero.
		overlapping=False
		slowRange=[blueStartDelay,blueStartDelay+tzb]
		for i in np.arange(P):
			fastRange=[redStartDelay+redCycleTime*i,redStartDelay+redCycleTime*i+tzr]
			print(np.amin(slowRange),fastRange[0],np.amax(slowRange))
			if(np.amin(slowRange)<=fastRange[0]<=np.amax(slowRange) or np.amin(slowRange)<=fastRange[1]<=np.amax(slowRange) or np.amin(fastRange)<=slowRange[10]<=np.amax(fastRange) or np.amin(fastRange)<=slowRange[1]<=np.amax(fastRange)):
				overlapping=True
				print(overlapping)
			else:
				print("Suitable phase selected")
		#shift the redStartPhase so that it starts immediately after blue zeroing finishs
		if(overlapping):
			adjRedStartDelay=(blueStartDelay+tzb+1)
			print("The Red Start Delay has been increased from "+str(redStartDelay)+" s to "+str(adjRedStartDelay)+" to prevent simultaneous zeroing.")
	#Check if redStartPhase needs to be shifted because zeroing occurs at the same time. red Start Phase should occur after Blue Zeroing has finished.
	elif(Q/P>=1):
		#need to check every short period as it overlaps with the long period zero.
		overlapping=False
		slowRange=[redStartDelay,redStartDelay+tzr]
		for i in np.arange(P):
			fastRange=[blueStartDelay+blueCycleTime*i,blueStartDelay+blueCycleTime*i+tzb]
			print(np.amin(slowRange),fastRange[0],np.amax(slowRange))
			if(np.amin(slowRange)<=fastRange[0]<=np.amax(slowRange) or np.amin(slowRange)<=fastRange[1]<=np.amax(slowRange) or np.amin(fastRange)<=slowRange[0]<=np.amax(fastRange) or np.amin(fastRange)<=slowRange[1]<=np.amax(fastRange)):
				overlapping=True
				print(overlapping)
		#shift the redStartPhase so that it starts immediately after blue zeroing finishs
		if(overlapping):
			adjBlueStartDelay=(redStartDelay+tzr+1)
			print("The Blue Start Delay has been increased from "+str(blueStartDelay)+" to "+str(adjBlueStartDelay)+" to prevent simultaneous zeroing.")
		else:
			print("Suitable phase selected")

	#As long as short period phase is set to start immediately after long period phase they will not overlap.
	print("Red Cycle Time:\t"+ str(adjRedCycleTime)+" (s)\tBlue Cycle Time:\t"+str(adjBlueCycleTime)+" (s)")
	print("Red Start Delay (s):\t"+ str(adjRedStartDelay)+" (s)\tBlue Start Delay (s):\t"+str(adjBlueStartDelay)+" (s)")
	return adjRedCycleTime,adjBlueCycleTime,adjRedStartDelay,adjBlueStartDelay

def plotZeroingTimeseries(tzr,tzb,rct,bct,rsd,bsd, sp=0,ep=600,dt=1,title="Zeroing Plot",saveloc=""):
	t=np.arange(sp,ep,dt)
	#phitr=((t+rsd)%rct)*2.0*3.1415/rct
	#phitb=((t+bsd)%bct)*2.0*3.1415/bct
	#bsp=bsd/bct*2.0*3.1415
	#rsp=rsd/rct*2.0*3.1415

	#startbp=np.ones(len(t))*bsp%(2.0*3.1415)
	#stopbp=np.ones(len(t))*(bsp+tzb/bct*2.0*3.1415)%(2.0*3.1415)
	#startrp=np.ones(len(t))*rsp%(2.0*3.1415)
	#stoprp=np.ones(len(t))*(rsp+tzr/bct*2.0*3.1415)%(2.0*3.1415)
	redZeroState=np.arange(-rsd,ep-rsd,dt)%rct<tzr
	blueZeroState=np.arange(-bsd,ep-bsd,dt)%bct<tzb

	overlap=redZeroState*blueZeroState
	fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True,constrained_layout=True)
	fig.suptitle(title)
	ax1.plot(t,redZeroState,'r',t,blueZeroState,'b')
	ax2.plot(t,overlap,'black')
	ax2.fill_between(t,overlap, facecolor='grey')
	ax2.set_xlabel('Time (s)')
	ax1.set_ylabel('Zeroing State')
	ax2.set_ylabel('Overlap of Zeroing State')
	if(saveloc!=""):
		plt.savefig(saveloc)
	else:
		plt.show()



adjRedCycleTime,adjBlueCycleTime,adjRedStartDelay,adjBlueStartDelay=restrictParameters(startRedZero,startBlueZero,redZero,blueZero,stopRedZero,stopBlueZero,redCycleTime,blueCycleTime,redStartDelay,blueStartDelay)

if(1):
	plotZeroingTimeseries(rzd,bzd,redCycleTime,blueCycleTime,redStartDelay,blueStartDelay,ep=600,title="Unadjusted Zeroing",saveloc="unadustedZeroing.png")
if(1):
	plotZeroingTimeseries(rzd,bzd,adjRedCycleTime,adjBlueCycleTime,adjRedStartDelay,adjBlueStartDelay,ep=500,title="Adjusted Zeroing",saveloc="AdjustedZeroing.png")
