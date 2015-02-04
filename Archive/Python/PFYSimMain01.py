#!/usr/bin/env python
import numpy
import simpy
import uuid
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import sys
import subprocess


# run your program and collect the string output
cmd = ('python PFYSimpyDraft11.py \
    -igc 12 \
    -ogc 12 \
    -tnc 137 \
    -tcl 53.0 \
    -pfw 10.5'
       )
out_str = subprocess.check_output(cmd, shell=True)


# tnc = train_car_count = 137
# tcl = train_car_length = 53
# pfw = pfinder_width = 10.5
# truck_lane_count = 4
# truck_lane_width = 13
# ingate_traffic_separation_length = 100
# outgate_traffic_merge_length = 100
# yard_train_capacity = 2
# truck_count = 274
# igc = ingates_capacity = 10
# ogc = outgates_capacity = 5
# pfinders_capacity = numpy.floor(train_car_count*2)
# iteration_count = 3000
