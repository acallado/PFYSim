#!/usr/bin/env python
import numpy
import simpy
import uuid

train_car_count = 137
train_car_length = 53
pfinder_width = 10.5
truck_lane_count = 4
truck_lane_width = 13
ingate_traffic_separation_length = 100
outgate_traffic_merge_length = 100
yard_train_capacity = 2
truck_count = 10
ingates_capacity = 3
pfinders_capacity = numpy.floor(train_car_count*2)
iteration_count = 20000
ingates = None
trucks = []


class Yard(object):
    def __init__(self):
        self.area = (
            train_car_count *
            (train_car_length + ingate_traffic_separation_length +
                outgate_traffic_merge_length) *
            truck_lane_width *
            truck_lane_count
            )
        self.trucks_active_count = 0
        self.truck_traffic_density = self.trucks_active_count/self.area


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
        self.back_in_time = 0
        self.pfinder_process_time = 0
        self.pull_out_time = 0
        self.travel_to_outgate_time = 0
        self.outgate_queue_time = 0
        self.outgate_process_time = 0
        self.fault_rate = 0
        self.max_in_yard_speed = 30
        self.max_through_gate_speed = 10
        self.acceleration_rate = 1
        self.deceleration_rate = 2
        self.emmision_rate = 1
        self.fuel_consumption_rate = 1
        self.action = env.process(self.run())

    def run(self):
        # Travel to ingates
        self.spawn_time = env.now
        yield self.env.timeout(numpy.random.normal(1.2, 0.1))
        self.ingate_arrival_time = env.now

        # Queue at ingates
        with ingates.request() as req:
            yield req
            self.ingate_process_time = numpy.random.normal(2, 0.3)
            self.ingate_queue_time = env.now - self.ingate_arrival_time
            yield env.timeout(self.ingate_process_time)
            # Went through ingates
            self.ingate_release_time = env.now
            yard.trucks_active_count += 1

        # Head to Pfinder
        self.travel_to_pfinder_time = numpy.random.uniform()

# Setup for run
env = simpy.Environment()

# Create resources
ingates = simpy.Resource(env, capacity=ingates_capacity)
pfinders = simpy.Resource(env, capacity=pfinders_capacity)
yard = Yard()  # Need to convert this to simpy.Resource through class
               # composition later

# Processes
for i in range(truck_count):
    truck = Truck(env)
    trucks.append(truck)
    print (i, truck.tractor_id)

env.run(until=iteration_count)

# Reporting
for t in trucks:
    print(
        t.ingate_arrival_time,
        t.ingate_queue_time,
        t.ingate_process_time,
        t.ingate_release_time
        )
    # for key, val in t.__dict__.items():
    #     print(key, ': ', val)
