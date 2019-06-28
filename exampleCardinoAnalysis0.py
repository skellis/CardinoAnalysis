import utilities as ut

time_Data=ut.loadCardinoData("2019_06_26 14_30_56 CARDINO.csv",columns="TimeStamp")
time_Series=ut.formatTime(time_Data)
humidity_Data=ut.loadCardinoData("2019_06_26 14_30_56 CARDINO.csv",manualCol=(13))
cavityPressure_Data=ut.loadCardinoData("2019_06_26 14_30_56 CARDINO.csv",columns="Cavity Pressures")
time_Data,allTemperature_data=ut.loadCardinoData("2019_06_26 14_30_56 CARDINO.csv",columns="Temperatures",includeTime=True)
ut.plotCardino(time_Series,allTemperature_data,saveloc="plotAllTemperatures.png")
ut.plotCardino(time_Series,cavityPressure_Data,title="Cavity Pressure", ylabel="Pressure (mbar)",dataLabels=["N2O5","NO3","NO2","O3"])