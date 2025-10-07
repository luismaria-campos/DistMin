#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=C0301, W0621, W0640, R0903, R0913

'''
Scheduling algorithm that minimizes the distance
Autor: Luis María Campos de la Morena
Email: luismaria.Camposm@gmail.com
'''

import operator
import matplotlib.pyplot as plt

B_MAX= 2500
B_MIN = 1975
B_INITIAL = 2237.5
N_SLOTS = 24
N_TASKS = 10

TASKS_ID = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
TASKS_EC = [0, 22, 32.2, 43.4, 52.6, 62.8, 73, 83.2, 93.4, 103.6]
TASKS_QoS = [0, 7, 23, 31, 46, 58, 66, 81, 90, 100]
# JANUARY
# EP = [0,0,0,0,0,0,0,1.96590558,11.79543348,29.50262589,44.24691774,54.09048783,59.00525178,54.09048783,44.24691774,29.50262589,14.74429185,5.897716741,1.96590558,0,0,0,0,0,0]
# JUNE
EP = [0,0,0,0,0,0,3.510545679,10.53163704,28.08436543,52.65818519,77.23200494,94.78473334,105.3163704,95,77.23200494,52.65818519,28.08436543,14.04218272,7.021091358,3.510545679,0,0,0,0,0]
# OCTOBER
# EP = [0,0,0,0,0,0,0,3.538630045,21.23178027,53.10753504,79.64726037,97.36849496,106.2150701,97.36849496,79.64726037,53.10753504,26.53972533,10.61589013,3.538630045,0,0,0,0,0,0]

TASKS = []
SLOTS = []

def create_tasks():
    '''
    Function that creates the tasks
    '''
    for i in range(N_TASKS):
        task = Task(TASKS_ID[i], TASKS_EC[i], TASKS_QoS[i])
        TASKS.append(task)

def create_slots():
    '''
    Function that creates the slots
    '''
    for i in range(N_SLOTS):
        slot = Slot(i, EP[i],-1,-1,-1,-1,-1)
        SLOTS.append(slot)

def initial_assignment():
    '''
    Function that creates the initial assignment with the tasks with the highest quality per slot
    '''
    for i in range(N_SLOTS):
        if SLOTS[i].s_ep < min(TASKS_EC):
            SLOTS[i].s_ec = TASKS[0].t_ec
        else:
            aux = filter(lambda x: x <= SLOTS[i].s_ep, TASKS_EC)
            SLOTS[i].s_ec = max(aux)
        if i== 0:
            SLOTS[i].s_battery = B_INITIAL - SLOTS[i].s_ec + SLOTS[i].s_ep
        else:
            SLOTS[i].s_battery = SLOTS[i-1].s_battery - SLOTS[i].s_ec + SLOTS[i].s_ep
        if SLOTS[i].s_battery > B_MAX:
            SLOTS[i].s_battery = B_MAX
        SLOTS[i].s_assig = TASKS_EC.index(SLOTS[i].s_ec)
        SLOTS[i].s_dist = abs(B_INITIAL - SLOTS[i].s_battery)
        SLOTS[i].s_qos = TASKS_QoS[SLOTS[i].s_assig]

def upgrade():
    '''
    Function that increases the tasks/quality if there is excess energy according to the established limits
    '''
    count = 0
    while((SLOTS[N_SLOTS-1].s_battery-B_INITIAL)>0 and count < N_SLOTS-1):
        sorted_slots = sort_distances()
        if sorted_slots[count].s_assig == N_TASKS-1:
            count += 1
            if len(sorted_slots) <= count:
                count -= 1
        else:
            SLOTS[sorted_slots[count].s_id].s_assig += 1
            recalculate()
            if check_plan():
                count = 0
            else:
                SLOTS[sorted_slots[count].s_id].s_assig -= 1
                recalculate()
                count += 1

def check_plan():
    '''
    Function that checks if the schedule is valid
    '''
    valid = True
    for i in range(N_SLOTS):
        if SLOTS[i].s_battery < B_MIN:
            valid = False
        if SLOTS[N_SLOTS-1].s_battery < B_INITIAL:
            valid = False
    return valid

def recalculate():
    '''
    Function that updates data according to task assignment
    '''
    for i in range(N_SLOTS):
        SLOTS[i].s_ec = TASKS_EC[SLOTS[i].s_assig]
        if i == 0:
            SLOTS[i].s_battery = B_INITIAL - SLOTS[i].s_ec + SLOTS[i].s_ep
        else:
            SLOTS[i].s_battery = SLOTS[i-1].s_battery - SLOTS[i].s_ec + SLOTS[i].s_ep
        if SLOTS[i].s_battery > B_MAX:
            SLOTS[i].s_battery = B_MAX
        SLOTS[i].s_dist = abs(B_INITIAL - SLOTS[i].s_battery)
        SLOTS[i].s_qos = TASKS_QoS[SLOTS[i].s_assig]

def sort_distances():
    '''
    Function that sorts the slots according to their distance
    '''
    sorted_slots = sorted(SLOTS, reverse=True, key=operator.attrgetter('s_dist'))
    return sorted_slots

def print_results():
    '''
    Function that prints the results
    '''
    print("--------TASKS--------")
    for i in range(N_TASKS):
        print ("TASK: {} \tENERGY: {} \tQoS: {}".format(TASKS[i].t_id,TASKS[i].t_ec,TASKS[i].t_qos))
    print("\n--------SCHEDULE--------")
    for i in range(N_SLOTS):
        print ("SLOT: {} \tEP:{:.2f} \tEC:{:.2f} \tQoS:{:.2f} \tBATTERY:{:.2f}   \tDIST:{:.2f} \tASSIG:{}".format(SLOTS[i].s_id, SLOTS[i].s_ep, SLOTS[i].s_ec, SLOTS[i].s_qos, SLOTS[i].s_battery, SLOTS[i].s_dist, SLOTS[i].s_assig))
    print("\n--------RESULTS--------")
    sum_ep = 0
    sum_ec = 0
    sum_qos = 0
    sum_dist = 0
    schedule = []
    battery = []
    quality = []
    for i in range(N_SLOTS):
        sum_ep += SLOTS[i].s_ep
        sum_ec += SLOTS[i].s_ec
        sum_qos += SLOTS[i].s_qos
        sum_dist += SLOTS[i].s_dist
        schedule.append(SLOTS[i].s_assig)
        battery.append(SLOTS[i].s_battery)
        quality.append(SLOTS[i].s_qos)
    print("Bmax: {:.2f} mA".format(B_MAX))
    print("Bmin: {:.2f} mA".format(B_MIN))
    print("B(0): {:.2f} mA".format(B_INITIAL))
    print("Slots: {}".format(N_SLOTS))
    print("Tasks: {}".format(N_TASKS))
    print("EP sum: {:.2f} mA".format(sum_ep))
    print("EC sum: {:.2f} mA".format(sum_ec))
    print("QoS: {:.2f}%".format(sum_qos/N_SLOTS))
    print("B(k): {:.2f} mA".format(SLOTS[N_SLOTS-1].s_battery))
    print("B(k)-B(0): {:.2f} mA".format(SLOTS[N_SLOTS-1].s_battery-B_INITIAL))
    print("Distance: {:.2f}".format(sum_dist))
    print("Schedule: ", schedule)

def show_plot():
    '''
    Function that shows a plot with battery levels and QoS
    '''
    battery = []
    quality = []
    for i in range(N_SLOTS):
        battery.append(SLOTS[i].s_battery)
        quality.append(SLOTS[i].s_qos)
    plt.subplot(2, 1, 1)
    plt.title("BATTERY")
    plt.axhline(B_MAX, color="red", label="B_MAX")
    plt.axhline(B_MIN, color="red", label="B_MAX")
    plt.plot(battery)
    plt.ylabel("Battery (mA)")
    plt.xlabel("Hour")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.title("QoS")
    plt.plot(quality)
    plt.ylabel("QoS (%)")
    plt.yticks(range(0,101, 10))
    plt.xlabel("Hour")
    plt.show()

class Task:
    '''
    Task class
    '''
    def __init__(self, t_id, t_ec, t_qos):
        self.t_id = t_id
        self.t_ec = t_ec
        self.t_qos = t_qos

class Slot:
    '''
    Slot class
    '''
    def __init__(self, s_id, s_ep, s_ec, s_qos, s_battery, s_dist, s_assig):
        self.s_id = s_id
        self.s_ep = s_ep
        self.s_ec = s_ec
        self.s_qos = s_qos
        self.s_battery = s_battery
        self.s_dist = s_dist
        self.s_assig = s_assig

if __name__ == "__main__":
    create_tasks()
    create_slots()
    initial_assignment()
    upgrade()
    print_results()
    show_plot()
