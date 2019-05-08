# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 00:10:00 2018

@author: Aditya Chondke
"""




from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import ttk
from tkinter.ttk import Progressbar
from tkinter.messagebox import showinfo
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import webbrowser



path2=""
basefolder=""
progress_bar=""
place=256



class Window(Frame):
    
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master=master
        self.init_window()
    
    def init_window(self):
        self.master.title("HOUGH TRANSFORM")
        self.grid(column=2048, row=2048, sticky=(N, W, E, S))
        
        menu=Menu(self.master)
        self.master.config(menu=menu)
        
        file=Menu(menu)        
        file.add_command(label='Open',command=self.openImg)
        menu.add_cascade(label='File',menu=file)
        
        
        
        edit=Menu(menu)
        edit.add_command(label='Default Hough',command=self.dHough)
        menu.add_cascade(label='Edit',menu=edit)
        edit2=Menu(menu)
        edit.add_command(label='Change directory',command=self.changedir)
        
        help1=Menu(menu)
        help1.add_command(label='Docs',command=self.gohelp)
        menu.add_cascade(label='Help',menu=help1)
        
        
        
        global progress_bar
        progress_bar=ttk.Progressbar(self,orient='horizontal', length=100,mode='indeterminate')
        
        
        button1=Button(self,text="Check Sobel",command=self.sobelout)
        button1.grid(column=240, row=1)
        
        label1=Label(self,text="Sobel Threshold").grid(column=0, row=0 )
        mEntry1=Entry(self,textvariable=ment1).grid(column=120, row=0)
        label1=Label(self,text="Range (RGB)-->[0,4328]         (Greyscale)-->[0, 1803]").grid(column=240, row=0 )
        label3=Label(self,text="Output file name").grid(column=0, row=1 )
        mEntry3=Entry(self,textvariable=ment3).grid(column=120, row=1 )
        label2=Label(self,text="Number of lines to detect").grid(column=0, row=2 )
        mEntry2=Entry(self,textvariable=ment2).grid(column=120, row=2 )
        
        button2=Button(self,text="Calculate Hough",command=self.Hough)
        button2.grid(column=240, row=2)
        
        

    def gohelp(self):
        webbrowser.open_new('https://goo.gl/maAnUR')
        
        
    def sobelout(self):
        mtext1=ment1.get()
        mtext3=ment3.get()
        
        try:
            min=int(mtext1)
            name=str(mtext3)
        except:
            mlabel1=Label(self,text="Enter Valid input").grid(column=0, row=9 )
        
        img = Image.open(path2)
        img.load()
        
        width,height=img.size
        
        
        try:
            p = img.getpixel((0, 0))
            print(p[0])
            type=1
        except:
            type=0
        if(type==1):
            label1=Label(self,text="Range 0 to 4328 ").grid(column=240, row=0 )
            newimg = Image.new("RGB", (width, height), "white")
            image = cv2.imread(path2)
            for x in range(1, width-1): 
                for y in range(1, height-1): 
            
                    
                    Gx = 0
                    Gy = 0
            
                   
                    p = img.getpixel((x-1, y-1))
                    
                    r = p[0]
                    g = p[1]
                    b = p[2]
            
                  
                    intensity = r + g + b
            
                    
                    Gx += -intensity
                    Gy += -intensity
            
                    
                    p = img.getpixel((x-1, y))
                    r = p[0]
                    g = p[1]
                    b = p[2]
            
                    Gx += -2 * (r + g + b)
            
                    p = img.getpixel((x-1, y+1))
                    r = p[0]
                    g = p[1]
                    b = p[2]
            
                    Gx += -(r + g + b)
                    Gy += (r + g + b)
            
                
                    p = img.getpixel((x, y-1))
                    r = p[0]
                    g = p[1]
                    b = p[2]
            
                    Gy += -2 * (r + g + b)
            
                    p = img.getpixel((x, y+1))
                    r = p[0]
                    g = p[1]
                    b = p[2]
            
                    Gy += 2 * (r + g + b)
            
                    
                    p = img.getpixel((x+1, y-1))
                    r = p[0]
                    g = p[1]
                    b = p[2]
            
                    Gx += (r + g + b)
                    Gy += -(r + g + b)
            
                    p = img.getpixel((x+1, y))
                    r = p[0]
                    g = p[1]
                    b = p[2]
            
                    Gx += 2 * (r + g + b)
            
                    p = img.getpixel((x+1, y+1))
                    r = p[0]
                    g = p[1]
                    b = p[2]
            
                    Gx += (r + g + b)
                    Gy += (r + g + b)
            
                   
                    length = math.sqrt((Gx * Gx) + (Gy * Gy))
                    
                  
                  
                    if(length>min):
                        newimg.putpixel((x,y),(255,255,255))
                    else:
                        newimg.putpixel((x,y),(0,0,0))
  
            for i in range(width):
                newimg.putpixel((i,0),(0,0,0))
                newimg.putpixel((i,height-1),(0,0,0))
            for i in range(height):
                newimg.putpixel((0,i),(0,0,0))
                newimg.putpixel((width-1,i),(0,0,0))
                
                   
            sobelpath=basefolder+"\\\\Outputsobel_"+name+".png"
            newimg.save(sobelpath)           
            
            load=Image.open(sobelpath)
            load=load.resize((256,256),Image.ANTIALIAS)
            render=ImageTk.PhotoImage(load)
            img=Label(self,image=render)
            img.image=render
            
            img.grid (column=width+20,row=4 )
            showinfo("Output Saved to Working Directory as Outputsobel_"+name+".png","You can change the sobel threshold value to improve sobel output")
            progress_bar.stop()
            
        else:
            label1=Label(self,text="Range 0 to 1803 ").grid(column=240, row=0 )
            newimg = Image.new("RGB", (width, height), "white")
            image = cv2.imread(path2)
            
            for x in range(1, width-1): 
                for y in range(1, height-1): 
            
                    
                    Gx = 0
                    Gy = 0
          
                    p = img.getpixel((x-1, y-1))
                    r = p
            
                   
                    intensity = r 
            
                    Gx += -intensity
                    Gy += -intensity
            
                    
                    p = img.getpixel((x-1, y))
                    r = p
            
                    Gx += -2 * (r )
            
                    p = img.getpixel((x-1, y+1))
                    r = p
            
                    Gx += -(r)
                    Gy += (r)
            
          
                    p = img.getpixel((x, y-1))
                    r = p
            
                    Gy += -2 * (r)
            
                    p = img.getpixel((x, y+1))
                    r = p
            
                    Gy += 2 * (r)
            
                    p = img.getpixel((x+1, y-1))
                    r = p
                    
                    Gx += (r )
                    Gy += -(r )
            
                    p = img.getpixel((x+1, y))
                    r = p
            
                    Gx += 2 * (r )
            
                    p = img.getpixel((x+1, y+1))
                    r = p
            
                    Gx += (r)
                    Gy += (r)
            
                   
                    length = math.sqrt((Gx * Gx) + (Gy * Gy))
                    
                  
                  
                    if(length>min):
                        newimg.putpixel((x,y),(255,255,255))
                    else:
                        newimg.putpixel((x,y),(0,0,0))
      
            
            for i in range(width):
                newimg.putpixel((i,0),(0,0,0))
                newimg.putpixel((i,height-1),(0,0,0))
            for i in range(height):
                newimg.putpixel((0,i),(0,0,0))
                newimg.putpixel((width-1,i),(0,0,0))
                
                 
            sobelpath=basefolder+"\\\\Outputsobel_"+name+".png"
            newimg.save(sobelpath) 
            
            load=Image.open(sobelpath)
            load=load.resize((256,256),Image.ANTIALIAS)
            render=ImageTk.PhotoImage(load)
            img=Label(self,image=render)
            img.image=render
            
            img.grid (column=width+20,row=4 )
            showinfo("Output Saved to Working Directory as Outputsobel_"+name+".png","You can change the sobel threshold value to improve sobel output")
            
        
    def Hough(self):
        mtext2=ment2.get()
        mtext3=ment3.get()
        image = cv2.imread(path2)
        status=Label(self,text="Calculating Hough",bd=1,relief=SUNKEN,anchor=W)
        status.grid(column=0,row=10)
        progress_bar.grid(column=0,row=5,pady=10)
        
        progress_bar.start()
        try:
            lines=int(mtext2)
            name=str(mtext3)
        except:
            mlabel1=Label(self,text="Enter Valid input").grid(column=0, row=5 )
        
        sobelpath=basefolder+"\\\\Outputsobel_"+name+".png" 
        sobelimg=Image.open(sobelpath)
        sobelimg.load()
        width,height=sobelimg.size
        finalimg = Image.new("RGB", (width, height), "black")
        
   
        k=[]
        for i in range(width):
            for j in range(height):
                if(sobelimg.getpixel((i,j))[0]==255 ):
                        k.append((i,j)) 
   
        
        ex=[]
        ey=[]
        e=[]
        for i in range(len(k)):
            for j in range(0,180,10):
                p=j*math.pi/180
                temp=int((k[i][0]*(np.cos(p)))+(k[i][1]*(np.sin(p))))
                ex.append(p)
                ey.append(temp)
                e.append((p,temp))
                    
                    
        f=Figure(figsize=(3,3),dpi=100)
        a=f.add_subplot(110.5)
        a.plot(ex,ey)
        canvas=FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().grid(column=width+20,row=5)
        
        check=set(e)
        count=[]
        rt=[]
        for i in check:
            t=e.count(i)
            count.append(t)
            rt.append(i)
            
        tt=count[:]
        tt.sort()
       
        val=tt[-lines:]
        
        v=[]
        for i in val:
            temp=count.index(i)
            v.append(rt[temp])
            
        pnt=[[]for _ in range(len(v))] 
       
        for ad in range(len(v)):
            theta=v[ad][0]
            rho=v[ad][1]
            for i in range(len(k)):
                if(rho==int((k[i][0]*(np.cos(theta)))+(k[i][1]*(np.sin(theta))))):
                    pnt[ad].append(k[i])
           
        for i in range(len(pnt)):
            for j in range(len(pnt[i])):
                finalimg.putpixel(pnt[i][j],(255,255,255))
                
                cv2.line(image,pnt[i][0],pnt[i][j],(0,0,255),1)
            
                    
                
                
                
                    
        chough=basefolder+"\\\\HoughOutput_"+name+".png"
        
        cv2.imwrite(chough,image)
        load2=Image.open(chough)
        load2=load2.resize((256,256),Image.ANTIALIAS)
        render=ImageTk.PhotoImage(load2)
        img2=Label(self,image=render)
        img2.image=render
        img2.grid(column=0,row=5)
        
        progress_bar.stop()    
        
        status.destroy()
            

                
        
    
    def openImg(self):
        root=Tk()
        root.fileName=filedialog.askopenfilename( filetypes=( ("All files","*.*"),("Image",".jpeg")))
        tpath=root.fileName
        l=tpath.split("/")
        m=l[:-1]

        global path2
        path2=('\\\\'.join(l))
        global basefolder
        basefolder=('\\\\'.join(m))
        wd=('/'.join(m))
        root.destroy()
        load=Image.open(path2)
        load=load.resize((256,256),Image.ANTIALIAS)
        
        render=ImageTk.PhotoImage(load)
        img=Label(self,image=render)
        img.image=render
        img.grid(column=0,row=4)
        
        showinfo("Image Opened","Working directory set to:  "+wd+"\n\n Working Directory can be changed from edit option")
        
        
        
        
    def dHough(self):
        
        image = cv2.imread(path2)
        name="defualt"
        try:
            name=a=str(ment3.get())
        except:
            mlabel1=Label(self,text="Enter Valid name").pack(side=BOTTOM)
            
        dhoughpath=basefolder+"\\\\DHoughOutput_"+name+".png"
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)
        lines = cv2.HoughLines(edges,1,np.pi/180,100)
        for i in range(len(lines)):
            for rho,theta in lines[i]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                cv2.line(image,(x1,y1),(x2,y2),(0,0,255),1)
                
        cv2.imwrite(dhoughpath,image)
        load=Image.open(dhoughpath)
        render=ImageTk.PhotoImage(load)
        img=Label(self,image=render)
        img.image=render
        
        
        img.grid (column=1200,row=5)
    


    def client_exit(self):
        exit()
        
    def changedir(self):
        temp=askdirectory()
        m=temp.split('/')
        global basefolder
        basefolder=('\\\\'.join(m))
        wd=('/'.join(m))
        showinfo("Working Directory changed","Working directory set to:  "+wd)
        
        
        
        
root=Tk()
ment1=StringVar()
ment2=StringVar()
ment3=StringVar()

root.wm_geometry("2048x2048")
                                                                               
app=Window(root)

root.mainloop()

