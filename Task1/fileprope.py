import csv
import os 
import os.path
from datetime import datetime

from pwd import getpwuid
def file(path):
    with open('out.csv', 'w') as csvFile:
        fieldnames=['Path','Size','CreatedDate','LastAccessDate','LastModifiedDate','OwnerName']                      
        writer= csv.DictWriter(csvFile,fieldnames=fieldnames)
        writer.writeheader()
        for entry in os.listdir(path):
            if os.path.isdir(os.path.join(path, entry)):
                with os.scandir(os.path.join(path,entry)) as entries:
                    for ent in entries:
                        if ent.is_file():
                            info=ent.stat()
                            pathoffile=f'{path}/{entry}/{ent.name}'
                            writer.writerow({"Path":pathoffile,"Size":info.st_size,"CreatedDate":convert_in_date(info.st_ctime),"LastAccessDate":convert_in_date(info.st_atime),"LastModifiedDate":convert_in_date(info.st_mtime),"OwnerName":getpwuid(info.st_uid).pw_name})
            else:
                if os.path.isfile(f'{path}/{entry}'):
                    info=os.stat(f'{path}/{entry}')
                    pathoffile=f'{path}/{entry}'
                    writer.writerow({"Path":pathoffile,"Size":info.st_size,"CreatedDate":convert_in_date(info.st_ctime),"LastAccessDate":convert_in_date(info.st_atime),"LastModifiedDate":convert_in_date(info.st_mtime),"OwnerName":getpwuid(info.st_uid).pw_name})
        print("Success")
                    
def convert_in_date(timestamp):
    d=datetime.utcfromtimestamp(timestamp)
    formated_date=d.strftime('%d %b %Y')
    return formated_date


filepath=input("Please enter Your file path \n")
try:
    file(filepath)
except FileNotFoundError as filenotfound:
    print("No such file or directory:",filepath)
