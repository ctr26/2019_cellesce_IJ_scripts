# @File(label='Choose the data directory', style='directory') import_dir
# @Boolean(label="Data from the microscope?", value = True) raw
# @String (visibility=MESSAGE, value="Otherwise, try and stitch files with 'Deconvolved' on the name.") desc_text1
# @File(label='Choose where to save the resulting tiffs', style='directory') out_dir

from ij import IJ
import MSquared

import_dir = MSquared.get_path_from_file(import_dir)

if (raw):
    data = MSquared.RAW_DATA_TYPE
else:
    data = MSquared.DECONVOLVED_DATA_TYPE

try:
    MSquared.convert_mm_acquisition_to_imagej_tiff(import_dir, data, out_dir)

    IJ.freeMemory()
    IJ.log("Aurora conversion script finished.")

except ValueError as e:
    print(str(e))

finally:
    print("Aurora conversion script finished.")
