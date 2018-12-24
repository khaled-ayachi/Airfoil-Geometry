"""
@author: khaled
"""

import numpy as np
import matplotlib.pyplot as plt
import os
 

directory = os.getcwd()
airfoil_list = []
new_x = []
new_y = []
x_up = []
y_up = []
x_low = []
y_low = []
X=[]
Y=[]
camberline = []

for i,j,k in os.walk('.'):
    airfoil_list = np.append(airfoil_list,k)

data_list = np.random.choice(airfoil_list,size = 50, replace = True, p =None)

for airfoil in data_list:
        with open(airfoil) as f:
            lines = f.read().splitlines()
        test = any(c.isalpha() for c in lines[0])
        if test == True:
            with open(airfoil, 'r') as fin:
                data = fin.read().splitlines(True)
            with open(airfoil, 'w') as fout:
                fout.writelines(data[1:])
print(data_list)
def plot (name,x,y):
    plt.figure(figsize= (12,10))
    plt.ylim(ymax=0.4)
    plt.ylim(ymin=-0.4)
    plt.plot(x,y, '--', label=name)
    plt.legend()

def normalization(x,y):   
    j = 0
    m = np.max(x)
    for i in x:
        X = [i/ m for i in x]
        Y = [i/ m for i in y]
        j = j + 1
    return(X, Y)

def chord_line (x,y,le,te): 
    plt.plot([0,1], [le, te], ':', label='chordline')
    plt.legend()
    return((le-te)/(0-1))

def mean_camber_line(x,y,x_up,y_up,y_low):
    camber_line = [(y_up[i] + y_low[i])/2 for i in range(0,len(y_up))]
    plt.plot(x_up, camber_line, ':', label='mean camber line')
    plt.legend()
    return(camber_line)

def maximum_thickness(x,y,x_up,y_up,y_low):
    t = [y_up[i] - y_low[i] for i in range(0,len(y_up))]
    index = np.argmax(t)
    location = x_up[index]
    plt.plot([location, location], [y[index], y[-index]], 'o-', label='maximum thickness')
    plt.legend()
    return(index)
    
def panels(name,x,y,x_up, y_up,x_low, y_low):
    plot(name,x,y)
    for i in range(0, len(x_up)):
        # For the upper surface
        plt.plot([x_up[i], x_up[i+1]], [y_up[i], y_up[i+1]],
                 '-o', color='g', alpha=1.0)
        upper_center = (x_up[i+1] + x_up[i])/2, (y_up[i+1] + y_up[i])/2
        slope_1 = (y_up[i+1] - y_up[i])/(x_up[i+1] - x_up[i])
        angle_1 = np.arctan(-1/slope_1)
        if np.sin(angle_1) >=0: 
            u,v = (np.cos(angle_1), np.sin(angle_1))  
        else: 
            u,v = (-np.cos(angle_1), -np.sin(angle_1))
        plt.quiver(upper_center[0], upper_center[1],u, v, color='red', alpha=0.7)
        # For the lower surface
        plt.plot([x_low[i], x_low[i+1]], [y_low[i], y_low[i+1]],
                 '-o', color='g', alpha=1.0)
        lower_center = (x_low[i+1] + x_low[i])/2, (y_low[i+1] + y_low[i])/2
        slope_2 = (y_low[i+1] - y_low[i])/(x_low[i+1] - x_low[i])
        angle_2 = np.arctan(-1/slope_2)
        if np.sin(angle_2) <=0: 
            u,v = (np.cos(angle_2), np.sin(angle_2))  
        else: 
            u,v = (-np.cos(angle_2), -np.sin(angle_2))
        plt.quiver(lower_center[0], lower_center[1],u, v, color='red', alpha=0.7)
    
def Type (x,y):
    slope_1 = (y[0]-y[1])/(x[0]-x[1])
    slope_2 = (y[-1]-y[-2])/(x[-1]-x[-2])
    angle = np.arctan(slope_1) - np.arctan(slope_2)
    if angle == 0:
        result = 'Cusped'
    else:
        result = 'Pointed'
    return(result)

for airfoil in data_list:
    f = np.loadtxt(airfoil, dtype = float)
    x_coordinates = f.T[0]
    y_coordinates = f.T[1]
    
    new_x, new_y = normalization(x_coordinates,y_coordinates)
    
    plot(airfoil,new_x,new_y)
    
    min_x = np.argmin(new_x)
    x_up = new_x[:min_x]
    x_low = new_x[min_x : -1]
    y_up = new_y[:min_x]
    y_low = new_y[min_x : -1]
    
    le = new_y[np.argmin(new_x)]
    te = new_y[np.argmax(new_x)]
   
    chord_line(new_x,new_y,le,te)
    
    mean_camber_line(new_x,new_y,x_up,y_up,y_low)
    
    maximum_thickness(airfoil,new_x,new_y,x_up,y_up,y_low)
    
    panels(airfoil,new_x,new_y,x_up, y_up,x_low, y_low)
    
    Type (new_x, new_y)
    
    plt.legend()
    plt.show()
    
 
    
    
    
    
    