#!/usr/bin/env python
# PFYFOBPerf
# Calculates train turning times for a variety of - yard, pfinder, crane -
#  structural and performance parameters.
# Units: length(ft), time(minutes). speed(ft/s), mass(1000 x lb)

import configparser  # Config file parser
import uuid  # Unique IDs module.
import numpy    # Numerical module.
import math
import datetime  # Date formatting module.
import copy  # For deepcopy capabilities.
import sys  # System interactions.

# Command-line parameters
cmdargs = str(sys.argv)
print('cmdargs: %s' % cmdargs)
python_file_name = str(sys.argv[0])
ini_profile_name = str(sys.argv[1])
ini_file_name = str(sys.argv[2])


class Car(object):  # Calculation.
    def __init__(self,
                 car_id,
                 car_number,
                 container_bottom,
                 container_top,
                 car_occupation,
                 car_position
                 ):
        self.car_id = car_id
        self.car_number = car_number
        self.container_bottom = container_bottom
        self.container_top = container_top
        self.car_occupation = car_occupation
        self.car_position = car_position


class Container(object):  # Calculation.
    def __init__(self, container_id, outbound, container_position):
        self.outbound = outbound
        self.container_id = container_id
        self.container_position = container_position


class PFinderPhysical(object):  # Calculation.
    def __init__(self,
                 pfinder_id,
                 container_bottom,
                 container_top,
                 pfinder_occupation,
                 pfinder_reserved,
                 pfinder_position
                 ):
        self.pfinder_id = pfinder_id
        self.container_bottom = container_bottom
        self.container_top = container_top
        self.pfinder_occupation = pfinder_occupation
        self.pfinder_reserved = pfinder_reserved
        self.pfinder_position = pfinder_position


class FOBPhysical(object):  # Calculation.
    def __init__(self,
                 fob_id,
                 fob_position,
                 dbl_cycle_list,
                 dbl_cycle_action_list,
                 operation_time
                 ):
        self.fob_id = fob_id
        self.fob_position = fob_position
        self.dbl_cycle_list = dbl_cycle_list
        self.dbl_cycle_action_list = dbl_cycle_action_list
        self.traverse_localpos = [0, 0, 0]
        self.house_localpos = [0, 0, 0]
        self.spreader_localpos = [0, 0, 0]
        self.spreader_localangle = 0.0
        self.spreader_loaded = False
        self.operation_time = 0.0


def createPFindersPhysical():  # Calculation.
    pfindersPhysical_list = []
    corrected_pfinder_width = pfinder_width/math.cos(
        math.radians(pfinder_angle))
    corrected_pfinder_length = pfinder_length*math.cos(
        math.radians(pfinder_angle))
    for i in range(pfinders_count):
        pfPosX = corrected_pfinder_width*i
        pfPosY = (
            rail_tracks_count*rail_track_width +
            (rail_tracks_count+1)*rail_track_service_lane_width +
            corrected_pfinder_length/2.0
        )
        pfPos = [pfPosX, pfPosY, 0.0]
        pfinder = PFinderPhysical(i, None, None, 0, False, pfPos)
        pfindersPhysical_list.append(pfinder)
    createDoubleCycleLists(
        fob_count, car_list, pfindersPhysical_list, staging_mode
    )


def createDoubleCycleLists(
        fob_count, car_list,
        pfindersPhysical_list,
        staging_mode):  # Calculation.

    # Create deepcopy of pfindersPhysical_list so we can manipulate it
    # without destroying the original
    pfindersPhysical_list_tmp = copy.deepcopy(pfindersPhysical_list)
    fob_car_list_length = []
    # Divide train car count by the number of FOBs.
    div_remainder = len(car_list) % fob_count
    if div_remainder != 0:
        remainder_wells = div_remainder
        while remainder_wells >= 0:
            fob_car_list_length.append(int(len(car_list)/fob_count)+1)
            remainder_wells = remainder_wells - 1
    else:
        for i in range(fob_count):
            fob_car_list_length.append(int(len(car_list)/fob_count))
    # Staging mode defines how we create the lists
    if staging_mode == 0:  # Double stacking inbounds, well-centered
        print('Double stacking inbounds')
        # For each car, find the closest unnocupied pair of PFinders.
        # First loop to find the first available PFinder.
        fob_car_pfinder_list = []
        for i in range(len(car_list)):
            car_pfinder_distance_min = 10000.0
            pfinder_min = 0
            for j in range(len(pfindersPhysical_list_tmp)):
                # Calculate distance between car and pfinders
                car_pfinder_distance = numpy.array(
                    pfindersPhysical_list_tmp[j].pfinder_position
                    ) - numpy.array(car_list[i].car_position)
                car_pfinder_distance = numpy.sqrt(
                    car_pfinder_distance.dot(car_pfinder_distance)
                )
                if (
                    car_pfinder_distance < car_pfinder_distance_min and
                    pfindersPhysical_list_tmp[j].pfinder_occupation == 0
                ):
                        car_pfinder_distance_min = car_pfinder_distance
                        pfinder_min = j
            fob_car_pfinder_list.append(
                [car_list[i], pfindersPhysical_list_tmp[pfinder_min], 0, None]
            )
        # Remove clo1sest PFinders from list.
        for q in fob_car_pfinder_list:
            pfindersPhysical_list_tmp.pop(
                pfindersPhysical_list_tmp.index(q[1])
            )
        # Second loop to find the second available PFinder.
        for i in range(len(car_list)):
            car_pfinder_distance_min = 10000.0
            pfinder_min = 0
            for j in range(len(pfindersPhysical_list_tmp)):
                # Calculate distance between car and pfinders
                car_pfinder_distance = numpy.array(
                    pfindersPhysical_list_tmp[j].pfinder_position
                    ) - numpy.array(car_list[i].car_position)
                car_pfinder_distance = numpy.sqrt(car_pfinder_distance.dot(
                    car_pfinder_distance))
                if (
                    car_pfinder_distance < car_pfinder_distance_min and
                    pfindersPhysical_list_tmp[j].pfinder_occupation == 0
                ):
                    car_pfinder_distance_min = car_pfinder_distance
                    pfinder_min = j
            fob_car_pfinder_list[i][2] = pfindersPhysical_list_tmp[pfinder_min]
        # Remove second closest PFinders from list.
        for q in fob_car_pfinder_list:
            pfindersPhysical_list_tmp.pop(
                pfindersPhysical_list_tmp.index(q[2]))
            # pdb.set_trace()
        # Define first car per FOB.
        first_car_list = []
        for m in range(fob_count):
            first_car_list.append(car_list[m*fob_car_list_length[0]])
        for p in fob_car_pfinder_list:
            try:
                print(p[0].car_number, p[1].pfinder_id, p[2].pfinder_id)
            except:
                print(p[0].car_number, p[1].pfinder_id, p[2].pfinder_id)
        # Populate PFinders with containers.
        #  For each car
        for n in fob_car_pfinder_list:
            #  Pick first PFinder fom car group.
            outbound_pfinder_position = n[1].pfinder_position
        # Generate two outbound containers,
        # position = PFinder pos, except for height.
            cnt_top = Container(uuid.uuid4(), True, (
                outbound_pfinder_position + numpy.array(
                    [
                        0.0, 0.0, container_dimensions[2]
                        + pfinder_top_shoes_height
                    ]
                    )))
            cnt_bottom = Container(uuid.uuid4(), True, (
                outbound_pfinder_position + numpy.array(
                    [
                        0.0, 0.0, container_dimensions[2]
                        + pfinder_bottom_shoes_height
                    ]
                    )))
        # Update PFinder occupation.
            n[1].container_bottom = cnt_bottom
            n[1].container_top = cnt_top
            n[1].pfinder_occupation = 2
            n[1].pfinder_reserved = True
        # Create movement list for each FOB.
        unique_fob_car_pfinder_list = []
        # For each FOB
        for r in range(fob_count):
            # Create new list from fob_car_pfinder_list starting at the
            #  first_car[r] and ending with
            #  unique_fob_car_pfinder_list_length[0]
            if r != fob_count-1:
                unique_fob_car_pfinder_list.append(
                    fob_car_pfinder_list[r*fob_car_list_length[0]:(
                        r*fob_car_list_length[0])+(fob_car_list_length[0])]
                )
            else:
                unique_fob_car_pfinder_list.append(fob_car_pfinder_list[
                    r*fob_car_list_length[0]:])
        fob_list = []
        for k in range(fob_count):
            # For each car in unique_fob_car_pfinder_list.
            # for cr in unique_fob_car_pfinder_list:
            fob = FOBPhysical(
                k, None, unique_fob_car_pfinder_list[k], None, 0.0)
            fob.fob_position = numpy.array([(
                fob.dbl_cycle_list[0][0].car_position[0]-(car_length/2.0) +
                (fob_length/2)), fob_width/2.0, 0.0])
            fob_list.append(fob)
        # Create action sequence for each FOB
        #  (cppccppppccccppppc...pccccppccppppccppc)
        #  where c is car and p is pfinder
        # For each FOB.
        for f in fob_list:
            unique_fob_car_pfinder_action_list = []
            # f.dbl_cycle_list[0][0] is the car inside fob_car_pfinder_list
            # f.dbl_cycle_list[0][1] is the first pfinder
            print('##################### FOB %s List begin ##### ' % f.fob_id)
            # For each FOB list.
            # For each line in each FOB list.
            x = 0
            for x in range(len(f.dbl_cycle_list)):
                if x == 0:  # First car has to be emptied before dbl cycling
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][0])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][2])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][0])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][2])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][1])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][0])
                elif x != (len(f.dbl_cycle_list))-1:
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][0])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][2])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x-1][1])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x-1][0])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][0])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][2])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][1])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][0])
                else:  # Last car does not dbl cycle to -nonexistent- next car
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][0])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][2])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x-1][1])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x-1][0])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][0])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][2])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][1])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][0])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][1])
                    unique_fob_car_pfinder_action_list.append(
                        f.dbl_cycle_list[x][0])
                x = x+1
            f.dbl_cycle_action_list = unique_fob_car_pfinder_action_list
            executeDblCycle(f)
    elif staging_mode == 1:  # Single stacking inbounds, well-centered
        print('Single stacking inbounds')
        # For each car, find the closest three unnocupied of PFinders.
        # First loop to find the first available PFinder.
        fob_car_pfinder_list = []
        for i in range(len(car_list)):
            car_pfinder_distance_min = 10000.0
            pfinder_min = 0
            for j in range(len(pfindersPhysical_list_tmp)):
                # Calculate distance between car and pfinders
                car_pfinder_distance = (numpy.array(
                    pfindersPhysical_list_tmp[j].pfinder_position) -
                    numpy.array(car_list[i].car_position))
                car_pfinder_distance = numpy.sqrt(
                    car_pfinder_distance.dot(car_pfinder_distance))
                if (car_pfinder_distance < car_pfinder_distance_min and
                        pfindersPhysical_list_tmp[j].pfinder_occupation == 0):
                    car_pfinder_distance_min = car_pfinder_distance
                    pfinder_min = j
            fob_car_pfinder_list.append(
                [car_list[i], pfindersPhysical_list_tmp[pfinder_min], 0, None])
        # Remove closest PFinders from list.
        for q in fob_car_pfinder_list:
            pfindersPhysical_list_tmp.pop(
                pfindersPhysical_list_tmp.index(q[1]))
        # Second loop to find the second available PFinder.
        for i in range(len(car_list)):
            car_pfinder_distance_min = 10000.0
            pfinder_min = 0
            for j in range(len(pfindersPhysical_list_tmp)):
                # Calculate distance between car and pfinders
                car_pfinder_distance = numpy.array(
                    pfindersPhysical_list_tmp[j].pfinder_position
                ) - numpy.array(car_list[i].car_position)
                car_pfinder_distance = numpy.sqrt(
                    car_pfinder_distance.dot(car_pfinder_distance))
                if (car_pfinder_distance < car_pfinder_distance_min and
                        pfindersPhysical_list_tmp[j].pfinder_occupation == 0):
                    car_pfinder_distance_min = car_pfinder_distance
                    pfinder_min = j
            fob_car_pfinder_list[i][2] = pfindersPhysical_list_tmp[pfinder_min]
        # Remove second closest PFinders from list.
        for q in fob_car_pfinder_list:
            pfindersPhysical_list_tmp.pop(
                pfindersPhysical_list_tmp.index(q[2]))
        # Third loop to find the third available PFinder.
        for i in range(len(car_list)):
            car_pfinder_distance_min = 10000.0
            pfinder_min = 0
            for j in range(len(pfindersPhysical_list_tmp)):
                # Calculate distance between car and pfinders
                car_pfinder_distance = numpy.array(
                    pfindersPhysical_list_tmp[j].pfinder_position
                ) - numpy.array(car_list[i].car_position)
                car_pfinder_distance = numpy.sqrt(
                    car_pfinder_distance.dot(car_pfinder_distance))
                if (car_pfinder_distance < car_pfinder_distance_min and
                        pfindersPhysical_list_tmp[j].pfinder_occupation == 0):
                    car_pfinder_distance_min = car_pfinder_distance
                    pfinder_min = j
            fob_car_pfinder_list[i][3] = pfindersPhysical_list_tmp[pfinder_min]
        # Remove second closest PFinders from list.
        for q in fob_car_pfinder_list:
            pfindersPhysical_list_tmp.pop(
                pfindersPhysical_list_tmp.index(q[3]))
        # Define first car per FOB.
        first_car_list = []
        for m in range(fob_count):
            first_car_list.append(car_list[m*fob_car_list_length[0]])
        for p in fob_car_pfinder_list:
            try:
                print(
                    p[0].car_number, p[1].pfinder_id,
                    p[2].pfinder_id, p[3].pfinder_id)
            except:
                print(p[0].car_number, p[1].pfinder_id,
                      p[2].pfinder_id, p[3].pfinder_id)
        # Populate PFinders with containers.
        #       For each car
        for n in fob_car_pfinder_list:
            # Pick first PFinder fom car group.
            outbound_pfinder_position = n[1].pfinder_position
        # Generate two outbound containers,
        #  position = PFinder pos, except for height.
            cnt_top = Container(uuid.uuid4(), True, (
                outbound_pfinder_position + numpy.array(
                    [0.0, 0.0, container_dimensions[2] +
                        pfinder_top_shoes_height])))
            cnt_bottom = Container(uuid.uuid4(), True, (
                outbound_pfinder_position + numpy.array(
                    [0.0, 0.0, container_dimensions[2] +
                     pfinder_bottom_shoes_height])))
        # Update PFinder occupation.
            n[1].container_bottom = cnt_bottom
            n[1].container_top = cnt_top
            n[1].pfinder_occupation = 2
            n[1].pfinder_reserved = True
        # Create movement list for each FOB.
        unique_fob_car_pfinder_list = []
        # For each FOB
        for r in range(fob_count):
            # Create new list from fob_car_pfinder_list starting at the
            #  first_car[r] and ending
            #  with unique_fob_car_pfinder_list_length[0]
            if r != fob_count-1:
                unique_fob_car_pfinder_list.append(
                    fob_car_pfinder_list[r*fob_car_list_length[0]:(
                        r*fob_car_list_length[0])+(fob_car_list_length[0])])
            else:
                unique_fob_car_pfinder_list.append(
                    fob_car_pfinder_list[r*fob_car_list_length[0]:])
        fob_list = []
        for k in range(fob_count):
            # For each car in unique_fob_car_pfinder_list.
            # for cr in unique_fob_car_pfinder_list:
            fob = FOBPhysical(
                k, None, unique_fob_car_pfinder_list[k], None, 0.0)
            fob.fob_position = numpy.array(
                [
                    (
                        fob.dbl_cycle_list[0][0].car_position[0]-(
                            car_length/2.0
                        ) + (fob_length/2)
                    ), fob_width/2.0, 0.0
                ])
            fob_list.append(fob)
        # Create action sequence for each FOB (ciciococ|ciciococG...) where
        # c is car and i is inbound pfinder and o is outbound pfinder
        # For each FOB.
        for f in fob_list:
            unique_fob_car_pfinder_action_list = []
            # f.dbl_cycle_list[0][0] is the car inside fob_car_pfinder_list
            # f.dbl_cycle_list[0][1] is the first pfinder
            print('##################### FOB %s List begin #### ' % f.fob_id)
            # For each FOB list.
            # For each line in each FOB list.
            x = 0
            for x in range(len(f.dbl_cycle_list)):
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][0])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][2])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][0])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][3])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][1])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][0])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][1])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][0])
                x = x+1
            f.dbl_cycle_action_list = unique_fob_car_pfinder_action_list
            executeDblCycle(f)
    elif staging_mode == 2:  # Single stacking inbounds, well-ranged
        print('Single stacking inbounds, well-ranged')
        # For each car, find the closest three unnocupied of PFinders.
        # First loop to find the first available PFinder.
        fob_car_pfinder_list = []
        car_max_x_range = []
        car_min_x_range = []
        for i in range(len(car_list)):
            # Determine which PFinders are in front of a well
            # Set x range for "in front of a well"
            car_max_x_range.append(
                car_list[i].car_position[0] +
                car_length/2.0 - pfinder_width/2.0)
            car_min_x_range.append(
                car_list[i].car_position[0] -
                car_length/2.0 + pfinder_width/2.0)
            pfinders_in_range = []
            for j in range(len(pfindersPhysical_list_tmp)):
                # If PFinder position x is within the min max x well range,
                #  add it to a list
                if (pfindersPhysical_list_tmp[j].pfinder_position[0] <
                        car_max_x_range[i] and
                        pfindersPhysical_list_tmp[j].pfinder_position[0] >
                        car_min_x_range[i]):
                    pfinders_in_range.append(pfindersPhysical_list_tmp[j])
            # From that list, choose 3 PFinders randomly
            rand_num = numpy.random.random_integers(
                0, len(pfinders_in_range)-1)
            first_pfinder = pfinders_in_range[rand_num]
            fob_car_pfinder_list.append(
                [car_list[i], first_pfinder, 0, None])
            pfinders_in_range.remove(first_pfinder)
            rand_num = numpy.random.random_integers(
                0, len(pfinders_in_range)-1)
            second_pfinder = pfinders_in_range[rand_num]
            fob_car_pfinder_list[i][2] = second_pfinder
            pfinders_in_range.remove(second_pfinder)
            rand_num = numpy.random.random_integers(
                0, len(pfinders_in_range)-1)
            third_pfinder = pfinders_in_range[rand_num]
            fob_car_pfinder_list[i][3] = third_pfinder
            pfinders_in_range.remove(third_pfinder)
        # Define first car per FOB.
        first_car_list = []
        for m in range(fob_count):
            first_car_list.append(car_list[m*fob_car_list_length[0]])
        # Populate PFinders with containers.
        #       For each car
        for n in fob_car_pfinder_list:
            # Pick first PFinder fom car group.
            outbound_pfinder_position = n[1].pfinder_position
        # Generate two outbound containers,
        #  position = PFinder pos, except for height.
            cnt_top = Container(uuid.uuid4(), True, (
                outbound_pfinder_position + numpy.array(
                    [0.0, 0.0, container_dimensions[2] +
                     pfinder_top_shoes_height])))
            cnt_bottom = Container(uuid.uuid4(), True, (
                outbound_pfinder_position + numpy.array(
                    [0.0, 0.0, container_dimensions[2] +
                     pfinder_bottom_shoes_height])))
        # Update PFinder occupation.
            n[1].container_bottom = cnt_bottom
            n[1].container_top = cnt_top
            n[1].pfinder_occupation = 2
            n[1].pfinder_reserved = True
        # Create movement list for each FOB.
        unique_fob_car_pfinder_list = []
        # For each FOB
        for r in range(fob_count):
            # Create new list from fob_car_pfinder_list starting at the
            #  first_car[r] and ending with
            #  unique_fob_car_pfinder_list_length[0]
            if r != fob_count-1:
                unique_fob_car_pfinder_list.append(
                    fob_car_pfinder_list[r*fob_car_list_length[0]:(
                        r*fob_car_list_length[0])+(fob_car_list_length[0])])
            else:
                unique_fob_car_pfinder_list.append(
                    fob_car_pfinder_list[r*fob_car_list_length[0]:])
        fob_list = []
        for k in range(fob_count):
            # For each car in unique_fob_car_pfinder_list.
            # for cr in unique_fob_car_pfinder_list:
            fob = FOBPhysical(
                k, None, unique_fob_car_pfinder_list[k], None, 0.0)
            fob.fob_position = numpy.array([(
                fob.dbl_cycle_list[0][0].car_position[0]-(car_length/2.0) +
                (fob_length/2)), fob_width/2.0, 0.0])
            fob_list.append(fob)
        # Create action sequence for each FOB (
        # ciciococ|ciciococG...) wher c is car and i is inbound pfinder and
        # o is outbound pfinder
        # For each FOB.
        for f in fob_list:
            unique_fob_car_pfinder_action_list = []
            # f.dbl_cycle_list[0][0] is the car inside fob_car_pfinder_list
            # f.dbl_cycle_list[0][1] is the first pfinder
            print('##################### FOB %s List begin ##### ' % f.fob_id)
            # For each FOB list.
            # For each line in each FOB list.
            x = 0
            for x in range(len(f.dbl_cycle_list)):
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][0])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][2])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][0])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][3])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][1])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][0])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][1])
                unique_fob_car_pfinder_action_list.append(
                    f.dbl_cycle_list[x][0])
                x = x+1
            f.dbl_cycle_action_list = unique_fob_car_pfinder_action_list
            executeDblCycle(f)


def executeDblCycle(fob):  # Calculation.
    cnt_move_type = -1
    for item in fob.dbl_cycle_list:
        print('***' + str(item[0].container_top.container_id))
    fob_spreader_position = (numpy.array(fob.fob_position) +
                             numpy.array([0, 0, fob_spreader_max_height]))
    # Defines FOB reach limits
    fob_top_x_limit = fob.fob_position[0] + fob_length/2
    fob_low_x_limit = fob.fob_position[0] - fob_length/2
    # Goes over each FOB action list (nodes, not trajectory)
    for move in fob.dbl_cycle_action_list:
        # Initializes move_vector
        move_vector = [0, 0, 0]
        # Begin FOB Gantry
        # Is our target within reach? Do we need to gantry the FOB?
        try:
            if move.car_position[0] > fob_top_x_limit:
                calcFOBMove(fob, cycle_mode, 'forward', fob_spreader_position)
            elif move.car_position[0] < fob_low_x_limit:
                calcFOBMove(fob, cycle_mode, 'reverse', fob_spreader_position)
        except:
            if move.pfinder_position[0] > fob_top_x_limit:
                calcFOBMove(fob, cycle_mode, 'forward', fob_spreader_position)
            elif move.pfinder_position[0] < fob_low_x_limit:
                calcFOBMove(fob, cycle_mode, 'reverse', fob_spreader_position)
        fob_top_x_limit = fob.fob_position[0] + fob_length/2
        fob_low_x_limit = fob.fob_position[0] - fob_length/2
        # End FOB Gantry
        # Begin Spreader Move
        # Calculating spreader translation vector.
        try:
            if move.car_occupation == 2:  # 0 Grabs container from car top pos
                move.car_position = move.container_top.container_position
                move.car_occupation = move.car_occupation - 1
                fob.spreader_loaded = True
                cnt_move_type = 0
            elif move.car_occupation == 1:  # 1 Drops container on car top pos
                if fob.spreader_loaded:
                    move.car_position = move.container_top.container_position
                    move.car_occupation = move.car_occupation + 1
                    fob.spreader_loaded = False
                    cnt_move_type = 1
                else:  # 2 Grabs container from car bot pos
                    move.car_position = (move.container_bottom.
                                         container_position)
                    move.car_occupation = move.car_occupation - 1
                    fob.spreader_loaded = True
                    cnt_move_type = 2
            else:  # 3 Drops container on car bot pos
                move.car_position = (
                    move.car_position[0],
                    move.car_position[1],
                    (car_height + container_dimensions[2])
                )
                move.car_occupation = move.car_occupation + 1
                fob.spreader_loaded = False
                cnt_move_type = 3
            node_pos = numpy.array(move.car_position)
        except:
            if fob.spreader_loaded is True:  # 4 Drops container on PFinder
                move.pfinder_occupation = move.pfinder_occupation + 1
                fob.spreader_loaded = False
                cnt_move_type = 4
            else:  # 5 Grabs container from PFinder
                move.pfinder_occupation = move.pfinder_occupation - 1
                fob.spreader_loaded = True
                cnt_move_type = 5
            move.pfinder_position[2] = (pfinder_top_shoes_height +
                                        container_dimensions[2] + 2.0)
            node_pos = numpy.array(move.pfinder_position)
        # End Spreader Move
        print('\n\n-> Calling calcSpreaderMove->node_pos: ' + str(node_pos))
        fob_spreader_position = calcSpreaderMove(
            fob, node_pos, fob_spreader_position, cnt_move_type)

    for r in a_reg_movement:
        print(str(r[0]) + ', ' + str(r[1][0]) + ', ' + str(r[1][1]) + ', '
              + str(r[1][2]) + ', ' + str(r[2]) + ', ' + str(r[3]))
    trajectoryScriptGenerator()


def calcFOBMove(fob, cycle_mode, direction, fob_spreader_position):
    print('Calculating FOB move...')
    fob_gantry_move_time = 0.0
    if direction == 'forward':
        fob.fob_position = numpy.array(fob.fob_position)
        + numpy.array([fob_displacement_positive_x, 0.0, 0.0])
        fob_gantry_move_time = calcFOBMoveTime(fob_displacement_positive_x)
        if cycle_mode == 1:  # Non-overlapping gantry
            fob_spreader_position = (numpy.array(fob_spreader_position)
                                     + numpy.array([car_length, 0.0, 0.0]))
    else:
        fob.fob_position = (numpy.array(fob.fob_position)
                            - numpy.array(
                                [fob_displacement_negative_x, 0.0, 0.0]))
        fob_gantry_move_time = calcFOBMoveTime(fob_displacement_negative_x)
        if cycle_mode == 1:  # Non-overlapping gantry
            fob_spreader_position = (numpy.array(fob_spreader_position)
                                     - numpy.array([car_length, 0.0, 0.0]))
    fob.operation_time += fob_gantry_move_time
    print('FOB Ops Time: ' + str(fob.operation_time))


def calcFOBMoveTime(distance):
    print('Calculating FOB move time...')
    time_gantry = 0.0
    if distance < 2*fob_gantry_ramp_distance:
        time_gantry = 2*numpy.sqrt(distance/fob_gantry_ramp_acceleration)
    else:
        time_gantry = (
            distance-(2*fob_gantry_ramp_distance)
        )/fob_gantry_speed + 2*fob_gantry_ramp_seconds*0.01667
    return time_gantry


def calcSpreaderMove(fob, node_pos, spreader_pos, cnt_move_type):
    print('NMNMNM -> ' + str(cnt_move_type))
    # Determine if we are dealing with car or PFinder
    if cnt_move_type == 0:
        print(
            'YYY FOB ' + str(fob.fob_id) + ' is grabbing cnt ' +
            str(fob.dbl_cycle_action_list[0].container_top.container_id))
    move_vector_partial = numpy.array([0.0, 0.0, 0.0])
    time = 0.0
    print('> BEGIN calcSpreaderMove spreader_pos: ' + str(spreader_pos))
    print('Inside calcSpreaderMove node_pos: ' + str(node_pos))
    # If the spreader is at the highest, skip first hoist.
    if spreader_pos[2] >= fob_spreader_max_height:
        print('\nSpreader at max height')
        # Go to XY.
        print('Moving to XY and rotating...')
        move_vector_partial = goToXY(node_pos, spreader_pos)
        time = calcSpreaderMoveTime(move_vector_partial)
        fob.operation_time += time
        print('time: ' + str(time))
        spreader_pos = numpy.array(
            spreader_pos) + numpy.array(move_vector_partial)
        print('SPREADER_POS: ' + str(spreader_pos))
        a_reg_movement.append(
            [fob.fob_id, spreader_pos, time, fob.operation_time])
        # Hoist down.
        print('Hoisting down...')
        mode = 0
        move_vector_partial = goToZ(node_pos, spreader_pos, mode)
        time = calcSpreaderMoveTime(move_vector_partial)
        fob.operation_time += time
        print('time: ' + str(time))
        spreader_pos = numpy.array(
            spreader_pos) + numpy.array(move_vector_partial)
        print('SPREADER_POS: ' + str(spreader_pos))
        a_reg_movement.append(
            [fob.fob_id, spreader_pos, time, fob.operation_time])
    elif node_pos[2] == spreader_pos[2]:  # Spreader at the same height as target
        print('\nSpreader is at the same height as target')
        # Hoist up clear height.
        print('Hoisting up clear height')
        mode = 1
        move_vector_partial = goToZ(node_pos, spreader_pos, mode)
        time = calcSpreaderMoveTime(move_vector_partial)
        fob.operation_time += time
        print('time: ' + str(time))
        spreader_pos = numpy.array(
            spreader_pos) + numpy.array(move_vector_partial)
        print('SPREADER_POS: ' + str(spreader_pos))
        a_reg_movement.append(
            [fob.fob_id, spreader_pos, time, fob.operation_time])
        # Move XY and rotate.
        print('Moving to XY and rotating')
        move_vector_partial = goToXY(node_pos, spreader_pos)
        time = calcSpreaderMoveTime(move_vector_partial)
        fob.operation_time += time
        print('time: ' + str(time))
        spreader_pos = numpy.array(
            spreader_pos) + numpy.array(move_vector_partial)
        print('SPREADER_POS: ' + str(spreader_pos))
        a_reg_movement.append(
            [fob.fob_id, spreader_pos, time, fob.operation_time])
        # Hoist down clear height.
        print('Hoisting down clear height')
        mode = 2
        move_vector_partial = goToZ(node_pos, spreader_pos, mode)
        time = calcSpreaderMoveTime(move_vector_partial)
        fob.operation_time += time
        print('time: ' + str(time))
        spreader_pos = numpy.array(
            spreader_pos) + numpy.array(move_vector_partial)
        print('SPREADER_POS: ' + str(spreader_pos))
        a_reg_movement.append(
            [fob.fob_id, spreader_pos, time, fob.operation_time])
    elif node_pos[2] < spreader_pos[2]:  # Spreader above target.
        print('\nSpreader is above target.')
        # Hoist up clear height.
        print('Hoisting up clear height')
        mode = 1
        move_vector_partial = goToZ(node_pos, spreader_pos, mode)
        time = calcSpreaderMoveTime(move_vector_partial)
        fob.operation_time += time
        print('time: ' + str(time))
        spreader_pos = numpy.array(
            spreader_pos) + numpy.array(move_vector_partial)
        print('SPREADER_POS: ' + str(spreader_pos))
        a_reg_movement.append(
            [fob.fob_id, spreader_pos, time, fob.operation_time])
        # Move XY and rotate.
        print('Moving to XY and rotating')
        move_vector_partial = goToXY(node_pos, spreader_pos)
        time = calcSpreaderMoveTime(move_vector_partial)
        fob.operation_time += time
        print('time: ' + str(time))
        spreader_pos = numpy.array(
            spreader_pos) + numpy.array(move_vector_partial)
        print('SPREADER_POS: ' + str(spreader_pos))
        a_reg_movement.append(
            [fob.fob_id, spreader_pos, time, fob.operation_time])
        # Hoist down clear height + abs(node_pos[2]).
        print('Hoisting down clear height + abs(node_pos[2])')
        mode = 4
        move_vector_partial = goToZ(node_pos, spreader_pos, mode)
        time = calcSpreaderMoveTime(move_vector_partial)
        fob.operation_time += time
        print('time: ' + str(time))
        spreader_pos = numpy.array(
            spreader_pos) + numpy.array(move_vector_partial)
        print('SPREADER_POS: ' + str(spreader_pos))
        a_reg_movement.append(
            [fob.fob_id, spreader_pos, time, fob.operation_time])
    elif node_pos[2] > spreader_pos[2]:  # Spreader below target.
        print('\nSpreader is below target')
        # Hoist up clear height + abs(node_pos[2])
        print('Hoisting up clear height + ' + str(abs(node_pos[2])))
        mode = 3
        move_vector_partial = goToZ(node_pos, spreader_pos, mode)
        time = calcSpreaderMoveTime(move_vector_partial)
        fob.operation_time += time
        print('time: ' + str(time))
        spreader_pos = numpy.array(
            spreader_pos) + numpy.array(move_vector_partial)
        print('SPREADER_POS: ' + str(spreader_pos))
        a_reg_movement.append(
            [fob.fob_id, spreader_pos, time, fob.operation_time])
        # Move XY and rotate.
        print('Moving to XY and rotating')
        move_vector_partial = goToXY(node_pos, spreader_pos)
        time = calcSpreaderMoveTime(move_vector_partial)
        fob.operation_time += time
        print('time: ' + str(time))
        spreader_pos = numpy.array(
            spreader_pos) + numpy.array(move_vector_partial)
        print('SPREADER_POS: ' + str(spreader_pos))
        a_reg_movement.append(
            [fob.fob_id, spreader_pos, time, fob.operation_time])
        # Hoist down clear height.
        print('Hoisting down clear height')
        mode = 2
        move_vector_partial = goToZ(node_pos, spreader_pos, mode)
        time = calcSpreaderMoveTime(move_vector_partial)
        fob.operation_time += time
        print('time: ' + str(time))
        spreader_pos = numpy.array(
            spreader_pos) + numpy.array(move_vector_partial)
        print('SPREADER_POS: ' + str(spreader_pos))
        a_reg_movement.append(
            [fob.fob_id, spreader_pos, time, fob.operation_time])
    print('> END calcSpreaderMove returning spreader_pos: '
          + str(spreader_pos))
    return spreader_pos


def goToXY(node_pos, spreader_pos):
    move_vector_partial = numpy.array([0.0, 0.0, 0.0])
    print('* BEGIN goToXY')
    print('Moving to XY and rotating...')
    move_vector_partial = numpy.array([
        node_pos[0] - spreader_pos[0],
        node_pos[1] - spreader_pos[1],
        0.0])
    print('* END goToXY returning move_vector_partial: '
          + str(move_vector_partial))
    return move_vector_partial


def goToZ(node_pos, spreader_pos, mode):
    move_vector_partial = numpy.array([0.0, 0.0, 0.0])
    print('! BEGIN goToZ')
    print('Hoisting to Z...')
    if mode == 0:  # Hoist down from max height
        move_vector_partial = numpy.array([
            0.0,
            0.0,
            node_pos[2]-spreader_pos[2]])
    elif mode == 1:  # Hoist up clear height
        move_vector_partial = numpy.array([
            0.0,
            0.0,
            spreader_clear_height])
    elif mode == 2:  # Hoist down clear height
        move_vector_partial = numpy.array([
            0.0,
            0.0,
            - spreader_clear_height])
    elif mode == 3:  # Hoist up clear height + abs(node_pos[2])
        move_vector_partial = numpy.array([
            0.0,
            0.0,
            ((spreader_clear_height+abs(node_pos[2])-spreader_pos[2]))])
    elif mode == 4:  # Hoist down clear height + abs(node_pos[2])
        move_vector_partial = numpy.array([
            0.0,
            0.0,
            +(node_pos[2]-spreader_pos[2])])
    print('! END goToZ returning move_vector_partial:' +
          str(move_vector_partial))
    return move_vector_partial


def calcSpreaderMoveTime(move_vector):
    dist_x = 0.0
    dist_y = 0.0
    dist_z = 0.0
    time_x = 0.0
    time_y = 0.0
    time_z = 0.0
    angle_z = 0.0
    time_rot_z = 0.0
    print('$ BEGIN calcSpreaderMoveTime move_vector: ' +
          str(move_vector))
    print('Calculating movement times.')
    dist_x = math.fabs(move_vector[0])
    if dist_x < 2*fob_house_ramp_distance:
        # time_x = 2*numpy.sqrt(dist_x/fob_house_ramp_acceleration)
        time_x = ((
            dist_x-(2*fob_house_ramp_distance)
        )/fob_house_speed + 2*fob_house_ramp_seconds*0.01667)*3
    else:
        time_x = (
            dist_x-(2*fob_house_ramp_distance)
        )/fob_house_speed + 2*fob_house_ramp_seconds*0.01667
    dist_y = math.fabs(move_vector[1])
    if dist_y < 2*fob_traverse_ramp_distance:
        # time_y = 2*numpy.sqrt(dist_y/fob_traverse_ramp_acceleration)
        time_y = ((
            dist_y-(2*fob_traverse_ramp_distance)
        )/fob_traverse_speed + 2*fob_traverse_ramp_seconds*0.01667)*3
    else:
        time_y = (
            dist_y-(2*fob_traverse_ramp_distance)
        )/fob_traverse_speed + 2*fob_traverse_ramp_seconds*0.01667
    if time_x >= time_y:
        time = time_x
    else:
        time = time_y
    dist_z = math.fabs(move_vector[2])
    if dist_z < 2*fob_hoist_ramp_distance:
        # time_z = 2*numpy.sqrt(dist_z/fob_hoist_ramp_acceleration)
        time_z = ((
            dist_z-(2*fob_hoist_ramp_distance)
        )/fob_hoist_speed + 2*fob_hoist_ramp_seconds*0.01667)*3
    else:
        time_z = (
            dist_z-(2*fob_hoist_ramp_distance)
        )/fob_hoist_speed + 2*fob_hoist_ramp_seconds*0.01667
    time = time + time_z
    print('$ END calcSpreaderMoveTime time: ' + str(time))
    return time


def trajectoryScriptGenerator():
    # Handles the creation of a Blender script for
    #  time-trajectory visualization purposes
    print('trajectoryScriptGenerator')
    count = 0
    time_multiplier = 30.0
    script_file_name = ('PFYFOBPerfScript' + str(datetime.datetime.now()) +
                        '.py')
    outfile = open(script_file_name, 'w')
    outfile.write('import bpy\nstart_pos = (0,0,0)\nbpy.ops.mesh.\
primitive_cube_add(radius = 0.5, location = start_pos)\n\
ob = bpy.context.active_object\ntime_multiplier = ' +
                  str(time_multiplier) +
                  '\n' + 'bpy.context.scene.frame_set(0)\n')
    for p in a_reg_movement:
        if count < 400:
            outfile.write('bpy.context.scene.frame_set(' +
                          str(p[3]*time_multiplier) + ')\n')
            outfile.write('ob.location = (' + str(p[1][0]) + ', ' +
                          str(p[1][1]) + ', ' + str(p[1][2]) + ')\n')
            outfile.write(
                'ob.keyframe_insert(data_path="location", index=-1)\n')
            count = count + 1

    outfile.write('bpy.context.scene.frame_set(0)\n')
    outfile.close()


def createTrain(car_count):  # Calculation.
    global car_list
    car_list = []
    # train_track = numpy.random.randint(0, rail_tracks_count)
    # Create cars and put 2 containers in each.
    for i in range(car_count):
        carPosX = (car_length/2)+car_length*i
        carPosY = ((
            (rail_tracks_count - (train_track+1)) * rail_track_width) +
            0.5 * rail_track_width) + (((rail_tracks_count - (train_track)) *
                                        rail_track_service_lane_width))
        carPos = numpy.array([carPosX, carPosY, car_height])
        cnt_top = Container(
            uuid.uuid4(), False, (
                carPos + numpy.array(
                    [0.0, 0.0, 2.0*container_dimensions[2]])))
        cnt_bottom = Container(
            uuid.uuid4(), False, (carPos + numpy.array(
                [0.0, 0.0, container_dimensions[2]])))
        car = Car(uuid.uuid4(), i, cnt_bottom, cnt_top, 2, carPos)
        car_list.append(car)
    createPFindersPhysical()


def setup():  # Calculation
    # Yard setup.
    # Header.
    print('+++++++++++++++++++++++++++++++++++++++++++++++')
    print('+++++            PFYFOBPerf                ++++')
    print('+++++++++++++++++++++++++++++++++++++++++++++++')
    # Independent parameters entry
    global rail_tracks_count
    global rail_track_service_lane_width
    global rail_track_width
    global fob_count
    global fob_length
    global fob_house_speed
    global fob_house_ramp_distance
    global fob_house_ramp_acceleration
    global fob_house_ramp_seconds
    global fob_traverse_speed
    global fob_traverse_ramp_distance
    global fob_traverse_ramp_acceleration
    global fob_traverse_ramp_seconds
    global fob_hoist_speed
    global fob_hoist_ramp_distance
    global fob_hoist_ramp_acceleration
    global fob_hoist_ramp_seconds
    global fob_gantry_speed
    global fob_gantry_ramp_distance
    global fob_gantry_ramp_acceleration
    global fob_gantry_ramp_seconds
    global car_length
    global car_height
    global pfinder_width
    global pfinder_length
    global pfinder_height
    global pfinder_bottom_shoes_height
    global pfinder_top_shoes_height
    global pfinder_angle
    global train_track
    global fob_spreader_max_height
    global container_dimensions
    global config_parameter_set
    global fob_displacement_positive_x
    global fob_displacement_negative_x
    global a_movement_log
    global a_spreader_xyzt
    global profile_parameters
    global profile_parameters_line_keys
    global profile_parameters_line_values
    global cycle_mode
    global staging_mode
    global a_fob_hoist_moves
    global a_fob_house_moves
    global a_fob_traverse_moves
    global a_fob_gantry_moves
    global train_turn_time_fob
    global spreader_clear_height
    global a_reg_movement

    a_reg_movement = []
    spreader_clear_height = 2.0
    profile_parameters_line_keys = ''
    profile_parameters_line_values = ''
    profile_parameters = 'Profile Parameter,Value\n'
    for key in config[ini_profile_name]:
        profile_parameters += (
            key + ' , ' + config[ini_profile_name][key] + '\n')
        profile_parameters_line_keys += (key + ', ')
        profile_parameters_line_values += (
            config[ini_profile_name][key] + ', ')
    a_movement_log = []
    a_spreader_xyzt = []
    a_fob_hoist_moves = []
    a_fob_house_moves = []
    a_fob_traverse_moves = []
    a_fob_gantry_moves = []

    # Double or simple cycling
    cycle_modes_tmp = config[ini_profile_name]['cycle_modes']
    cycle_modes = cycle_modes_tmp[1:-1].split(",")
    cycle_mode = int(cycle_modes[numpy.random.randint(len(cycle_modes))])
    print('cycle_mode: ' + str(cycle_mode))

    # Double stacking or simple stacking for outbounds
    staging_modes_tmp = config[ini_profile_name]['staging_modes']
    staging_modes = staging_modes_tmp[1:-1].split(",")
    staging_mode = int(
        staging_modes[numpy.random.randint(len(staging_modes))])
    print('staging_mode: ' + str(staging_mode))

    # Enter number of cars per train
    train_car_count_min = int(
        config[ini_profile_name]['train_car_count_min'])
    train_car_count_max = int(
        config[ini_profile_name]['train_car_count_max'])
    train_car_count = numpy.random.random_integers(
        train_car_count_min, train_car_count_max)
    print('train_car_count: ' + str(train_car_count))

    # Enter number of rail tracks.
    rail_tracks_count = float(config[ini_profile_name]['rail_tracks_count'])

    # Enter rail track service lane width
    rail_track_service_lane_width_min = float(
        config[ini_profile_name]['rail_track_service_lane_width_min'])
    rail_track_service_lane_width_max = float(
        config[ini_profile_name]['rail_track_service_lane_width_max'])
    rail_track_service_lane_width = numpy.random.uniform(
        rail_track_service_lane_width_min, rail_track_service_lane_width_max)
    print(
        'rail_track_service_lane_width: ' + str(
            rail_track_service_lane_width))

    # Enter rail track width.
    rail_track_width = float(config[ini_profile_name]['rail_track_width'])

    # Enter number of FOBs.
    fob_counts_tmp = config[ini_profile_name]['fob_counts']
    fob_counts = fob_counts_tmp[1:-1].split(",")
    fob_count = int(fob_counts[numpy.random.randint(len(fob_counts))])
    print('fob_count: ' + str(fob_count))

    # Enter length of FOBs.
    fob_length_min = float(config[ini_profile_name]['fob_length_min'])
    fob_length_max = float(config[ini_profile_name]['fob_length_max'])
    fob_length = numpy.random.uniform(fob_length_min, fob_length_max)
    print('fob_length: ' + str(fob_length))

    # Enter FOB house speed (ft/min).
    fob_house_speed_min = float(
        config[ini_profile_name]['fob_house_speed_min'])
    fob_house_speed_max = float(
        config[ini_profile_name]['fob_house_speed_max'])
    fob_house_speed = numpy.random.uniform(
        fob_house_speed_min, fob_house_speed_max)
    print('fob_house_speed: ' + str(fob_house_speed))
    fob_house_ramp_seconds_min = float(
        config[ini_profile_name]['fob_house_ramp_seconds_min'])
    fob_house_ramp_seconds_max = float(
        config[ini_profile_name]['fob_house_ramp_seconds_max'])
    fob_house_ramp_seconds = numpy.random.uniform(
        fob_house_ramp_seconds_min, fob_house_ramp_seconds_max)
    print('fob_house_ramp_seconds: ' + str(fob_house_ramp_seconds))
    fob_house_ramp_acceleration = (
        fob_house_speed/60.0)/fob_house_ramp_seconds
    print(fob_house_ramp_acceleration)
    fob_house_ramp_distance = 0.5*numpy.square(
        fob_house_speed/60.0)/fob_house_ramp_acceleration
    print(fob_house_ramp_distance)

    # Enter FOB traverse speed.
    fob_traverse_speed_min = float(
        config[ini_profile_name]['fob_traverse_speed_min'])
    fob_traverse_speed_max = float(
        config[ini_profile_name]['fob_traverse_speed_max'])
    fob_traverse_speed = numpy.random.uniform(
        fob_traverse_speed_min, fob_traverse_speed_max)
    print('fob_traverse_speed: ' + str(fob_traverse_speed))
    fob_traverse_ramp_seconds_min = float(
        config[ini_profile_name]['fob_traverse_ramp_seconds_min'])
    fob_traverse_ramp_seconds_max = float(
        config[ini_profile_name]['fob_traverse_ramp_seconds_max'])
    fob_traverse_ramp_seconds = numpy.random.uniform(
        fob_traverse_ramp_seconds_min, fob_traverse_ramp_seconds_max)
    print('fob_traverse_ramp_seconds: ' + str(fob_traverse_ramp_seconds))
    fob_traverse_ramp_acceleration = (
        fob_traverse_speed/60.0)/fob_traverse_ramp_seconds
    print(fob_traverse_ramp_acceleration)
    fob_traverse_ramp_distance = 0.5*numpy.square(
        fob_traverse_speed/60.0)/fob_traverse_ramp_acceleration
    print(fob_traverse_ramp_distance)

    # Enter FOB hoist
    fob_hoist_speed_min = float(
        config[ini_profile_name]['fob_hoist_speed_min'])
    fob_hoist_speed_max = float(
        config[ini_profile_name]['fob_hoist_speed_max'])
    fob_hoist_speed = numpy.random.uniform(
        fob_hoist_speed_min, fob_hoist_speed_max)
    print('fob_hoist_speed: ' + str(fob_hoist_speed))
    fob_hoist_ramp_seconds_min = float(
        config[ini_profile_name]['fob_hoist_ramp_seconds_min'])
    fob_hoist_ramp_seconds_max = float(
        config[ini_profile_name]['fob_hoist_ramp_seconds_max'])
    fob_hoist_ramp_seconds = numpy.random.uniform(
        fob_hoist_ramp_seconds_min, fob_hoist_ramp_seconds_max)
    print('fob_hoist_ramp_seconds: ' + str(fob_hoist_ramp_seconds))
    fob_hoist_ramp_acceleration = (
        fob_hoist_speed/60.0)/fob_hoist_ramp_seconds
    print(fob_hoist_ramp_acceleration)
    fob_hoist_ramp_distance = 0.5*numpy.square(
        fob_hoist_speed/60.0)/fob_hoist_ramp_acceleration
    print(fob_hoist_ramp_distance)

    # Enter FOB gantry speed.
    fob_gantry_speed_min = float(
        config[ini_profile_name]['fob_gantry_speed_min'])
    fob_gantry_speed_max = float(
        config[ini_profile_name]['fob_gantry_speed_max'])
    fob_gantry_speed = numpy.random.uniform(
        fob_gantry_speed_min, fob_gantry_speed_max)
    print('fob_gantry_speed: ' + str(fob_gantry_speed))
    fob_gantry_ramp_seconds_min = float(
        config[ini_profile_name]['fob_gantry_ramp_seconds_min'])
    fob_gantry_ramp_seconds_max = float(
        config[ini_profile_name]['fob_gantry_ramp_seconds_max'])
    fob_gantry_ramp_seconds = numpy.random.uniform(
        fob_gantry_ramp_seconds_min, fob_gantry_ramp_seconds_max)
    print('fob_gantry_ramp_seconds: ' + str(fob_gantry_ramp_seconds))
    fob_gantry_ramp_acceleration = (
        fob_gantry_speed/60.0)/fob_gantry_ramp_seconds
    print(fob_gantry_ramp_acceleration)
    fob_gantry_ramp_distance = 0.5*numpy.square(
        fob_gantry_speed/60.0)/fob_gantry_ramp_acceleration
    print(fob_gantry_ramp_distance)

    # Enter car length.
    car_lengths_tmp = config[ini_profile_name]['car_lengths']
    car_lengths = car_lengths_tmp[1:-1].split(",")
    car_length = float(car_lengths[numpy.random.randint(len(car_lengths))])
    print('car_length: ' + str(car_length))

    # Enter car height (from top of rail to bottom of well).
    car_height = float(config[ini_profile_name]['car_height'])

    # Enter PFinder width.
    pfinder_width_min = float(config[ini_profile_name]['pfinder_width_min'])
    pfinder_width_max = float(config[ini_profile_name]['pfinder_width_max'])
    pfinder_width = numpy.random.uniform(pfinder_width_min, pfinder_width_max)
    print('pfinder_width: ' + str(pfinder_width))

    # Enter PFinder length
    pfinder_length = float(config[ini_profile_name]['pfinder_length'])
    print('pfinder_length: ' + str(pfinder_length))

    # Enter PFinder height (top container roof, not high-cube).
    pfinder_height = float(config[ini_profile_name]['pfinder_height'])

    # Enter PFinder bottom shoes height.
    pfinder_bottom_shoes_height = float(config[ini_profile_name]
                                        ['pfinder_bottom_shoes_height'])

    # Enter PFinder top shoes height.
    pfinder_top_shoes_height_min = float(
        config[ini_profile_name]['pfinder_top_shoes_height_min'])
    pfinder_top_shoes_height_max = float(
        config[ini_profile_name]['pfinder_top_shoes_height_max'])
    pfinder_top_shoes_height = numpy.random.uniform(
        pfinder_top_shoes_height_min, pfinder_top_shoes_height_max)
    print('pfinder_top_shoes_height: ' + str(pfinder_top_shoes_height))

    # Enter PFinder angle (degrees).
    pfinder_angle = float(config[ini_profile_name]['pfinder_angle'])

    # Enter train track.
    train_track = int(config[ini_profile_name]['train_track'])

    # Enter FOB spreader maximum height.
    fob_spreader_max_height = float(
        config[ini_profile_name]['fob_spreader_max_height'])

    # Enter container dimensions.
    container_dimensions = [
        float(config[ini_profile_name]['container_dimensions_x']),
        float(config[ini_profile_name]['container_dimensions_y']),
        float(config[ini_profile_name]['container_dimensions_z'])
    ]

    # Derivative parameters

    # How much the FOB moves when gantrying is needed
    if cycle_mode == 0:  # Overlapping gantry
        if (fob_length < 2*car_length):
            fob_displacement_positive_x = car_length
        else:
            fob_displacement_positive_x = fob_length - car_length
        fob_displacement_negative_x = car_length
    elif (cycle_mode == 1 or cycle_mode == 2):
        fob_displacement_positive_x = fob_length
        fob_displacement_negative_x = car_length

    # Rail track length
    rail_track_length = float(train_car_count) * car_length
    print('Rail tracks length: %.2f ft.' % rail_track_length)

    # Number of PFinders.
    global pfinders_count
    pfinders_count = int(rail_track_length/pfinder_width) + 1
    print('PFinders count: %d' % pfinders_count)

    # Number of cars per train.
    global car_count
    # car_count = int(rail_track_length/car_length)
    car_count = train_car_count
    print('Car count: %d' % car_count)

    # FOB width = rail tracks  count + aux lanes count
    global fob_width
    fob_width = (rail_tracks_count * rail_track_width) + (
        (rail_tracks_count + 1) * rail_track_service_lane_width)

    # Initialize simulation

    # Create train-> car_list, inbound container list
    createTrain(car_count)
    # Stage containers-> outbound container list
    # Create PFinder+Car pairings
    # Split yard by FOB count
    # Create per FOB double cycle lists


# End Defs & Classes
def main():
    global config
    config = configparser.ConfigParser()
    config.read(ini_file_name)
    print(config.sections())
    setup()
# Execute.
if __name__ == '__main__':
    main()
