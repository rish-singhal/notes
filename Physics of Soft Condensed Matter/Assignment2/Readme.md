## Assignment 2

Take dcd file -> load into vmd -> save as pdb

Q1. Take (x, y, z) and a small volume (dx dy dz) around and count the number of
times the atoms visited this volume. And also find the density (N/volume)
.

INPUT: x, y, z, dx, dy, dz 
OUTPUT: n(x,y,z:t)/(dxdydz) (Plot as a function of time -- FRAMES)

Also, calcultate the average of this quantity over time period t.

Q2. Take two points (x1, y1, z1) and (x2, y2, z2), and two volumes (as an input). Calculate the number of FRAMES for which both are non-empty (or there is
atleast one atom in both volumes).

## Assignment 3

Q1. Take all (pairs) and then take distance -> form histogram (FOR ONE FRAME).



## Instructions 

- For getting matplotlib-cpp working, checkout [matplotlib-cpp](https:
//github.com/lava/matplotlib-cpp)

- Run
```bash

g++ script.cpp -std=c++11 -I/usr/include/python3 -lpython3

```

[] Add insturctions for the compilation
[] Use matplotlib-cpp (if it works) else find out alternative
