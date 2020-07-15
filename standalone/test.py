import glob
import os

upload_folder = "C:/Users/Computer/Desktop/text_archive/dummy"

file_list = glob.glob(os.path.join(upload_folder, "*.txt"))
print(file_list)
for f in file_list:
    os.remove(f)



