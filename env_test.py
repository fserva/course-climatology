#!/usr/bin/env python

# Run this script with: `python env_test.py`

import numpy as np # library for array operations
import matplotlib.pyplot as plt # library for plotting
from mpl_toolkits.basemap import Basemap # library for maps
#import cartopy.crs as ccrs # alternative library for maps


# 'Arrays' of objects
list_int = [1,2,3]
list_str = ['a','b','c']
tupl_int = (4,5,6)

# One can change a list item (by index)
list_int[1] = 100.

# TODO Try changing a tuple value. What happens?
# ...

# TODO Try multiplying a list by 2. What happens?
# ...


# Define two arrays (range of values, or with list)
x = np.array([0.,1.,2.,3.,4.,5.,6.,7.,8.,9.])
y = np.arange(10,dtype='f') # specify type here
y *= 2. # multiply by 2


# Example of a for loop (note *indentation*)
for idx in range(len(x)):
    # Use a numpy built-in function
    y[idx] = np.sin(x[idx])**2


# Define boolean switch for plot (if True, plot is shown)
do_plot = False

# Check condition (again, note *indentation*)
if do_plot is True:  
    # Create a figure object
    plt.figure()
    # Do a line plot; if field is 2D, then contour is used
    plt.plot(x,y,color='black')
    plt.show()
 

# An example of function, with a block 
# description at the beginning
def myfunction(myvalue):
    """ Define a function with this 
    structure, as an indented block. 
    The strings in the () are the function 
    input parameters. 
    Make some calculation, then return 
    some output (migh be None) """
    myoutput = myvalue**2 # square
    return myoutput 

# Simply call any function with its name, 
# output(s) = function name (parameter1,...parameterN)
squared_value = myfunction(100)
print(squared_value)






