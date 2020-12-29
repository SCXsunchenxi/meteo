from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import numpy as np
import os
import conda
import urllib
import matplotlib as mpl
import matplotlib.pyplot as plt
conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib
os.environ["BASEMAPDATA"] = os.path.join(os.path.join(conda_dir, 'share'), 'basemap')
from mpl_toolkits.basemap import Basemap,shiftgrid,addcyclic, cm, maskoceans
import matplotlib.mlab as mlab
import pandas as pd
import time
import random
import matplotlib.gridspec as gridspec
import h5py
import re
import math

### INPUTS ###

## Filepaths ## 
# outputdir = 'C:/Users/张天航/OneDrive/桌面/OPERA/plots/' # Directory where radar plot graphics will be stored #
# prim_radar_dir = '/C:/Users/张天航/OneDrive/桌面/OPERA/data/' # Directory where OPERA radar files will be stored #
# opera_login_filepath = "C:/Users/张天航/OneDrive/桌面/OPERA_login.py" # Location login script (OPERA_login.py) #
# opera_username = "tianhang.zhang" # OPERA username #
# webdriver_path = 'C:/Users/张天航/OneDrive/桌面/geckodriver' # Location of webdriver linked to selenium package #
#############

## Filepaths ##
outputdir = 'output/plot/' # Directory where radar plot graphics will be stored #
prim_radar_dir = 'output/data/' # Directory where OPERA radar files will be stored #
opera_login_filepath = "OPERA_login.py" # Location login script (OPERA_login.py) #
opera_username = "tianhang.zhang" # OPERA username #
webdriver_path = 'geckodriver' # Location of webdriver linked to selenium package #
#############

start_date_input = '10/20/2020' # MM/DD/YYYY
end_date_input = '10/20/2020' # MM/DD/YYYY

raw_start_time = '12:00' # HH:MM
raw_end_time = '12:45' # HH:MM

urlat = 70 # Upper Right Latitude of plot
urlon = 40 # Upper Right Longitude of plot
lllat = 40 # Lower Left Latitude of plot
lllon = -15 # Lower Left Longitude of plot

# This will determine the resolution of the land /topography background for the plots# 
# A value too high may take longer to download from the server #
background_resolution = 500

dataset_name = "ARCHIVED IMAGES OF Rainfall Rate (MM/H) European radars (HDF5 format)" # Text must match exactly what is on the OPERA website #

time_delay = 5 #seconds... time delay when loading pages on OPERA website. Slower internet connections require a longer time delay

### End of inputs ###

## Function to read opera data in Python ##
def read_opera_hdf5(fname):
    """Reads hdf5 files according to OPERA conventions
    Please refer to the OPERA data model documentation :cite:`OPERA-data-model`
    in order to understand how an hdf5 file is organized that conforms to the
    OPERA ODIM_H5 conventions.
    In contrast to other file readers under :meth:`wradlib.io`, this function
    will *not* return a two item tuple with (data, metadata). Instead, this
    function returns ONE dictionary that contains all the file contents - both
    data and metadata. The keys of the output dictionary conform to the
    Group/Subgroup directory branches of the original file.
    If the end member of a branch (or path) is "data", then the corresponding
    item of output dictionary is a numpy array with actual data.
    Any other end member (either *how*, *where*,
    and *what*) will contain the meta information applying to the corresponding
    level of the file hierarchy.
    Parameters
    ----------
    fname : string
        a hdf5 file path
    Returns
    -------
    output : dict
        a dictionary that contains both data and metadata according to the
        original hdf5 file structure
    """
    f = h5py.File(fname, "r")

    # now we browse through all Groups and Datasets and store the info in one
    # dictionary
    fcontent = {}

    def filldict(x, y):
        if isinstance(y, h5py.Group):
            if len(y.attrs) > 0:
                fcontent[x] = dict(y.attrs)
        elif isinstance(y, h5py.Dataset):
            fcontent[x] = np.array(y)

    f.visititems(filldict)

    f.close()

    return fcontent

## Function to find ID's on OPERA website ##
def id_value_find(word,ext_type):
	if word == 'x-grid3-body':
		region_limit = 60
	else:
		region_limit = 100
	dummy = -1
	count_while = 0
	while dummy == -1:
		count_while = count_while + 1
		if count_while > 10:
			print ("Not found")
			break
		html_source = driver.page_source
		word_region = html_source[(html_source.find(str(word))-region_limit):(html_source.find(str(word))+region_limit)]
		key_position = word_region.find(str(ext_type))
		if key_position == -1:
			dummy = -1
		else:
			return re.sub("\D", "", str(word_region[key_position:key_position+20]) )


## Time list created in hours and minutes format int(hours), int(minutes) 
#  i.e. 1.15 (1.15am),0.30 (0.30am) ,8.0 (8am), 23.0 (11pm).
time_list = []
for  i in range(0,24):
	for j in [0,15,30,45]:
		time_list.append(str(i)+'.'+str(j))
if 'time_list' in locals():
	print ("Time List Defined")

month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']

#####
print ("Running OPERA Login")
## Login to opera website ##
exec(open(opera_login_filepath).read())
print ("Logged into OPERA")
#####

input_start_time = str(int(raw_start_time[0:2]))+'.'+str(int(raw_start_time[3:5])) #Hour.Minutes
input_end_time = str(int(raw_end_time[0:2]))+'.'+str(int(raw_end_time[3:5]))

print ("Input Start Date:", start_date_input, "-", end_date_input)
print ("Input Time:", str(raw_start_time[0:2]) + '.' + str(raw_start_time[3:5]) + "-" + str(raw_end_time[0:2]) + '.' + str(raw_end_time[3:5]))

saved_files_dir = prim_radar_dir+str(start_date_input[-4:])+'/'+str(start_date_input[:2])+'/'+str(start_date_input[3:5])+'/'

## Creating directory for download if required ##
try:
	os.makedirs(saved_files_dir)
except OSError:
	print ("ALREADY DIRECTORY")
else:
	print ("CREATED DIR: "+str(prim_radar_dir)+str(start_date_input[-4:])+'/'+str(start_date_input[:2])+'/'+str(start_date_input[3:5])+'/')

time.sleep(time_delay)

driver.find_element_by_class_name('btnXXLFixedSize').click() 

time.sleep(time_delay)

id_value = id_value_find('Date de debut','ext-comp')

start_date = driver.find_element_by_id("ext-comp-"+str(id_value))
start_date.clear()
start_date.send_keys(start_date_input) # Input date

id_value = id_value_find('Heure de debut','ext-comp')

driver.find_element_by_id("ext-comp-"+str(id_value)).click() ## Clicks on dropdown arrat for start time
moves = [Keys.DOWN] * np.where(np.array(time_list) == input_start_time)[0][0]
for i in moves:
	driver.find_element_by_id("ext-comp-"+str(id_value)).send_keys(i)
driver.find_element_by_id("ext-comp-"+str(id_value)).send_keys(Keys.ENTER)

id_value = id_value_find('Heure de fin','ext-comp')

driver.find_element_by_id("ext-comp-"+str(id_value)).click() ## Clicks on dropdown arrat for start time
moves = [Keys.UP] * ( len(time_list) - np.where(np.array(time_list) == input_end_time)[0][0] - 1 )
for i in moves:
	driver.find_element_by_id("ext-comp-"+str(id_value)).send_keys(i)
driver.find_element_by_id("ext-comp-"+str(id_value)).send_keys(Keys.ENTER)

id_value = id_value_find('Date de fin','ext-comp')

end_date = driver.find_element_by_id("ext-comp-"+str(id_value))
end_date.clear()
end_date.send_keys(end_date_input) # Input date
print ("Inputted Start and End Time")

## Save and submit request ##

id_value = id_value_find('Save</button','ext-gen')

driver.find_element_by_id("ext-gen"+str(id_value)).click()

print ("Wait 20 seconds for request to complete")
### While loop could be used here to optimse code
time.sleep(20)

#### Refreshes to get download available ~~~#

id_value = id_value_find('x-tbar-loading','ext-gen')
driver.find_element_by_id("ext-gen"+str(id_value)).click()

time.sleep(3)
## Clicks on download ###

id_value = id_value_find('x-grid3-body','ext-gen')
driver.find_element_by_id("ext-gen"+str(id_value)).click()

print ("Open download page")

time.sleep(3)
### Clicks download button ##

id_value = id_value_find('Download</button','ext-gen')

driver.find_element_by_id("ext-gen"+str(id_value)).click()

print ("Download data clicked")

### Opening request for doing downloads ##
### Need to get to download screen after submitted request 
time.sleep(3)
if len(driver.window_handles) == 1: # If only one tab, i.e download tab not opened then skip 
	#### Close button brings back to main menu ###
	id_value = id_value_find('Close</button','ext-gen')
	driver.find_element_by_id("ext-gen"+str(id_value)).click()
	print ("NO RADAR DATA")
else:
	driver.switch_to.window(driver.window_handles[1]) ## This changes to second tab. Second tab is opened when "Download" is clicked, but HTML was staying with original page 

time.sleep(3)
#### Produces links to download all files on download page
elems = driver.find_elements_by_xpath("//a[@href]")
file_links = []
for elem in elems:
	file_links.append(elem.get_attribute("href"))

downloaded_file_paths = []
## Download all files on page into correct folder 
for  i in range(0,len(file_links)):
	word_search = file_links[i].find("ODC")
	urllib.request.urlretrieve(file_links[i],saved_files_dir+str(file_links[i][word_search:]))
	## Check that files are downloaded ##
	if os.path.exists(saved_files_dir+str(file_links[i][word_search:])):
		print ("File "+str(i+1)+" Downloaded Successfully")
		downloaded_file_paths.append(saved_files_dir+str(file_links[i][word_search:]))
	else:
		print ("File "+str(i+1)+" Download Failed")
# As well as the radar files (h5 files) a text file will also be downloaded showing the details of the download #

downloaded_file_paths = downloaded_file_paths[:-1]

driver.close() # Close download files tab #

driver.switch_to.window(driver.window_handles[0]) # Switch back to main menu page

#### Close button brings back to main menu ###

id_value = id_value_find('Close</button','ext-gen')
driver.find_element_by_id("ext-gen"+str(id_value)).click()

## Dealing with ZIP files if downloaded ##
## Assumes zip file is called "p" when downloaded ##
path_to_zip_file = saved_files_dir
if os.path.isfile(path_to_zip_file+'p'):
	print ("ZIP FILE DOWNLOADED")
	with zipfile.ZipFile(path_to_zip_file+'p', 'r') as zip_ref:
    		zip_ref.extractall(path_to_zip_file)
	os.remove(path_to_zip_file+'p')

########## PLOTTING ##########
directories = os.listdir(saved_files_dir)

## Removing text file so only radar files are attempted to be plotted ##
for radar_file in directories:
	if ".txt" in radar_file:
		directories.remove(radar_file)

directories.sort() # Make sure timesteps are in order #

## Designed to plot in groups of 4 ##
for file_limit in np.arange(0,int(math.ceil(len(directories) / 4.0)) * 4.0,4):
	files = directories[int(file_limit):int(file_limit)+4]
	for file_no in range(len(files)):

		fcontent = read_opera_hdf5(saved_files_dir+str(files[file_no]))


		data = fcontent['dataset1/data1/data']

		no_rainfall_val = -8888000.0

		min_rainfall_val = 0.1 # threshold where not considered as rainfall, just clutter 

		data[np.where(data == no_rainfall_val ) ] = np.nan # No rainfall value
		data[np.where((data>=0)&(data<=min_rainfall_val))] = np.nan

		LL_lat = fcontent['where']['LL_lat']
		LL_lon = fcontent['where']['LL_lon']
		LR_lat = fcontent['where']['LR_lat']
		LR_lon = fcontent['where']['LR_lon']
		UL_lat = fcontent['where']['UL_lat']
		UL_lon = fcontent['where']['UL_lon']
		UR_lat = fcontent['where']['UR_lat']
		UR_lon = fcontent['where']['UR_lon']

		# lat_0_where = fcontent['where']['projdef'].find('lat_0')
		# lat_0 = float(fcontent['where']['projdef'][lat_0_where+6:lat_0_where+10])
		# lon_0_where = fcontent['where']['projdef'].find('lon_0')
		# lon_0 = float(fcontent['where']['projdef'][lon_0_where+6:lon_0_where+10])

		# ---- Drawing basemap for plot ------- #

		lat_0 = 55.0
		lon_0 = 10.0
		if len(files) > 2:
			plt.subplot(2,2,file_no+1)
			print ("Size>2",len(files))
		else:
			print ("Size = 2",len(files))
			plt.subplot(2,1,file_no+1)

		plt.title(str(files[file_no][13:15]) + ' ' + str(month_list[int(files[file_no][11:13])-1])+' ' + str(files[file_no][7:11])+' '+files[file_no][15:19]+"UTC")

		m = Basemap(llcrnrlon=lllon,llcrnrlat=lllat ,urcrnrlon=urlon,urcrnrlat=urlat,resolution='c',projection='laea',lat_0=lat_0,lon_0=lon_0,epsg = 3035)
		try:
			m.arcgisimage(service="World_Shaded_Relief",xpixels = background_resolution,verbose=True,zorder=0)
		except  urllib2.HTTPError: # If error relating to pixel 
			print ("Failed to download map try less pixels")
			m.arcgisimage(service="World_Shaded_Relief",xpixels = 1500,verbose=True,zorder=0)

		m.drawcoastlines()
		m.drawcountries()

		full_m = Basemap(llcrnrlon=LL_lon,llcrnrlat=LL_lat ,urcrnrlon=UR_lon,urcrnrlat=UR_lat,resolution='c',projection='laea',lat_0=lat_0,lon_0=lon_0)#,epsg = 3035)

		levels = [0,0.2,0.5,1,2,3,5,7,10,15,20,25,30,40,50,75,100,150] ### mm/hr precipitation levels
		norm = mpl.colors.BoundaryNorm(levels,256)
		ny = data.shape[0]; nx = data.shape[1]
		lons, lats = full_m.makegrid(nx, ny)
		x, y = m(lons, lats)
		im = m.contourf(x,y,np.flipud(data),cmap='jet',levels=levels,norm=norm,extend='both')
		im.cmap.set_under(color='grey')
		im.cmap.set_over(color='pink')

		cbar = plt.colorbar(im,orientation="horizontal")
		cbar.set_ticks(levels)
		cbar.set_ticklabels(levels)
		cbar.ax.set_title('$mm hr^{-1}$')

	#############################
	fig = plt.gcf()
	if len(files)>2:
		fig.set_size_inches((16, 12), forward=False)
	else:
		fig.set_size_inches((8, 12), forward=False)

	fig.savefig(outputdir+'Figure_'+str( 1+int(file_limit/4.0))+'.eps',dpi=400,format='eps')
	plt.close()

