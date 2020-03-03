# reads a directory and outputs the input csv used for amazon mechanical turk

base_url = "https://test-bucket-03022020.s3.amazonaws.com/"

base_dir = r"C:\Users\Walter\Downloads\turk\gsv_20200228112722\renamed"

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(base_dir) if isfile(join(base_dir, f))]


with open(r"C:\Users\Walter\Downloads\turk\input.csv", "w") as f:
    f.write("image_url\n")
    for files in onlyfiles:
        url = base_url + files
        f.writelines(url + "\n")
