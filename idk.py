# ( Don't worry so loud, your roommate )
# ( can't think.                       )
#  ------------------------------------
#         o   ^__^
#          o  (00)\_______
#             (__)\       )\/\
#                 ||----w |                 
#                 ||     ||

import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt("pH.txt",skiprows=1)
extra = np.loadtxt("pH.txt", usecols=range(3,1287))
data = data.T
row1 = extra[0,:].T

##############################################
###               Analysis                 ###
##############################################

data[1,-1] = 0.
data[1,:] = np.roll(data[1,:],1)
deltaV = data[1,1] - data[1,0] 

data[2,0] = data[2,1] * .99

v1 = input("What is the initial volume?\n")
print " "

v = data[1,:]
df = (v1 + v) / v1
data[1,:] = data[1,:]*df

##############################################
###               User input               ###
##############################################

metal_1 = raw_input(
        "What is the name of the metal used?\n" )

mc = input(
        "What is the concentration of " +metal_1+ "?\n" )

ligand_1 = raw_input(
        "What is the name of the ligand used?\n" )

lc = input(
        "What is the concentration of " +ligand_1+ "?\n" ) 

more = raw_input(
        "Is there another other metal and ligand concentrations?\n"
        "Type yes or no.\n")

if more == 'yes':
    metal_2 = raw_input(
         "What is the name of the metal used?\n" )
         
    mc_2 = input(
         "What is the concentration of " +metal_2+ "?\n" )
 
    ligand_2 = raw_input(
         "What is the name of the ligand used?\n" )
    lc_2 = input(
         "What is the concentration of " +ligand_2+ "?\n" )

#############################################
###                Output                 ###
#############################################

points = data[0,:].astype(int)
Id = np.append('id', points)

p = np.full(237, 1, dtype=int)
path = np.append('path', p)

pH = np.append('pH', data[2,:])

spectra = np.hstack((row1, data[3:,:]))
print data[3:,:].shape
print spectra.shape

c1 = np.full(237, mc, dtype="float64")
M1 = np.append('Total M', c1)

lc1 = np.full(237, lc, dtype="float64")
L1 = np.append('Total M', lc1)

if more == 'yes':
    c2 = np.full(237, mc_2, dtype="float64")
    M2 = np.append('Total M', c2)
    
    lc2 = np.full(237, lc_2, dtype="float64")
    L2 = np.append('Total M', lc2)

exit()
array_size = data[0,:].size
np.set_printoptions(threshold=array_size)
np.savetxt('dum.txt', data)
