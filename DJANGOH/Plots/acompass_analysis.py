#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 19:22:43 2021

@author: Stefano Veroni

Analyses the output_evt.dat file and plots. Particular interest given to the
detected and true value of the kinematic variables and the event channel.
"""

import numpy as np
import matplotlib as mlib
import matplotlib.pyplot as plt
import re
import copy
#%%
"RETRIEVE CHANNEL AND KINEMATIC VARIABLES STATISTICS"

ch = ["Channel", ""]

x  = ["Bjorken x", ""]
y  = ["Bjorken y", ""]
nu = ["Virtual's \u03BD", "(Gev)"]
Q2 = ["$Q^2$", "(GeV$^2$)"]
W2 = ["$W^2$", "(GeV$^2$)"]
z0 = ["Bjorken z", ""]
z  = ["Bjorken z", ""]    # t heone without zeroes
Pht0= ["P$_h$$_\perp$", "(Gev/c)"]
Pht= ["P$_h$$_\perp$", "(Gev/c)"]

xtr  = ["Bjorken x", ""]
ytr  = ["Bjorken y", ""]
nutr = ["Virtual's \u03BD","(Gev)"]
Q2tr = ["$Q^2$", "(GeV$^2$)"]
W2tr = ["$W^2$", "(GeV$^2$)"]
ztr0 = ["Bjorken z", ""]
ztr  = ["Bjorken z", ""]    #the one without zeroes
Phttr0= ["P$_h$$_\perp$", "(Gev/c)"]
Phttr= ["P$_h$$_\perp$", "(Gev/c)"]

Det = [x,     y,   nu,   Q2,   W2,   z,   Pht]
Tru = [xtr, ytr, nutr, Q2tr, W2tr, ztr, Phttr]

with open("/home/stefano/DJANGOH-main/acompass_shortevt.dat", 'r') as fl:
    f = fl.readlines()
 
    for ln in f:
        if ln.startswith("  PDF"): #retrieve pdf icode
            pdficode = int(re.findall(r'\d+', ln)[0])
            
        elif ln.startswith("  Total Cross Section"): 
            split = re.split('[+]', re.split('=', ln)[1])
            s = float(split[0])              #cross section (nb)
            serr = float(split[1][2:-3])     #uncertainty   (nb)
        
        elif ln.startswith("Event"):
            ch.append(float(re.findall(r'\d+', ln)[1])) #channel
            
        elif ln.startswith("Det  X"):
            values = re.split(',', re.split('=', ln)[1])
            x.append(float(values[0]))
            y.append(float(values[1]))
            nu.append(float(values[2]))
            Q2.append(float(values[3]))
        elif ln.startswith("Det"):
            values = re.split(',', re.split('=', ln)[1])
            W2.append(float(values[0]))
            z0.append(float(values[1]))
            Pht0.append(float(values[2]))
            if float(values[1]):
                z.append(float(values[1]))
            if float(values[2]):
                Pht.append(float(values[2]))
                    
                  
        elif ln.startswith("True X"):
            valuestr = re.split(',', re.split('=', ln)[1])
            xtr.append(float(valuestr[0]))
            ytr.append(float(valuestr[1]))
            nutr.append(float(valuestr[2]))
            Q2tr.append(float(valuestr[3]))
        elif ln.startswith("True"):
            valuestr = re.split(',', re.split('=', ln)[1])
            W2tr.append(float(valuestr[0]))
            ztr0.append(float(valuestr[1]))
            Phttr0.append(float(valuestr[2]))
            if float(valuestr[1]):
                ztr.append(float(valuestr[1]))
            if float(valuestr[2]):
                Phttr.append(float(valuestr[2]))
#%%

"RETRIEVE Q2MIN & W2MIN"

with open("/home/stefano/DJANGOH-main/acompass_out.dat", 'r') as gl:
    g = gl.readlines()
    
    for ln in g:
        try:
            Q2min = float(re.split("GEV", re.split("Q2MIN=", ln)[1])[0])
        except:  
            try:
                W2min = float(re.split("GEV", re.split("WMIN=", ln)[1])[0])**2
                W2min = round(W2min, 3)
                break
            except:
                continue

#%%

"PLOTTING THE CHANNEL DISTRIBUTION"
chcount = []
labels = []
procs = "\
           1 :non-radiative neutral current \n\
           2 :non-radiative charged current \n\
           3 :non-radiative elastic scattering \n\
           6 :leptonic photon ISR \n\
           7 :leptonic final photon FSR\n\
           8 :Compton event \n\
           9 :quarkonic radiation \n\
          12 :radiative charged current \n\
          13 :quarkonic ISR \n\
          14 :quarkonic FSR \n\
          15 :quasi-elastic with ISR \n\
          16 :quasi-elastic with FSR\n\
          17 :quasi-elastc (Compton type)"
for i in range(1,16):
    c = ch.count(i)
    if c != 0:
        chcount.append(ch.count(i))  
        labels.append(str(i))
plt.figure(figsize=(6,6))
plt.pie(chcount, labels = labels)
plt.annotate("PDF ICODE = %g" %(pdficode), (-0.1, 0.9), \
                 xycoords="axes fraction", size = 10)
plt.annotate("N Events =  %g" %(len(x)-2), (-0.1, 0.85), \
                 xycoords="axes fraction", size = 10)
plt.title("DIS Channels Distribution", size = 17)
plt.savefig("/home/stefano/DJANGOH-main/acompass_ch")
#%%
"DETECTED vs TRUE KINEMATIC VALUES PLOTS"
""""Distinguish values between
                              the first 3 channels,
                              the central 6-9, 
                              the last ones"""

for arrind in range(0, len(Det)): #loop over the kinematic variables arrays
    fv = []
    fvtr = []
    cv = []
    cvtr = []
    lv = []
    lvtr = []
    arr   = Det[arrind]
    arrtr = Tru[arrind]
    i = 2
    while i < len(ch):            #distinguish based on the channel
        if ch[i] <= 3:
            fv.append(arr[i])
            fvtr.append(arrtr[i])
        elif ch[i] < 12:
            cv.append(arr[i])
            cvtr.append(arrtr[i])          
        else:
            lv.append(arr[i])
            lvtr.append(arrtr[i])
        i += 1

    # Plot for the arrindth kinematic variable 
    plt.figure(figsize=(10,7))
    plt.plot(fv, fvtr, ',', label = "Channels 1-3", ls=' ', c="blue")
    plt.plot(cv, cvtr, ',', label = "Channels 6-9", ls=' ', c="red", zorder=0)
    plt.plot(lv, lvtr, ',', label="Channels 12-17", ls=' ', c="green")
    plt.title ("True vs Detected %s" %(arr[0]), size = 18, pad = 12)
    plt.xlabel("Detected Values %s"  %(arr[1]), size = 15)
    plt.ylabel("True Values %s"      %(arr[1]), size = 15)
    plt.legend(loc = "upper left", labelcolor = "linecolor", fontsize = 8, \
               labelspacing = 0.2, columnspacing=0.5)
    plt.grid()
    plt.annotate("N Events =  %g" %(len(x)-2), (0, 1.04), \
                 xycoords="axes fraction", size = 10)
    plt.annotate("PDF ICODE = %g" %(pdficode), (0, 1.01), \
                 xycoords="axes fraction", size = 10)
    plt.annotate("Q2MIN = %g GEV$^2$" %(Q2min), (0.85, 1.04), \
                 xycoords="axes fraction", size = 10)
    plt.annotate("W2MIN = %g GEV$^2$" %(W2min), (0.85, 1.01), \
                 xycoords="axes fraction", size = 10)
    plt.savefig("/home/stefano/DJANGOH-main/acompassplt_%s" %(arr[0]))
    plt.show()
      
#%%
"DETECTED vs TRUE KINEMATIC VALUES: LOGARITHMIC HEIGHTS 2D HISTOGRAMS"

#First compute the relative Deltas: (Atr-A)/Atr for each kinematic variable 

rDs  = [] #it will be a list of numpy arrays, one for each kin variable
tolog = [0, 3, 5] #x, Q2, z

for arrind in range(0, len(Det)): #loop over the kinematic variables arrays
    arr   = copy.deepcopy(Det[arrind])
    arrtr = copy.deepcopy(Tru[arrind])
    del arr[0:2]
    del arrtr[0:2]
    arr   = np.array(arr)
    arrtr = np.array(arrtr)
    rDarr = (arrtr - arr) / arrtr
    rDs.append(rDarr)
    
    N = int(np.sqrt(len(arr)) / 2)
    if arrind in tolog and min(arr) and min(arrtr): #x, Q2, maybe z
        edges   = np.logspace( np.log10(min(arr)),   np.log10( max(arr)),  N)
        edgestr = np.logspace( np.log10(min(arrtr)), np.log10(max(arrtr)), N) 
    else:
        edges   = np.linspace( min(arr),   max(arr),   N)
        edgestr = np.linspace( min(arrtr), max(arrtr), N)
    edgesrD = np.linspace( min(rDarr), max(rDarr), N)      
    
    # HISTOGRAM1
    plt.figure(figsize = (10, 7)) 
    n = mlib.colors.LogNorm()
    plt.hist2d(arrtr, rDarr, bins=[edgestr, edgesrD], norm = n)   
    plt.colorbar()
    if arrind in tolog and min(arr) and min(arrtr):
        plt.xscale("log")
    plt.title ("Detected vs True %s"%(Tru[arrind][0]), size = 17, pad = 12)
    plt.xlabel("True Values %s"     %(Tru[arrind][1]), size = 13)
    plt.ylabel("(True - Det) / True"                 , size = 13) 
    plt.annotate("N Events =  %g" %(len(x)-2), (0, 1.04), \
                 xycoords="axes fraction", size = 10)
    plt.annotate("PDF ICODE = %g" %(pdficode), (0, 1.01), \
                 xycoords="axes fraction", size = 10)
    plt.annotate("Q2MIN = %g GEV$^2$" %(Q2min), (0.85, 1.04), \
                 xycoords="axes fraction", size = 10)
    plt.annotate("W2MIN = %g GEV$^2$" %(W2min), (0.85, 1.01), \
                 xycoords="axes fraction", size = 10)
    plt.annotate("a)", (-0.05, 1.05), xycoords="axes fraction")
    plt.savefig("/home/stefano/DJANGOH-main/acompasshist1_%s" \
                %(Tru[arrind][0]))
    plt.show()
    
    #HISTOGRAM2
    plt.figure(figsize = (10, 7))
    n = mlib.colors.LogNorm()
    plt.hist2d(arrtr, arr, bins=[edgestr, edges], norm = n)
    plt.colorbar()
    if arrind in tolog and min(arr) and min(arrtr):
        plt.xscale("log")
        plt.yscale("log")     
    plt.title ("Detected vs True %s"%(Tru[arrind][0]), size = 17, pad = 12)
    plt.xlabel("True Values %s"     %(Tru[arrind][1]), size = 13)
    plt.ylabel("Detected Values %s" %(Det[arrind][1]), size = 13) 
    plt.annotate("N Events =  %g" %(len(x)-2), (0, 1.04), \
                 xycoords="axes fraction", size = 10)
    plt.annotate("PDF ICODE = %g" %(pdficode), (0, 1.01), \
                 xycoords="axes fraction", size = 10)
    plt.annotate("Q2MIN = %g GEV$^2$" %(Q2min), (0.85, 1.04), \
                 xycoords="axes fraction", size = 10)
    plt.annotate("W2MIN = %g GEV$^2$" %(W2min), (0.85, 1.01), \
                 xycoords="axes fraction", size = 10)
    plt.annotate("b)", (-0.05, 1.05), xycoords="axes fraction")
    plt.savefig("/home/stefano/DJANGOH-main/acompasshist2_%s" \
                %(Tru[arrind][0]))
    plt.show()








