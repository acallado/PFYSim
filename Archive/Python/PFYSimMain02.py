#!/usr/bin/env python
import numpy
import simpy
import uuid
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import sys
import subprocess
import configparser


python_sim_file_name = 'PFYSimpyDraft11.py'


def call_subprocess():
    # run your program and collect the string output
    cmd = ('python ' + python_sim_file_name + ' \
    -igc ' + igc.get() + ' \
    -ogc ' + ogc.get() + ' \
    -tnc 137 \
    -tcl 53.0 \
    -pfw 10.5'
           )
    out_str = subprocess.check_output(cmd, shell=True)
    # print(out_str)


# GUI
root = tk.Tk()
root.title(python_sim_file_name)

mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky='N, W, E, S')
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# Parameters
igc = tk.StringVar()
igc.set('5')
ogc = tk.StringVar()
ogc.set('5')
pfc = tk.StringVar()
pfc.set('691')

# Label and entry for ingates count
ttk.Label(
    mainframe,
    text='Ingates count: '
    ).grid(
    column=0, row=0, sticky='W, E'
    )
igc_entry = ttk.Entry(
    mainframe, width=7, textvariable=igc)
igc_entry.grid(column=1, row=0, sticky='W, E')

# Label and entry for outgates count
ttk.Label(
    mainframe,
    text='Outgates count: '
    ).grid(
    column=0, row=1, sticky='W, E'
    )
ogc_entry = ttk.Entry(
    mainframe, width=7, textvariable=ogc)
ogc_entry.grid(column=1, row=1, sticky='W, E')

# Label and entry for pfinder count
ttk.Label(
    mainframe,
    text='Pathfinders count: '
    ).grid(
    column=0, row=2, sticky='W, E'
    )
pfc_entry = ttk.Entry(
    mainframe, width=7, textvariable=pfc)
pfc_entry.grid(column=1, row=2, sticky='W, E')


# Run simulation button
run_button = ttk.Button(mainframe, text='Run', command=call_subprocess)
run_button.grid(
    column=3, row=3, sticky='W')
run_button.bind('<Return>', call_subprocess
root.mainloop()


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
