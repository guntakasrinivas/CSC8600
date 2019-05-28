# pip3 install Pillow 
# pip install Pillow
# '''
# # Impoert Packages

import csv
# Reaad File , write file
import os 
import os.path
# Date and time
from datetime import datetime
# pillow - for images 
from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS
#getpwid used for getting file 's user name 
import audio_metadata
from pwd import getpwuid
def file(path):
# its used for file open and create out.csv
    with open('out.csv', 'w') as csvFile:
        #column of csv file
                                    
        fieldnames=['Path','Size','CreatedDate','LastAccessDate','LastModifiedDate','OwnerName','Dimensions',"Tag","Bitrate",'Bitrate_mode','Channel_mode','Channels','Duration','Layer','Protected','Sample_rate','Version']                      
       #pass file name and column name
        writer= csv.DictWriter(csvFile,fieldnames=fieldnames)
       #write all conint in file 
        writer.writeheader()
        #variavle declaration
        tag=''
        #get all directory from path
        for entry in os.listdir(path):
            #if get directory then
            if os.path.isdir(os.path.join(path, entry)):
                #scan directory from given directory
                with os.scandir(os.path.join(path,entry)) as entries:
                    for ent in entries:
                        #if file then
                        if ent.is_file():
                            # take containt of file property
                            info=ent.stat()
                            #take file name
                            fileext=ent.name.split('.')[-1]
                            #file path
                            pathoffile=f'{path}/{entry}/{ent.name}'
                            #chek file type
                            if fileext=='png' or fileext=='jpg' or fileext=='svg' or fileext=='avi':
                                # print(fileext,"-----------------")
                                imagereturn=getimage(ent)
                                if(imagereturn!=None):
                                    print(imagereturn)
                                    # print("Image return",imagereturn)
                                    with Image.open(pathoffile) as img:
                                        width, height = img.size
                                        imginfo = img._getexif()
                                # # print(imginfo)
                                        if imginfo:
                                            for tag, value in imginfo.items():
                                                key = TAGS.get(tag, tag)
                                                print(value)
                                        img.close()
                                    writer.writerow({"Path":pathoffile,"Size":info.st_size,"CreatedDate":convert_in_date(info.st_ctime),"LastAccessDate":convert_in_date(info.st_atime),"LastModifiedDate":convert_in_date(info.st_mtime),"OwnerName":getpwuid(info.st_uid).pw_name,"Dimensions":f'{width}x{height}',"Tag":''})
        
                            elif fileext == 'mp3':
                                try:
                                    metadata=audio_metadata.load(ent)
                                # print("|||||||||||||||||||||||||||||||||||||||",ent,'||||||||||||||||||||||')
                                    # print(metadata)


                                    print(metadata['streaminfo'].bitrate)
                                    print(metadata['streaminfo'].bitrate_mode)
                                    print(metadata['streaminfo'].channel_mode)
                                    print(metadata['streaminfo'].channels)
                                    print(metadata['streaminfo'].duration)
                                    print(metadata['streaminfo'].layer)
                                    print(metadata['streaminfo'].protected)
                                    print(metadata['streaminfo'].sample_rate)
                                    print(metadata['streaminfo'].version)
                                    # for i in metadata:
                                        # print(i)
                                        # print(metadata[i])
                                        
                                        # print(metadata[i])
                                except:
                                    print("________________________",ent)
                        else:
                            writer.writerow({"Path":pathoffile,"Size":info.st_size,"CreatedDate":convert_in_date(info.st_ctime),"LastAccessDate":convert_in_date(info.st_atime),"LastModifiedDate":convert_in_date(info.st_mtime),"OwnerName":getpwuid(info.st_uid).pw_name})    
            


        print("Success")
  #convert date time                   
def convert_in_date(timestamp):
    d=datetime.utcfromtimestamp(timestamp)
    formated_date=d.strftime('%d %b %Y')
    return formated_date

# # take input from user

def getimage(filepath):
    try:
        ret = {}
        i = Image.open(filepath)
        info = i._getexif()
        if info is not None:
            print(info)
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                print(decoded)
                ret[decoded] = value
            return ret
        else:
            return None
    except:
        print(filepath)
filepath=input("Enter Your file path \n")
try:
    #call file funcation with argument as filepath
    file(filepath)
except FileNotFoundError as filenotfound:
    print("No such file or directory:",filepath)
