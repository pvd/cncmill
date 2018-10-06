#!/bin/bash

maxgeo=root_window.tk.call("wm","maxsize",".")
print "maxgeo=",maxgeo,type(maxgeo)
if type(maxgeo) == tuple:
        fullsize=str(maxgeo[0]) + "x" + str(maxgeo[1])
else:
        fullsize=maxgeo.split(' ')[0] + 'x' + maxgeo.split(' ')[1]
root_window.tk.call("wm","geometry",".",fullsize)
