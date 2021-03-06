from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk
import PIL.Image
import csv
from tkinter import filedialog,scrolledtext,messagebox,Image
import os
import pandas
filedialogname=[]
root = Tk()
root.title("Python - Import CSV File To Tkinter Table")
width = 1300
height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
 
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
# canvas=Canvas(root, width = 300, height = 300)
# canvas.pack()
# img=PhotoImage(file=filepath)
# canvas.create_image(20,20,anchor=NW,image=img)
import operator

def filterdata(*args):
    print(tkvar.get())
    search=tkvar.get()
    for i in tree.get_children():
        tree.delete(i)
    with open(filedialogname[0]) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0] !='File Name':

                if(search in row[4] ):
                    tree.insert("", 0, values=row)  
                    tree.pack()  
        f.close()  
# filter by size when you chose any one sizw
def filtersize(*args):
    for i in tree.get_children():
        tree.delete(i)
    search=sizevar.get()
    minimum,maximum=search.split('-')  
    # print(minimum,maximum)
    with open(filedialogname[0]) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0] !='File Name':    
                a=row[2].split(' ')
                # conver size in mb
                value=None
                if(a[-1]=='kB'):
                    value=float(a[0])/1024
                elif(a[-1]=='gB' or a[-1]=='GB' or a[-1] =='Gb'):
                    value=float(a[0])*1024
                elif (a[-1]=='bytes'):
                    value=float(a[0])/1000000
                elif(a[-1]=='MB'):
                    value=float(a[0])
                # check filter 
                try:
                    if minimum=='Above':
                        if int(maximum) <= value:
                                tree.insert("", 0, values=row)
                                tree.pack()
                    elif minimum=='Below':
                            print(maximum)
                            if int(maximum) >= value:
                                tree.insert("", 0, values=row)
                                tree.pack() 
                    else:
                        if minimum!='Above':
                            if int(maximum) >= value and int(minimum) <=value:
                                tree.insert("", 0, values=row)
                                tree.pack()
                except:
                    pass           
        f.close()
# sorting data when click on button 
count=0  
def sortingdata():
    reve=None
    global count
    if(count==1):
        reve=True
        count=0
    else:
        reve=False
        count=1
    # search=e1_value.get()
    for i in tree.get_children():
        tree.delete(i)
    with open(filedialogname[0]) as f:
        # listvalue=[]
        reader = csv.reader(f, delimiter=',')
        sortedlist = sorted(reader, key=operator.itemgetter(3), reverse=reve)
        for row in sortedlist:
            if row[0] !='File Name':
                tree.insert("", 0, values=row)  
                tree.pack()  
        f.close() 

# use find file from   
def find_file(*event):
    search=e1_value.get().lower()
    for i in tree.get_children():
        tree.delete(i)
    with open(filedialogname[0]) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if (len(search)!=0):
                for i in range(len(row)):
                    if(search in (row[i].lower())):   
                        tree.insert("", 0, values=row)  
                        tree.pack()  
            else:
                tree.insert("", 0, values=row)  
                tree.pack()  
        f.close()    

# use for clic in column then sort 
def treeview_sort_column(tv, col, reverse):
    reve=None
    global count
    if(count==1):
        reve=True
        count=0
    else:
        reve=False
        count=1
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reve)
    # sorted(l,reverse=True)
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda:treeview_sort_column(tv, col, not reverse))
# file_value=StringVar()
e1_value=StringVar()
e1=Entry(root,textvariable=e1_value)
e1.pack()
e1.bind("<Return>",find_file)
button=Button(root,text='Search',command=find_file)
button.pack()

# Sorting csv file data 
button2=Button(root,height=1, width=10,text='sort',command=sortingdata)
button2.pack(side="top", expand=True, padx=0, pady=10)
datechoices=['2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
sizechoice=['Below-0','0-50','51-100','101-150','151-200','201-250','251-300','Above-301']
tkvar=StringVar(root)
tkvar.set('2019')
sizevar=StringVar(root)
sizevar.set('0-50')
popupMenu=OptionMenu(root,tkvar,*datechoices)
# label for display filter 
Label(root,text = 'Choose date ').pack(side="top", fill='x', expand=True, padx=100, pady=10)
popupMenu.pack()

popupMenu2=OptionMenu(root,sizevar,*sizechoice)
Label(root,text = 'Choose Size ').pack(side="top", fill='x', expand=True, padx=10, pady=10)
popupMenu2.pack()
# set size 
tkvar.trace('w',filterdata)
sizevar.trace('w',filtersize)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)

# display csv file in grid view 
tree = ttk.Treeview(TableMargin, columns=('File Name','Directory','File Size','File Type','Create Date','Modify Date','Encoder Settings',"Software",'Aperture Value','Brightness Value','Pixels Per Unit X','Pixels Per Unit Y','Pixel Units','Flash','Image Width','Image Height','Bit Depth','Color Type'
    ,'Compression',"F Number",'ISO','GPS Time Stamp','Aperture','Audio Sample Rate','Movie Data Size','Movie Data Offset','Handler Vendor ID','Audio Bits Per Sample','Image Size','App Version','Creator','Doc Security','Hyperlinks' ,'Changed','LastSaved','Links Up To Date','Scale Crop','Artist','Album','Year','Video Frame Rate','Duration','MPEG Audio Version','Audio Layer','Audio Bitrate','Sample Rate','Channel Mode','MS Stereo','Genre','Copyright Flag','Title','ID3 Size','PDF Version','Linearized','Page Count','Producer','Compatible Brands','Movie Header Version','Time Scale','Duration','Preferred Rate','Preferred Volume','Preview Time','Preview Duration',"Poster Time","Camera Model Name","Make","Resolution Unit",'Megapixels','Filter','Interlace','Significant Bits','Language','Revision Number','Subject','Template','Total Edit Time'), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)

tree.pack()
# diaply file dialog box in which you choose csv file
def Display():
    id=1
    filepath=filedialog.askopenfilename()
    filedialogname.append(filepath)
    with open(filepath) as f:
        listvalue=[]
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:            
            for i in row:
                tree.heading(str(i), text=str(i), anchor=W,command=lambda: treeview_sort_column(tree, i, False))
                tree.column('#'+'2', stretch=NO, minwidth=300, width=400)
                listvalue.append(row[i])
                id+=1
            tree.column('#1', stretch=NO, minwidth=0, width=400)
            tree.insert("", 0, values=listvalue)  
            tree.pack()  
            listvalue.clear()
# open image file when double click
def opencanvas(filepath):
    canvas = Canvas(root, width = 1000, height = 1000)  
    canvas.place(x=0,y=0)  
    img = ImageTk.PhotoImage(PIL.Image.open("/home/amit/Pictures/amit_icard.jpg"))  
    canvas.create_image(-1000, -1000, image=img)
    canvas.config(height=10000, width=10000)

    canvas.image=img
    # run firsr this 
if __name__ == '__main__':
    Display()
    root.mainloop()

