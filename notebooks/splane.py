"""
Combination of 
http://scipy-central.org/item/52/1/zplane-function
and
http://www.dsprelated.com/showcode/244.php
with my own modifications (Own --> Andres Di Donato)
"""

# Copyright (c) 2011 Christopher Felton
# 2018 modified by Andres Di Donato

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# The following is derived from the slides presented by
# Alexander Kain for CS506/606 "Special Topics: Speech Signal Processing"
# CSLU / OHSU, Spring Term 2011.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.pyplot import axvline, axhline, title, grid, figure, xlabel, ylabel
from collections import defaultdict
from scipy.signal import tf2zpk,tf2sos

def pzmap(myFilter):
    """Plot the complex s-plane given zeros and poles.
    Pamams:
     - b: array_like. Numerator polynomial coefficients.
     - a: array_like. Denominator polynomial coefficients.
    
    http://www.ehu.eus/Procesadodesenales/tema6/102.html
    
    """
        
        # Get the poles and zeros
    z, p, k = tf2zpk(myFilter.num, myFilter.den)

    # Create zero-pole plot
    figure#(figsize=(16, 9))
    #subplot(2, 2, 1)
    
   
    # get a figure/plot
    #ax = plt.subplot(1, 1, 1)   # Eric
    fig, ax = plt.subplots()     # Eric

    # Add unit circle and zero axes    
    unit_circle = patches.Circle((0,0), radius=1, fill=False,
                                 color='black', ls='solid', alpha=0.1)
    ax.add_patch(unit_circle)
    axvline(0, color='0.7')
    axhline(0, color='0.7')

    
    #Add circle lines
    
    maxRadius = np.abs(10*np.sqrt(p[0]))
   
    for circleRadius in np.arange(0.5,maxRadius,0.5):

        circle = patches.Circle((0,0), radius=circleRadius, fill=False,
                                 color='black', ls='solid', alpha=0.1)
        ax.add_patch(circle)
        axvline(0, color='0.7')
        axhline(0, color='0.7')
    
    
    
    # Plot the poles and set marker properties
    poles = plt.plot(p.real, p.imag, 'x', markersize=9, alpha=0.5)
    
    # Plot the zeros and set marker properties
    zeros = plt.plot(z.real, z.imag,  'o', markersize=9, 
             color='none', alpha=0.5,
             markeredgecolor=poles[0].get_color(), # same color as poles
             )

    # Scale axes to fit
    r = 1.5 * np.amax(np.concatenate((abs(z), abs(p), [1])))
    plt.axis('scaled')
    plt.axis([-r, r, -r, r])
#    ticks = [-1, -.5, .5, 1]
#    plt.xticks(ticks)
#    plt.yticks(ticks)

    """
    If there are multiple poles or zeros at the same point, put a 
    superscript next to them.
    TODO: can this be made to self-update when zoomed?
    """
    # Finding duplicates by same pixel coordinates (hacky for now):
    poles_xy = ax.transData.transform(np.vstack(poles[0].get_data()).T)
    zeros_xy = ax.transData.transform(np.vstack(zeros[0].get_data()).T)    

    # dict keys should be ints for matching, but coords should be floats for 
    # keeping location of text accurate while zooming

    

    d = defaultdict(int)
    coords = defaultdict(tuple)
    for xy in poles_xy:
        key = tuple(np.rint(xy).astype('int'))
        d[key] += 1
        coords[key] = xy
    for key, value in d.items():
        if value > 1:
            x, y = ax.transData.inverted().transform(coords[key])
            plt.text(x, y, 
                        r' ${}^{' + str(value) + '}$',
                        fontsize=13,
                        )

    d = defaultdict(int)
    coords = defaultdict(tuple)
    for xy in zeros_xy:
        key = tuple(np.rint(xy).astype('int'))
        d[key] += 1
        coords[key] = xy
    for key, value in d.items():
        if value > 1:
            x, y = ax.transData.inverted().transform(coords[key])
            plt.text(x, y, 
                        r' ${}^{' + str(value) + '}$',
                        fontsize=13,
                        )

    

    xlabel(r'$\sigma$')
    ylabel('j'+r'$\omega$')

    grid(True, color='0.9', linestyle='-', which='both', axis='both')
    
    title('Poles and zeros')
    
    # Display zeros, poles and gain
    print(str(len(z)) + " zeros: " + str(z))
    print(str(len(p)) + " poles: " + str(p))
    print("gain: " + str(k))
    
    
    plt.show()

def grpDelay(myFilter):

    w,_,phase = myFilter.bode()

    phaseRad = phase * np.pi / 180.0
    groupDelay = -np.diff(phaseRad)/np.diff(w)

    plt.figure()
    plt.semilogx(w[1::], groupDelay)    # Bode phase plot
    plt.grid(True)
    plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Group Delay [sec]')
    plt.title('Group delay')

    
def bodePlot(myFilter):
    
    w, mag, phase = myFilter.bode()

    plt.figure()
    plt.semilogx(w, mag)    # Bode magnitude plot
    plt.grid(True)
    plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Magnitude response [dB]')
    plt.title('Frequency response')
    
    plt.figure()
    plt.semilogx(w, phase)    # Bode phase plot
    plt.grid(True)
    plt.xlabel('Angular frequency [rad/sec]')
    plt.ylabel('Phase response [deg]')
    plt.title('Frequency response')
    
def convert2SOS(myFilter):
    
    SOSarray = tf2sos(myFilter.num, myFilter.den)
    
    SOSnumber,_ = SOSarray.shape
    
    SOSoutput = np.empty(shape=(SOSnumber,3))
    
    for index in range(SOSnumber):
        SOSoutput[index][:] = SOSarray[index][3::]
        
        if SOSoutput[index][2]==0:
            SOSoutput[index] = np.roll(SOSoutput[index],1)
        
    return SOSoutput