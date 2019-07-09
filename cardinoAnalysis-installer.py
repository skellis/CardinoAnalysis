"""
.. module: cardinoAnalysis-installer
   :platform: Windows
.. moduleauthor:: Scott R. Ellis <skellis@gmail.com>
   This file is an installer of the libraries required to run the cardinoAnalysis
   If your python libraries are too old or too new many of the functions 
   will break. Thus we recommend staying with these versions.
   

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   You should have received a copy of the GNU General Public License
   along with this program. If not, see <http://www.gnu.org/licenses/>.
   Copyright 2014-2016 Daniel Dietze <daniel.dietze@berkeley.edu>.
"""

import os

def installNumpy():
	try:
		import numpy as np
		npversion= np.version.version
		if npversion == "1.16.4":
			print "numpy version is up to date."
		else:
			print "scipy version is up not preferable for this software. Installing version 1.16.4:"
			os.system("pip install -U numpy==1.16.4")

	except ImportError:
		print "numpy is not installed. Installing version 1.16.4:"
		os.system("pip install -U numpy==1.16.4")




def installMatplotlib():
	try:
		import matplotlib
		matplotlibversion= matplotlib.__version__
		if matplotlibversion == "3.1.0":
			print "matplotlib version is up to date."
		else:
			print "matplotlib version is up not preferable. Installing version 3.1.0:"
			os.system("pip install -U matplotlib==3.1.0")
	except ImportError:
		print "matplotlib is not installed. Installing version 3.1.0:"
		os.system("pip install -U matplotlib==3.1.0")



installNumpy()
installMatplotlib()
installpyDAQmx()
print "-If all packages installed correctly run 'python exampleCardinoAnalysis.py