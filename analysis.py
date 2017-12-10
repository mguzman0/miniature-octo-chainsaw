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

fname_in = raw_input(
              "What is the name of the input file?\n")
print " "
fname_out = raw_input(
              "And what do you want to name output file? \n")
print " "

data = np.loadtxt(fname_in, skiprows=1)
last = data[1,:].size
extra = np.loadtxt(fname_in, usecols=range(3,last))
data = data.T
row1 = extra[0,:].T
row1 = row1.reshape(row1.size,1)

##############################################
###               Analysis                 ###
##############################################

data[1,-1] = 0.
data[1,:] = np.roll(data[1,:],1)
deltaV = data[1,1] - data[1,0] 

data[2,0] = data[2,1] * .99

while True:
    try:
        v1 = float(raw_input("What is the initial volume?\n"))
        print " "
        break
    except ValueError:
        print "That is not a valid number. Try again...\n"
        print " "

v = data[1,:]
df = (v1 + v) / v1
data[1,:] = data[1,:]*df

##############################################
###               User input               ###
##############################################

# Ask user for concentration info
while True:
    try:
        metal_1 = raw_input(
         "What is the name of the metal used?\n" )
        print " "

        mc = float(raw_input(
         "What is the concentration of " +metal_1+ "?\n"))
        print " "

        ligand_1 = raw_input(
         "What is the name of the ligand used?\n" )
        print " "

        lc = float(raw_input(
         "What is the concentration of " +ligand_1+ "?\n")) 
        print " "
        break
    except ValueError:
        print "That is not a valid number. Start from the begining..."
        text = raw_input("Press any key to continue.\n")
        print " "

#Ask user if there are more concentrations
while True: 
    more = raw_input(
         "Are there any other metal and ligand concentrations?\n"
         "Type yes or no.\n")
    print " "
    if more == 'yes' or more == 'no':
        break
    else:
        print "Type yes or no."
        text = raw_input("Press the ENTER key to continue.")
        print " "

if more == 'yes':
    while True:
        try:
            metal_2 = raw_input(
              "What is the name of the second metal used?\n")
            print " "
         
            mc_2 = float(raw_input(
              "What is the concentration of "
                            +metal_2+ "?\n"))
            print " "
 
            ligand_2 = raw_input(
              "What is the name of the second ligand used?\n")
            print " "

            lc_2 = float(raw_input(
              "What is the concentration of "
                            +ligand_2+ "?\n"))
            print " "
            break
        except ValueError:
            print "That is not a valid number." 
            print "Start from the begining..."
            text =raw_input("Press the ENTER key to continue.\n")
            print " "

#Ask user to choose wavelengths
while True:
    wave = raw_input(("Do you want to choose the range of wavelengths?\n"
               "If \"no\" then default wavelength range will be selected.\n"
               "Type yes or no.\n"))
    print " "

    if wave == 'yes' or wave == 'no':
        break
    else:
        print "Type yes or no. Try again..."
        text = raw_input("Press the ENTER key to continue.")
        print " "

if wave == 'yes':
    while True:
        try:
            high = float(raw_input(
               "Choose range of wavelength from {} to {}.\n"
               "Insert highest wavelength first.\n"
               .format(np.amax(row1),np.amin(row1))))
            print " "
            
            if high > max(row1) or high < min(row1):
                print "Wavelength choosen is out of range."
                print "Try again..."
                print " "
            else:
                break

        except ValueError:
            print "That is not a valid number. Try again..."
            print " "
    while True:
        try:
            low = float(raw_input(
                "Insert lowest wavelength.\n"))
            print " "
            if low < min(row1) or low > max(row1):
                print "Wavelength choosen is out of range."
                print "Try again..."
                print " "
            else:
                break
        except ValueError:
            print "That is not a valid number. Try again..."
            print " "

#############################################
###                Output                 ###
#############################################

# Choosing desired wavelengths
if wave == 'yes':
    # Finds nearest value in row1 to the wavelengths choosen
    # Argument returns index
    high_indx = (np.abs(row1 - high)).argmin()
    low_indx = (np.abs(row1 -  low)).argmin()
   
    # b_idx reffers to the index of the body array.
    # body array is spectrum left in data array.
    # +3 because there are 3 more rows in data array 
    # than in row1.
    # high_indx is +1 to get the value and not the one 
    # before when slicing
    high_indx += 1
    b_idx_low = low_indx + 3   
    b_idx_high = high_indx + 3
    
    # Because the max index is +1 the index will be out of range
    # if user wants the last wavelength.
    # To avoid this error we check if high is equal to the last
    # element of the wavelength array (row1).
    if high == row1[-1]: 
        col = row1[low_indx :]
        body = data[b_idx_low :, :]

    else:
        # Slice arrays according to the nearest values
        # col reffers to the wavelength column
        col = row1[low_indx : high_indx]
        body = data[b_idx_low : b_idx_high, :]
else:
    col = row1
    body = data[3:,:]

# Organizing data write on text file
points = data[0,:].astype(int)
Id = np.append('id', points)

p = np.full(237, 1, dtype=int)
path = np.append('path', p)

pH = np.append('pH', data[2,:])

spectra = np.hstack((col, body))

c1 = np.full(237, mc, dtype="float64")
M1 = np.append('Total M', c1)

lc1 = np.full(237, lc, dtype="float64")
L1 = np.append('Total L', lc1)

if more == 'yes':
    c2 = np.full(237, mc_2, dtype="float64")
    M2 = np.append('Total M', c2)
    
    lc2 = np.full(237, lc_2, dtype="float64")
    L2 = np.append('Total L', lc2)

    out = np.vstack((Id, path, M1, L1, M2, L1, pH, spectra))
# Append Id, path, pH, Metal, Ligand concentrations and spectra
else:
    out = np.vstack((Id, path, M1, L1, pH, spectra))

np.savetxt(fname_out, out, fmt='%5s')
