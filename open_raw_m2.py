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
