import glob
import os

unet_suffix = "*_unet.tif"
sub_folders = ["2019-03-15",
               "2019-03-19",
               "2019-03-20",
               "2019-03-21",
               "2019-03-22",
               "2019-03-25",
               "2019-03-26",
               "2019-03-27",
               "2019-03-28",
               "2019-03-29",
               "2019-04-01",
               "2019-04-02",
               "2019-04-03",
               "2019-04-04",
               "2019-04-05",
               "2019-04-09",
               "2019-04-13",
               "2019-04-30",
               "2019-05-01",
               "2019-05-03",
               "2019-05-08",
               "2019-05-16",
               "2019-05-20",
               "2019-05-21",
               "2019-05-22",
               "2019-05-24"]

cellesce_cropped = [os.path.join(
    "~/npl_ftp/_2019_cellesce", sub_folder, "**", unet_suffix) for sub_folder in sub_folders]

sub_folders = ["2019-05-07",
               "2019-05-09",
               "2019-05-10",
               "2019-05-13",
               "2019-05-14",
               "2019-05-15",
               "2019-05-23",
               "2019-05-24",
               "2019-05-28",
               "2019-05-29",
               "2019-05-30"]

cellesce_uncropped = [os.path.join(
    "~/npl_ftp/_2019_cellesce_uncropped", sub_folder, "**", unet_suffix) for sub_folder in sub_folders]

print(cellesce_uncropped)
print(cellesce_cropped)

folders = cellesce_cropped + cellesce_uncropped

# glob.glob(cellesce_uncropped, recursive=True)
out = [glob.glob(os.path.expanduser(sub_folder), recursive=True)
       for sub_folder in folders]

# out = glob.glob(os.path.expanduser(folders[0]), recursive=True); out

images = list(set(list(sum(out, []))))

with open('list_unet.txt', 'w') as f:
    for item in images:
        f.write("\"%s\"\n" % item)
