# -*- coding: utf-8 -*-
"""
Created on Tue May 05 02:40:29 2015

@author: Nathaniel Bass
"""

import numpy as np

# Ok, I have data like this:

meta_dt = np.dtype([
    ('mrg', '|f4'),
    ])

meta = np.array([
    (1000, ),  
    (100, ),  
    (1, ), 
    ], dtype=meta_dt, )
    
data_dt = np.dtype([ 
    ('meas', '<f8'),
    ])

data = np.array([
    (0.001, ),
    (45.5, ),
    (0.65, ),
    ], dtype=data_dt, )

meas = data['meas']
mrg = meta['mrg']

# I think this function does what I want it to, now.
# I was really trying to avoid a for loop, but I think
# in this case it is only iterating over a couple dozen 
# entries, so it should not bog down the code

def adc_err(meas, mrg, adc_div=2.0**-16.0):
    '\
    meas : ndarray \n\
        measurements made by the device in real units \n\
    mrg : ndarray \n\
        full range of device used to make measurement \n\
        (0[meas unit] to mrg[meas unit] == 0 V to [1 V, 5 V, or 10 V]) \n\
    adc_div : scalar \n\
        set for 16-bit. \n\
    \n\
    Returns \n\
    ------- \n\
    adc_err : ndarray \n\
        the size in [meas unit] of one step of the adc,  \n\
        based on the total range of the device, \n\
        and the range selected on the adc in response to the measurement \n\
    '
    rg_dict = {
        0.1 : [0.0, 0.09],
        0.5 : [0.09, 0.45],
        1.0 : [0.45, 1.0],
        }
    a = np.divide(meas,mrg)
    
    for i, e in enumerate(a):
        newe = 0.1
        for k, v in rg_dict.items():
            vn, vm = v
            if vn <= e < vm:
                newe = k
        a[i] = newe
    
    a *= 10 # volts, full range of adc
    a *= adc_div
    a *= mrg
    return a

print adc_err(meas, mrg)
