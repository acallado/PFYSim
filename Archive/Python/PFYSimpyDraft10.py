#!/usr/bin/env python
import numpy
import simpy
import uuid
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import sys


train_car_count = 137
train_car_length = 53
pfinder_width = 10.5
truck_lane_count = 4
truck_lane_width = 13
ingate_traffic_separation_length = 100
outgate_traffic_merge_length = 100
yard_train_capacity = 2
truck_count = 274
ingates_capacity = 10
outgates_capacity = 5
pfinders_capacity = numpy.floor(train_car_count*2)
iteration_count = 3000
ingates = None
trucks = []
mph_to_fpm_factor = 88
env = None
ingates = None
outgates = None
pfinders = None
yard = None

# Command-line parameters
cmdargs = str(sys.argv)
python_file_name = str(sys.argv[0])


class Yard(object):

    def __init__(self):
        self.length = ((train_car_count * train_car_length) +
                       ingate_traffic_separation_length +
                       outgate_traffic_merge_length
                       )
        self.area = (
            train_car_count *
            (train_car_length + ingate_traffic_separation_length +
                outgate_traffic_merge_length) *
            truck_lane_width *
            truck_lane_count
            )
        self.trucks_active_count = 0
        self.truck_traffic_density = 0
        self.ingates_queue_length = []

    def trafficSpeedMultiplier(self):
        # Max trucks = yard area / truck area
        # Truck area = (53 + 20) * 11 = 803 sq ft
        # If density >= 0.8 max -> factor = 0.001
        # If density <= 0.1 max -> factor = 1
        truck_area = 803
        max_truck_count = self.area / truck_area
        # print('Max truck count inside yard: ', max_truck_count)
        max_density = max_truck_count / self.area
        self.truck_traffic_density = self.trucks_active_count/self.area
        if self.truck_traffic_density <= 0.1*max_density:
            multiplier = 1
        elif self.truck_traffic_density >= 0.8*max_density:
            multiplier = 0.01
        else:
            multiplier = 0.5
        return multiplier


class Truck(object):

    def __init__(self, env):
        self.env = env
        self.tractor_id = uuid.uuid4()
        self.ini_cnt_id = 0
        self.end_cnt_id = 0
        self.spawn_time = 0
        self.ingate_arrival_time = 0
        self.ingate_queue_time = 0
        self.ingate_process_time = 0
        self.ingate_release_time = 0
        self.travel_to_pfinder_time = 0
        self.back_in_time = 5
        self.pfinder_process_time = 3
        self.pull_out_time = 2
        self.travel_to_outgate_time = 0
        self.outgate_arrival_time = 0
        self.outgate_queue_time = 1
        self.outgate_process_time = 1
        self.outgate_release_time = 0
        self.fault_rate = 0
        self.max_in_yard_speed = 30*mph_to_fpm_factor
        self.max_through_gate_speed = 10*mph_to_fpm_factor
        self.acceleration_rate = 1
        self.deceleration_rate = 2
        self.emmision_rate = 1
        self.fuel_consumption_rate = 1
        self.action = env.process(self.run())

    def run(self):
        global env
        # Drives to ingates
        self.spawn_time = env.now
        yield self.env.timeout(numpy.random.normal(1.2, 0.1))
        self.ingate_arrival_time = env.now

        # Queues at ingates
        with ingates.request() as req:
            yield req
            print(
                'Ingate queue length: ', len(ingates.queue),
                ' at: ', env.now
                )
            yard.ingates_queue_length.append((env.now, len(ingates.queue)))

            self.ingate_process_time = numpy.random.normal(2, 0.3)
            self.ingate_queue_time = env.now - self.ingate_arrival_time
            yield env.timeout(self.ingate_process_time)
            # Went through ingates
            self.ingate_release_time = env.now
            yard.trucks_active_count += 1
            print('Trucks inside yard: ', yard.trucks_active_count,
                  ' at: ', env.now
                  )

        # Heads to Pfinder
        # print('truck density: ', yard.truck_traffic_density)
        self.travel_to_pfinder_time = (
            (yard.length/2) / (
                self.max_in_yard_speed * yard.trafficSpeedMultiplier())
            )
        yield env.timeout(self.travel_to_pfinder_time)

        # Backs into Pfinder
        yield env.timeout(numpy.random.normal(self.back_in_time, 0.2))

        # Pfinder processing time
        yield env.timeout(numpy.random.normal(self.pfinder_process_time, 0.2))

        # Pulls out of Pfinder
        yield env.timeout(numpy.random.normal(self.pull_out_time, 0.2))

        # Drives to outgates
        self.travel_to_outgate_time = (
            (yard.length/2) / (
                self.max_in_yard_speed * yard.trafficSpeedMultiplier())
            )
        yield env.timeout(self.travel_to_outgate_time)

        # Queues at outgates
        with outgates.request() as req:
            yield req
            self.outgate_process_time = numpy.random.normal(2, 0.3)
            self.outgate_queue_time = env.now - self.outgate_arrival_time
            yield env.timeout(self.outgate_process_time)
            # Went through outgates
            self.outgate_release_time = env.now
            yard.trucks_active_count -= 1
            print('Trucks inside yard: ', yard.trucks_active_count,
                  ' at: ', env.now
                  )


def spawnTrucks(env):
    # Generate inter-arrival times list
    truck_spawn_times = numpy.random.normal(110, 20, 274)
    truck_spawn_times_sorted = sorted(truck_spawn_times)
    truck_interarrival_times = numpy.diff(truck_spawn_times_sorted)
    ini_time = truck_spawn_times_sorted[0]
    yield env.timeout(ini_time)
    for t in truck_interarrival_times:
        yield env.timeout(t)
        truck = Truck(env)
        trucks.append(truck)


def main():
    global env
    global ingates
    global outgates
    global pfinders
    global yard

    # Setup for run
    env = simpy.Environment()

    # Create resources
    ingates = simpy.Resource(env, capacity=ingates_capacity.get())
    outgates = simpy.Resource(env, capacity=outgates_capacity.get())
    pfinders = simpy.Resource(env, capacity=pfinders_capacity.get())

    # Need to convert this to simpy.Resource through class composition later
    yard = Yard()

    # Processes
    env.process(spawnTrucks(env))

    env.run(until=iteration_count)

    # Reporting
    truck_times = []
    for t in trucks:
        print(
            t.ingate_arrival_time,
            t.outgate_release_time,
            t.outgate_release_time - t.ingate_arrival_time
            )
        truck_times.append(t.outgate_release_time - t.ingate_arrival_time)
    x = []
    y = []
    for q in yard.ingates_queue_length:
        print(q[0], q[1])
        x.append(q[0])
        y.append(q[1])

    # Plotting
    # ingate queue x time
    # outgate queue x time
    # truck yard time x truck
    # yard truck count x time
    plt.figure(1)
    plt.plot(truck_times)
    plt.title('PFYard Simulation')
    plt.ylabel('Time spent inside terminal')
    plt.xlabel('Truck number')
    plt.savefig('a.png', dpi=300)
    # plt.show()
    # plt.hist(truck_times, 50)
    plt.figure(2)
    plt.plot(x, y)
    plt.title('PFYard Simulation')
    plt.ylabel('Ingates queue size')
    plt.xlabel('Truck arrival time')
    plt.style.use('ggplot')
    plt.savefig('b.png', dpi=300)
    plt.show()

    # for key, val in t.__dict__.items():
    #     print(key, ': ', val)
# GUI
root = tk.Tk()
root.title(python_file_name)

mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky='N, W, E, S')
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# Parameters
ingates_capacity = tk.IntVar()
ingates_capacity.set(5)
outgates_capacity = tk.IntVar()
outgates_capacity.set(5)
pfinders_capacity = tk.IntVar()
pfinders_capacity.set(691)

# Label and entry for ingates count
ttk.Label(
    mainframe,
    text='Ingates count: '
    ).grid(
    column=0, row=0, sticky='W, E'
    )
ingates_capacity_entry = ttk.Entry(
    mainframe, width=7, textvariable=ingates_capacity)
ingates_capacity_entry.grid(column=1, row=0, sticky='W, E')

# Label and entry for outgates count
ttk.Label(
    mainframe,
    text='Outgates count: '
    ).grid(
    column=0, row=1, sticky='W, E'
    )
outgates_capacity_entry = ttk.Entry(
    mainframe, width=7, textvariable=outgates_capacity)
outgates_capacity_entry.grid(column=1, row=1, sticky='W, E')

# Label and entry for pfinder count
ttk.Label(
    mainframe,
    text='Pathfinders count: '
    ).grid(
    column=0, row=2, sticky='W, E'
    )
pfinders_capacity_entry = ttk.Entry(
    mainframe, width=7, textvariable=pfinders_capacity)
pfinders_capacity_entry.grid(column=1, row=2, sticky='W, E')


# Run simulation button
ttk.Button(mainframe, text='Run', command=main).grid(
    column=3, row=3, sticky='W')

root.mainloop()
