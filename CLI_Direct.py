'''
download zip file from following link
https://sno.phy.queensu.ca/~phil/exiftool/Image-ExifTool-11.45.tar.gz

if use exiftool then put above file path here
'''
import csv
# Reaad File , write file
import os
import os.path
# Date and time
from datetime import datetime
# pillow - for images
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
# getpwid used for getting file 's user name
import subprocess
import csv
from pwd import getpwuid
metadata = []
fieldnames = []
dictapp = {}


def file(path):
    fieldnames = ['File Name','Directory','File Size','File Type','Create Date','Modify Date','Encoder Settings',"Software",'Aperture Value','Brightness Value','Pixels Per Unit X','Pixels Per Unit Y','Pixel Units','Flash','Image Width','Image Height','Bit Depth','Color Type'
    ,'Compression',"F Number",'ISO','GPS Time Stamp','Aperture','Audio Sample Rate','Movie Data Size','Movie Data Offset','Handler Vendor ID','Audio Bits Per Sample','Image Size','App Version','Creator'
    ,'Doc Security','Hyperlinks' ,'Changed','LastSaved','Links Up To Date','Scale Crop','Artist','Album','Year','Video Frame Rate','Duration','MPEG Audio Version','Audio Layer','Audio Bitrate','Sample Rate','Channel Mode','MS Stereo','Genre','Copyright Flag'
    ,'Title','ID3 Size','PDF Version','Linearized','Page Count','Producer','Compatible Brands','Movie Header Version','Time Scale'
    ,'Duration','Preferred Rate','Preferred Volume','Preview Time','Preview Duration',"Poster Time","Camera Model Name"
    ,"Make","Resolution Unit",'Megapixels','Filter','Interlace','Significant Bits','Language','Revision Number','Subject','Template','Total Edit Time']

# # its used for file open and create out.csv
    with open('out.csv', 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()
        print("In Process")
        try:
            for entry in os.listdir(path):
                #             #if get directory then
                if os.path.isdir(os.path.join(path, entry)):
                    #                 #scan directory from given directory
                    with os.scandir(os.path.join(path, entry)) as entries:
                        
                        for ent in entries:
                            #                         #if file then
                            if ent.is_file():
                                #                             # take containt of file property
                                info = ent.stat()
        #                             #take file name
                                fileext = ent.name.split('.')[-1]
        #                             #file path
                                pathoffile = f'{path}/{entry}/{ent.name}'
                                d = extractmetadata(pathoffile)
                                for i in d:
                                    # print(d[i])
                                    try:
                                        writer.writerow(d)
                                    except:
                                        # print(e)
                                        pass
       
            csvFile.close()
            print("--------------Success--------------------------")
        except:
            print("Given Path is a Not Directory Path")

# extract matadat 
def extractmetadata(filepath):
    try:
        # exe = 'hachoir-metadata'
        exifttoolpath = './Image-ExifTool/'
        exe = '{}{}'.format(exifttoolpath, 'exiftool')
        process = subprocess.Popen(
            [exe, filepath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        info = {}
        for output in process.stdout:
            line = output.strip().split(':')
            # print(line[0])
            fieldnames.append(line[0].strip())
            info[line[0].strip()] = line[1].strip()
        return info
    except:
        print("Errrorr----------------")

# take input from user
filepath = input("Enter Your file path \n")
try:
    # call file funcation with argument as filepath
    file(filepath)
except FileNotFoundError as filenotfound:
    print("No such file or directory:", filepath)

