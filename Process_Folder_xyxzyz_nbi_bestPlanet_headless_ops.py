#@ OpService ops
from ij import IJ
import datetime
import ij
from ij.io import FileOpener,FileInfo
# from ij import io

# import ij.plugin
import os
import sys
from glob import glob
from net.imglib2.img.display.imagej import ImageJFunctions
from ij.gui import ProfilePlot
import fnmatch
import sys

# IJ.setBatchMode(True)
# old_f = sys.stdout
# class F:
#     def write(self, x):
#         old_f.write(x.replace("\n", "\n[%s]" % str(datetime.datetime.now())))
# sys.stdout = F()

# #@ OpService ops
# import fnmatch
# from ij import IJ
# from ij.io import FileInfo, FileOpener
# # import ij.plugin
#
# import ij
# import os
# import sys
# from glob import glob
# from net.imglib2.img.display.imagej import ImageJFunctions
# from ij.gui import ProfilePlot
# import re
# # import path

print("Begin")
print(ops)

def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)

    def show(j):
        x = int(size * j / count)
        file.write("%s[%s%s] %i/%i\r" %
                   (prefix, "#" * x, "." * (size - x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    file.write("\n")
    file.flush()


def open_raw(file,SHOW_FLAG):
	file_name = os.path.basename(file)
	print(file)
	dir = os.path.dirname(file)
	raw_file = os.path.join(os.path.abspath(dir),"Deconvolved.txt")
	print(raw_file)
	#quit()
	f= open(raw_file,"r")
	#print(f.readlines()[0].split())
	fi = FileInfo()
	fi.fileFormat = ij.io.FileInfo.RAW
	fi.fileName = file_name
	fi.directory =  dir
	fi.fileType = ij.io.FileInfo.GRAY32_FLOAT
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
	fo = FileOpener(fi)
	imp = fo.open(False)
	if(SHOW_FLAG):imp.show()
	return imp

# def z_projectfile(file):
#current_file = "T:\\DATA0\\LSM\\_Processed\\2019-04-02\\190402_10.41.05_ISO34_Vemurafenib_0_0412uM\\190402_10.41.05_Step_Size_-0.4_Wavelength_DAPI 452-45_ISO34_Vemurafenib_0_0412uM\\Deconvolved.raw"
#current_file = "T:\\DATA0\LSM\\_Processed\\2019-04-02\\190402_10.41.05_ISO34_Vemurafenib_0_0412uM\\190402_10.41.05_Step_Size_-0.4_Wavelength_RFP 600-52_ISO34_Vemurafenib_0_0412uM\\Deconvolved.raw"


def z_project(imp):
    z_project = ij.plugin.ZProjector.run(imp, "max")
    if(SHOW_FLAG):
        z_project.show()
    z_project_contrast = ij.plugin.Duplicator().run(z_project)
    IJ.run(z_project_contrast, "Enhance Contrast", "saturated=0")
    IJ.run(z_project_contrast, "Apply LUT", "0.35")
#	print(z_project_contrast)
    return z_project_contrast

def project(imp, img, axis):
    maxOp = ops.op("stats.max", img)

    x_dim, y_dim, nChannels, z_dim, nFrames = imp.getDimensions()
    if(axis == 0):
        slicer = [y_dim, z_dim]
    #	if(axis==1): slicer = [x_dim,y_dim]
    #	if(axis==2): slicer = [x_dim,z_dim]
    if(axis == 1):
        slicer = [x_dim, z_dim]
    if(axis == 2):
        slicer = [x_dim, y_dim]
#	print(slicer)

    projection = ops.create().img(slicer)
    #	projection_16bit = ops.convert().uint16(projection)
    ops.run("project", projection, imp, maxOp, axis)
    projection16 = ops.convert().uint16(projection)

    impProjection = ImageJFunctions.wrap(projection, "project")
    if(SHOW_FLAG):
        impProjection.show()
    for channel in range(0, impProjection.getNChannels()):
        impProjection.setC(channel + 1)
        IJ.run(impProjection, "Enhance Contrast", "saturated=0.35")
    return impProjection


def best_plane(imp, img):
    #imp16 = ops.convert().uint16(imp)
    x_dim, y_dim, nChannels, z_dim, nFrames = imp.getDimensions()
    maxOp = ops.op("stats.sum", img)
    #maxOp = ops.op("stats.max", img)
    x_dim, y_dim, nChannels, z_dim, nFrames = imp.getDimensions()
    #slicer = z_dim
    axis_1 = 0
    axis_2 = 1
    blurring_kernel_size = 8
    slicer = [y_dim, z_dim]
    projection = ops.create().img(slicer)

    #ops.transform().project(projected, data, proj_op, dim)

    ops.run("project", projection, img, maxOp, axis_1)
    impProjection = ImageJFunctions.wrap(projection, "best_plane")

    impProjection_blur = ops.filter().gauss(
        projection, [blurring_kernel_size, 0, 0])

    line_profile = ops.create().img([z_dim])
    sumOp = ops.op("stats.sum", line_profile)
    ops.transform().project(line_profile, impProjection_blur, sumOp, axis_2)
    line_profile_imp = ImageJFunctions.wrap(line_profile, "best_plane")
    # line_profile_imp.show()

    #line_profile_imp = ImageJFunctions.wrap(line_profile)
    IJ.run(line_profile_imp, "Select All", "")
    profile = ij.gui.ProfilePlot(line_profile_imp).getProfile()
    best_plane_index = profile.index(max(profile))
    # print(line_profile_imp.getDimensions())

    # Really hope this chooses slices correctly.
    output = ops.run("hyperSliceView", img, 2, best_plane_index)
    output_imp = ImageJFunctions.wrap(output, "best_plane")
    return output_imp


# z_projectfile(file)
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
dir = 'T:\\DATA0\\LSM\\_Processed\\_2019_kcl\\2019-06-04 - Fuad'
dir = 'T:\\DATA0\\LSM\\_Processed\\_2019_cellesce_uncropped'
dir = 'T:\\DATA0\\LSM\\_Processed\\_2019_kcl\\_processed\\'

dir = '/Users/ctr26/npl_ftp/'
dir = '/Users/ctr26/npl_ftp/_2019_cellesce_uncropped/2019-05-09/190509_17.07.23_ISO49_5FU_0_0412uM/Position_9/'
dir = '/Volumes/GoogleDrive/My Drive/_data/_cellesce/'
dir = '/homes/ctr26/gdrive/_data/_cellesce/'
dir = '/homes/ctr26/npl_ftp/'
dir = '/nfs/biostudies/ftp/pub/.dropbox/b6/58f8c7-0d88-424c-96bd-63d97210703c-a408'

# dir = "/homes/ctr26/npl_ftp/_2019_cellesce_uncropped/2019-05-13/190513_10.51.39_ISO49_Dabrafenib_0uM/Position_5/190513_10.51.39_Step_Size_-0.4_Wavelength_RFP 600-52_Position_Position_5_ISO49_Dabrafenib_0uM/"
# dir = '/homes/ctr26/npl_ftp/_2019_cellesce_uncropped/2019-05-15/190515_17.09.42_ISO49_Dabrafenib_0_0137uM/Position_11'

#dir = 'T:\\DATA0\\LSM\\_Processed\\_2019_kcl\good'
#dir = 'T:\\DATA0\\LSM\\_Processed\\_2019_kcl\\redo'

#dir = 'T:\\DATA0\\LSM\\_Processed\\_2019_kcl\\_processed\\2019-06-04 - Fuad\\190621_14.31.33_EOMES KOSR'
#dir = 'T:\\DATA0\\LSM\\_Processed\\_2019_kcl\\_processed\\2019-07-10 Fuad\\190710_14.25.04_SOX17 KOSR'
#dir = 'T:\\DATA0\LSM\\_Processed\\_2019_kcl\\_processed\\2019-04-18 - Fuad\\190418_11.41.56_Sample 1'
#dir = 'T:\\DATA0\\LSM\\_Processed\\_2019_kcl\\_processed\\2019-05-15 - Fuad - HipSci\\190515_14.45.22_KOSR-BMP4-2'


#dir = 'T:\DATA0\\LSM\\_Processed\\_2019_kcl\\_processed\\2019-05-15 - Fuad - HipSci\\190515_11.36.30_E8-1\\'
#dir = 'T:\\DATA0\\LSM\\_Processed\\_2019_kcl\\_processed\\2019-05-15 - Fuad - HipSci\\190515_11.36.30_E8-1\\190515_11.36.30_Step_Size_-0.4_Wavelength_GFP-D 520-40_E8-1'
#dir = "T:\\DATA0\\LSM\\_Processed\\2019-04-03"
##dir = "T:\\DATA0\\LSM\\_Processed\\2019-04-04"
#dir = "T:\\DATA0\\LSM\\_Processed\\2019-04-05"
#dir = "T:\\DATA0\\LSM\\_Processed\\2019-04-09"
# contrast process
# if(PROCESS_FLAG):
#	for root, dirs, files in os.walk(dir):
#		for file in files:
#	#		print(file)
#			if file.endswith(image_extension):
#				current_file_path = os.path.join(root,file)
#				print(current_file_path)
#				z_project_contrast,path_to_z_project = z_projectfile(current_file_path)
# print(glob(dir+"/*/"))
# Convert projections to png and tiff
#colour_folders = glob(dir+"/*/*/")
PROJECT = 0

print("Listing raw files")
raw_files = []

for root, dirnames, filenames in os.walk(dir):
	for filename in fnmatch.filter(filenames, '*_32bit.raw'):
		raw_files.append(os.path.join(root, filename))

# for root, dirnames, filenames in os.walk(dir):
#     # for filename in fnmatch.filter(filenames, '*32bit.raw'):
#         # raw_files.append(os.path.join(root, filename))
#     # print(root)
#     raw_files.extend(glob(root + "*32bit.raw"))

#raw_files = glob(dir+"/**/*.raw", recursive=True)
print("Found: " + str(len(raw_files)) + "raw files")
colour_folders = list(set([os.path.dirname(filename)
                           for filename in raw_files]))
image_folders = list(set([os.path.dirname(foldername)
                          for foldername in colour_folders]))

raw_files = [os.path.abspath(raw_file) for raw_file in raw_files]
colour_folders = [os.path.abspath(colour_folder)
                  for colour_folder in colour_folders]
image_folders = [os.path.abspath(image_folder)
                 for image_folder in image_folders]

# print(colour_folders)
# raw_files = ["/homes/ctr26/npl_ftp/_2019_cellesce_uncropped/2019-05-15/190515_17.09.42_ISO49_Dabrafenib_0_0137uM/Position_11/190515_17.09.42_Step_Size_+0.4_Wavelength_RFP\ 600-52_Position_Position_11_ISO49_Dabrafenib_0_0137uM/Deconvolved_32bit.raw"]
# os.path.dirname(for file_name in raw_files[0])]
# print('raw_files')
#for folder in raw_files:print(folder)
# print('colour_folders')
#for folder in colour_folders:print(folder)
# print('image_folders')
#for folder in image_folders:print(folder)

##image_folders = glob(dir+"/*/")
projections_axes = {'YZ': 0, 'XZ': 1, 'XY': 2}

def project_yz(imp,img):return project(imp, img, 0)
def project_xz(imp,img):return project(imp, img, 0)
def project_xy(imp,img):return project(imp, img, 0)

function_list = [project,project,project,]

projections_axes = {'YZ': 0, 'XZ': 1, 'XY': 2,'best_plane'}


SHOW_FLAG = 0

PROCESS_FLAG = 0
COMPOSITE_FLAG = 1
MONTAGE_FLAG = 0

colour_folders_todo = colour_folders[23:]

print("Processing")
if(PROCESS_FLAG):
    for i,colour_folder in enumerate(colour_folders_todo):
        print("Colour folder: " + os.linesep +colour_folder + os.linesep +
			"-------" + str(i) + "/" + str(len(colour_folders_todo)) + "-------")
        try:
	        current_file_path = os.path.join(colour_folder, "Deconvolved_32bit.raw")
	        print("Opening")
	        # print(current_file_path)
	        imp = open_raw(current_file_path, False)
	        print("Opened, now convert")
	        img = ImageJFunctions.wrapFloat(imp)
	        print("Converted")
	        # print("Projecting")
	        # print(current_file_path)
			# z_project_contrast,path_to_z_project = z_projectfile(imp)
			# print("Projecting")
	        if(PROJECT):
		        for projection_axis_key in projections_axes:
		            print("Projecting " + str(projection_axis_key))
		            projections_axis = projections_axes[projection_axis_key]
		            projection = project(imp, img, projections_axis)
		            print("Saving " + str(projection_axis_key))
		            path_to_z_project = os.path.join(colour_folder, projection.getTitle() + "_" + str(projection_axis_key))
		            print(path_to_z_project)
		            IJ.saveAs(projection, "Tiff", path_to_z_project)
		            print("Saved" + str(projection_axis_key))
		            if(SHOW_FLAG):
		                projection.show()
	            # print(current_file_path)
	        best_plane_img = best_plane(imp, img)
	        path_to_best_plane = os.path.join(colour_folder, "best_plane")
	        print("Saving best plane")
	        IJ.saveAs(best_plane_img, "Tiff", path_to_best_plane)

	#			best_plane(imp,img,projections_axis)
	#			except:
	        imp.close()
	        IJ.freeMemory()
        except:
            print("Failed")
            print(current_file_path)

# print(image_folders)
print("Compositing")
if(COMPOSITE_FLAG):
    images_array = [None] * 12
    for image_folder in image_folders:
        wavelengths = glob(image_folder + "/*Wavelength*/")
        # print(image_folder)
        # print(os.path.join(image_folder,"Composite.png"))
        try:
            # print(current_file)
            # for projection_axis_key in projections_axes:
            for projection_axis_key in projections_axes:
                for i, wavelength in enumerate(wavelengths):
        			 # print(wavelength)
        			 # print()
        				#  current_file = os.path.join(wavelength,"DUP_project_YZ.tif")
                    projections_axis = projections_axes[projection_axis_key]
                    current_file = os.path.join(wavelength,
                                    "project_"+projections_axis+".tif")
                    current_file = glob(wavelength+'/*raw_XY*')[0]
                    images_array[wavelength] = IJ.openImage(current_file)
                    current_image_single = IJ.openImage(current_file)
                    #ij.plugin.ContrastEnhancer().stretchHistogram(current_image_single,0.0)
                    #IJ.run(current_image.getProcessor(), "Enhance Contrast", "saturated=0.35")
                    images_array[i + 5] = current_image_single
                    # images_array[i+5] = ij.io.Opener.openImage(current_file) # TRY THIS LATER
                    #images_array.append(IJ.openImage(current_file))
                    #images_array[wavelength].show()
                    #print(current_file)
                out = ij.plugin.RGBStackMerge.mergeChannels(images_array, False)
                # out.show()
                try:
                    IJ.saveAs(out, "png", os.path.join(
                        image_folder, "Composite.png"))
                except:
                    print("Couldn't save png")
                try:
                    IJ.saveAs(out, "tif", os.path.join(
                        image_folder, "Composite.tif"))
                except:
                    print("Couldn't save tif")
                images_array = [None] * 12
        except:
            print("Failed on " + str(image_folder))
# print(image_folders.size())
#	for image_folder in image_folders:
#		wavelengths = glob(image_folder+"/*Wavelength*/")

# FIX BEASTIARY
image_count = 0
print("Montaging")
if(MONTAGE_FLAG):
    montage_array = []  # [None]*len(image_folders)
    #montage_stack = ij.ImageStack()
    if(MONTAGE_FLAG):
        for image_folder in image_folders:
            try:
                current_file = os.path.join(image_folder, "Composite.png")
                print(current_file)
                path = os.path.normpath(image_folder)
                split_path = path.split(os.sep)
#				print(split_path[-1])
                current_image = IJ.openImage(current_file)
                current_image.setTitle(split_path[-1])
                current_image.setProperty("Label", split_path[-1])
        #		current_image.show()
                montage_array.append(current_image)
                image_count += 1
            except:
                print("Failed on " + str(image_folder))
    concat_montage_array = ij.plugin.Concatenator.run(montage_array)
    # concat_montage_array.show()
    #IJ.run(concat_montage_array, "Make Montage...", "columns=6 rows=5 scale=1 font=20 label");
    import math
    # math.sqrt(2)
#	image_count = len(image_folders)
    montage_columns = round(math.sqrt((image_count)))
    montage_rows = round(image_count / (montage_columns))
    print(str(montage_columns) + '  ' + str(montage_rows))
    # montaged=MontageMaker.makeMontage2(concat_montage_array,scale=1,labels=True,columns=montage_columns,rows=montage_rows,first=1,last=int(image_count),	borderWidth=0,inc=1)
    MontageMaker = ij.plugin.MontageMaker()
    MontageMaker.setFontSize(48)

    montaged = MontageMaker.makeMontage2(concat_montage_array, int(
        montage_columns), int(montage_rows), 1.00, 1, image_count, 1, 0, True)
    montaged.show()

    IJ.saveAs(montaged, "png", os.path.join(dir, "montage" + "_XY"))


#dirs = os.walk(dir)
# print(dirs)
# for image_volumes in dirs:
#	print(image_volumes[0])
#
# for root, dirs, files in os.walk(dir):
#	print(root)
#		print(image_volumes)
# print(file)
#		if file.endswith(image_extension):
#
#			print(root)
#			current_file_path = os.path.join(root,file)
# print(current_file_path)

###
# z_projectfile
##
# for fname in os.listdir(dir):
# print(fname)
# if fname.endswith(image_extension):
# print(fname)
###
###srcDir = srcFile.getAbsolutePath()
###dstDir = dstFile.getAbsolutePath()
# for root, directories, filenames in os.walk(srcDir):
# filenames.sort();
# for filename in filenames:
# Check for file extension
# if not filename.endswith(ext):
# continue
# Check for file name pattern
# if containString not in filename:
# continue
###  process(srcDir, dstDir, root, filename, keepDirectories)
