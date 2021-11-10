from ij import IJ
import ij
import ij.io
import ij.plugin
import os
import sys
from glob import glob

def open_raw(file,SHOW_FLAG):
	file_name = os.path.basename(file)
	dir = os.path.dirname(file)
	raw_file = os.path.join(dir,"Deconvolved.txt")
	print(raw_file)
	#quit()
	f= open(raw_file,"r")
	#print(f.readlines()[0].split())
	fi = ij.io.FileInfo()
	fi.fileFormat = ij.io.FileInfo.RAW
	fi.fileName = file_name
	fi.directory =  dir
	fi.fileType = ij.io.FileInfo.GRAY16_UNSIGNED
	fi.intelByteOrder = True;
	
	for line in f.readlines():
	#	print(line)
		split_line = line.split()
#		print(split_line)
		if(split_line[0] == "width"):  		fi.width = int(split_line[1])
		if(split_line[0] == "height"):  	fi.height = int(split_line[1])
		if(split_line[0] == "depth"):  		fi.nImages = int(split_line[1])
	#	if(split_line[0] == "bitdepth"):  	fi.fileFormat = ij.io.FileInfo.GRAY16_UNSIGNED
	
	#print(fi)
	
	#imp = ij.plugin.Raw.open(file,fi);		
	#imp = ij.plugin.Raw.open(file, fi)
	fo = ij.io.FileOpener(fi)
	imp = fo.open(False)
	if(SHOW_FLAG):imp.show()
	return imp

#def z_projectfile(file):
#current_file = "T:\\DATA0\\LSM\\_Processed\\2019-04-02\\190402_10.41.05_ISO34_Vemurafenib_0_0412uM\\190402_10.41.05_Step_Size_-0.4_Wavelength_DAPI 452-45_ISO34_Vemurafenib_0_0412uM\\Deconvolved.raw"
#current_file = "T:\\DATA0\LSM\\_Processed\\2019-04-02\\190402_10.41.05_ISO34_Vemurafenib_0_0412uM\\190402_10.41.05_Step_Size_-0.4_Wavelength_RFP 600-52_ISO34_Vemurafenib_0_0412uM\\Deconvolved.raw"

def z_projectfile(imp):
	
	z_project = ij.plugin.ZProjector.run(imp,"max")
	if(SHOW_FLAG):z_project.show()
	z_project_contrast = ij.plugin.Duplicator().run(z_project)
	IJ.run(z_project_contrast, "Enhance Contrast", "saturated=0")
	IJ.run(z_project_contrast, "Apply LUT", "0.35")
	print(z_project_contrast.getTitle())
	path_to_z_project =  os.path.join(dir,z_project_contrast.getTitle()+"_XY")
	IJ.saveAs(z_project_contrast, "Tiff", os.path.join(dir,z_project_contrast.getTitle()+"_XY"))
	if(SHOW_FLAG):z_project_contrast.show()

#	print(z_project_contrast)
	return z_project_contrast,path_to_z_project

#z_projectfile(file)
##dir = "T:\\DATA0\\LSM\\_Processed"
##dir = "T:\\DATA0\\LSM\\_Processed\\2019-04-02"
#
image_extension = ".raw"
dir = "T:\\DATA0\\LSM\\_Processed\\2019-04-02"
dir = "T:\\DATA0\LSM\\_Processed\\2019-05-08"
dir = "T:\\DATA0\LSM\\_Processed\\2019-05-03"
dir = "T:\\DATA0\\LSM\\_Processed\\2019-05-03\\"
dir = "T:\\DATA0\\LSM\\_Processed\\2019-04-04\\"
dir = "T:\\DATA0\\LSM\\_Processed\\2019-05-15 - Fuad - HipSci\\"
dir = 'T:\\DATA0\\LSM\\_Processed\\_2019_cellesce\\2019-04-05\\'
dir = 'T:\\DATA0\LSM\\_Processed\\_2019_cellesce\\2019-05-01\\'
dir = 'T:\\DATA0\\LSM\\_Processed\\_2019_cellesce\\'
dir = 'T:\\DATA0\\LSM\\_Processed\\_2019_kcl\\'
dir =  'T:\\DATA0\\LSM\\_Processed\\_2019_kcl\\2019-06-04 - Fuad'
#dir = "T:\\DATA0\\LSM\\_Processed\\2019-04-03"
##dir = "T:\\DATA0\\LSM\\_Processed\\2019-04-04"
#dir = "T:\\DATA0\\LSM\\_Processed\\2019-04-05"
#dir = "T:\\DATA0\\LSM\\_Processed\\2019-04-09"
## contrast process
#if(PROCESS_FLAG):
#	for root, dirs, files in os.walk(dir):
#		for file in files:
#	#		print(file)
#			if file.endswith(image_extension):
#				current_file_path = os.path.join(root,file)
#				print(current_file_path)
#				z_project_contrast,path_to_z_project = z_projectfile(current_file_path)
#


#print(glob(dir+"/*/"))


# Convert projections to png and tiff

#colour_folders = glob(dir+"/*/*/")

import fnmatch
import os

raw_files = []
for root, dirnames, filenames in os.walk(dir):
    for filename in fnmatch.filter(filenames, '*.raw'):
        raw_files.append(os.path.join(root, filename))
       
for root, dirnames, filenames in os.walk(dir):
	raw_files.extend(glob(root + "/*.raw"))
#raw_files = glob(dir+"/**/*.raw", recursive=True)
#print(raw_files)
colour_folders = list(set([os.path.dirname(filename) for filename in raw_files]))
image_folders = list(set([os.path.dirname(foldername) for foldername in colour_folders]))
#os.path.dirname(for file_name in raw_files[0])]
#print('raw_files')
#for folder in raw_files:print(folder)
#print('colour_folders')
#for folder in colour_folders:print(folder)
#print('image_folders')
#for folder in image_folders:print(folder)

##image_folders = glob(dir+"/*/")

SHOW_FLAG = 0
PROCESS_FLAG = 0
COMPOSITE_FLAG = 1
MONTAGE_FLAG = 1
print("Processing")
if(PROCESS_FLAG):
	for colour_folder in colour_folders:
		try:
			current_file_path = os.path.join(colour_folder,"Deconvolved.raw")
			z_project_contrast,path_to_z_project = z_projectfile(current_file_path)
			print(current_file_path)
		except:
			print("Failed on: " + current_file_path)

#print(image_folders)
print("Compositing")
if(COMPOSITE_FLAG):	
	images_array = [None]*12	
	for image_folder in image_folders:
		wavelengths = glob(image_folder+"/*Wavelength*/")	
		#print(image_folder)
		#print(os.path.join(image_folder,"Composite.png"))
		try:
			for i,wavelength in enumerate(wavelengths):
	#			 print(wavelength)
	#			 print()
				 current_file = os.path.join(wavelength,"DUP_MAX_Deconvolved.raw_XY.tif")
				 current_file = glob(wavelength+'/*raw_XY*')[0]
				 print(current_file)
		#		 images_array[wavelength] = IJ.openImage(current_file)
				 current_image_single = IJ.openImage(current_file)				 
				 ij.plugin.ContrastEnhancer().stretchHistogram(current_image_single,0.35)			  
#				 IJ.run(current_image.getProcessor(), "Enhance Contrast", "saturated=0.35")
				 images_array[i+5] = current_image_single
#				 images_array[i+5] = ij.io.Opener.openImage(current_file) # TRY THIS LATER
		#		 images_array.append(IJ.openImage(current_file))
				 
		#		 images_array[wavelength].show()
		#		 print(current_file)
			out = ij.plugin.RGBStackMerge.mergeChannels(images_array,False)
			#out.show()
			try:
				IJ.saveAs(out, "png", os.path.join(image_folder,"Composite.png"));
			except:
				print("Couldn't save png")
			try:
				IJ.saveAs(out, "tif", os.path.join(image_folder,"Composite.tif"));
			except:
				print("Couldn't save tif")
			images_array = [None]*12
		except:
			print("Failed on " + str(image_folder))
##	print(image_folders.size())
#	for image_folder in image_folders:
#		wavelengths = glob(image_folder+"/*Wavelength*/")	

# FIX BEASTIARY
print("Montaging")
if(MONTAGE_FLAG):
	montage_array = [] #[None]*len(image_folders)
	#montage_stack = ij.ImageStack()
	if(MONTAGE_FLAG):
		for image_folder in image_folders:
			current_file = os.path.join(image_folder,"Composite.png")
	#		print(current_file)
			path = os.path.normpath(image_folder)
			split_path = path.split(os.sep)
			print(split_path[-1])
			current_image = IJ.openImage(current_file)
			current_image.setTitle(split_path[-1])
			current_image.setProperty("Label", split_path[-1]) 
	#		current_image.show()
			montage_array.append(current_image)
	concat_montage_array = ij.plugin.Concatenator.run(montage_array)
	#concat_montage_array.show()
	#IJ.run(concat_montage_array, "Make Montage...", "columns=6 rows=5 scale=1 font=20 label");
	import math
	#math.sqrt(2)
	montage_columns =round(math.sqrt((len(image_folders))))
	montage_rows =  round(len(image_folders)/(montage_columns))
	print(str(montage_columns)+'  ' + str(montage_rows))
	#montaged=MontageMaker.makeMontage2(concat_montage_array,scale=1,labels=True,columns=montage_columns,rows=montage_rows,first=1,last=int(len(image_folders)),	borderWidth=0,inc=1)
	MontageMaker = ij.plugin.MontageMaker()
	MontageMaker.setFontSize(48)
	
	montaged=MontageMaker.makeMontage2(concat_montage_array,int(montage_columns),int(montage_rows),1.00,1,len(image_folders),1,0,True)
	montaged.show()

	IJ.saveAs(montaged, "png", os.path.join(dir,"montage"+"_XY"))


















#dirs = os.walk(dir)
#print(dirs)
#for image_volumes in dirs:
#	print(image_volumes[0])
#
#for root, dirs, files in os.walk(dir):
#	print(root)
#		print(image_volumes)
##		print(file)
#		if file.endswith(image_extension):
#			
#			print(root)
#			current_file_path = os.path.join(root,file)
##			print(current_file_path)

###
###z_projectfile
##			
###for fname in os.listdir(dir):
###    print(fname)
###    if fname.endswith(image_extension):
###        print(fname)
###
###srcDir = srcFile.getAbsolutePath()
###dstDir = dstFile.getAbsolutePath()
###for root, directories, filenames in os.walk(srcDir):
###filenames.sort();
###for filename in filenames:
###  # Check for file extension
###  if not filename.endswith(ext):
###    continue
###  # Check for file name pattern
###  if containString not in filename:
###    continue
###  process(srcDir, dstDir, root, filename, keepDirectories)