#using numpy arrays
import os
import PySpin
import numpy
import matplotlib.pyplot as plt
import time
import datetime
from PIL import Image
from numpy import array, empty, ravel, where, ones, reshape, arctan2
from matplotlib.pyplot import plot, draw, show, ion
from datetime import date


#User input of which Data folder they desire
Folder_Name = input("Enter the name of the file you wish to retrieve the images from: ") #Folder_Name in some previous save_aquire (versions newer than 191216)

#Find number of numpy array files within 'Folder_Name'
Data_dir = 'C:/Users/localadmin/Desktop/Phase_Camera_Images/Data/'
data_path = os.path.join(Data_dir,Folder_Name)
NUM_IMAGES_list = os.listdir(data_path) #Num(instensity images)=Num(numpy arrays), not the number of phase maps
NUM_IMAGES = len(NUM_IMAGES_list)
print("Number of intensity image numpy arrays present in " + Folder_Name + " is: ", NUM_IMAGES)

picList = []
NOVAK_PHA_PLT =[]	

#open image arrays 
for i in range(NUM_IMAGES):
	imgName = data_path +"/" + Folder_Name + '_%d.npy' % i
	IMG = numpy.load(imgName)
	picList.append(IMG)
	
		
#average carre phase map
FPP_avg = numpy.empty(388800)
carre_no_Mask = numpy.empty(388800) #maybe later. compare to mask
c = 0

for i in range(NUM_IMAGES):	
	if i % 8 == 0 and i > 0:  #MAKE SURE OVERLAP IS RIGHT... (%8 FOR NOVAK, %4 FOR 4P AND CARRE)
		c += 1
		#phase of each pixel, assuming: list of five images read in, equally centered and sized
		arr1 = numpy.ravel(numpy.array(picList[0],dtype='int'))
		arr2 = numpy.ravel(numpy.array(picList[1],dtype='int')) #converts to numpy arrays for faster operation
		arr3 = numpy.ravel(numpy.array(picList[2],dtype='int'))
		arr4 = numpy.ravel(numpy.array(picList[3],dtype='int'))
		arr5 = numpy.ravel(numpy.array(picList[4],dtype='int'))
		phase = numpy.empty(388800)

		mask = numpy.ones(388800,dtype=bool)

		cuts = numpy.where(arr1 < 15)

		mask[cuts] = False

		p1 = arr1[mask]
		p2 = arr2[mask]
		p3 = arr3[mask]
		p4 = arr4[mask]
		p5 = arr5[mask]	

		den = 2*p3-p1-p5

		A = p2-p4

		B = p1-p5

		num = numpy.sqrt(abs(4*A**2-B**2))

		pm = numpy.sign(A)

		pha = numpy.arctan2(pm*num,den)

		phase[~mask] = 0
		phase[mask] = pha
		
		FPP_avg += phase

	
FPP_avg = FPP_avg / c 
FPP_avg = numpy.reshape(FPP_avg,(540,720))

plt.ion()						
plt.imshow(FPP_avg, cmap = 'jet')
cbar = plt.colorbar()#
plt.clim(vmin=-numpy.pi,vmax=numpy.pi)#
cbar.set_label("Phase Shift (rad)")#
plt.xlabel("Pixels(x)")
plt.ylabel("Pixels(y)")
plt.xlim([250,500])
plt.ylim([450,200])
plt.pause(0.00001)

today=date.today()
d1 = today.strftime("%Y%m%d")	

phase_map_name = 'C:/Users/localadmin/Desktop/Phase_Camera_Images/phase_maps/' + Folder_Name + '_' + d1  + '_Novak.png' 
plt.savefig(phase_map_name)
plt.show()
plt.clf()

print("phase map saved at:", phase_map_name)