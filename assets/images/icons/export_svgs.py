#!/usr/bin/env python
import os, sys

path='svgs'

cmd = "inkscape -z -e %s.png -w 250 -h 250 %s/%s.svg"

lsdir = os.listdir(path)
for fname in lsdir:
    if '.svg' in fname:
        if 'blue' in fname:
            name = fname.replace('.svg','')
            os.system(cmd % (name, path, name))
        
