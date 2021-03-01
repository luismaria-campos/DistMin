#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=C0301, W0621, W0640, R0903, R0913

'''
Scheduling algorithm that minimizes the distance
Autor: Luis María Campos de la Morena
Email: LuisMaria.Campos@uclm.es
'''

import operator
import matplotlib.pyplot as plt

B_MAX= 2600         # 2500
B_MIN = 260         # 1975
B_INITIAL = 1170    # 2237.5
N_SLOTS = 24
N_TASKS = 10        # 5

# EXCEL JANUARY
#TASKS_ID = [0, 1, 2, 3, 4]
#TASKS_EC = [1, 25, 50, 75, 100]
#TASKS_QoS = [1, 50, 60, 70, 80]
#EP = [0,0,0,0,0,0,0.03191398989,53.04295834,89.56600597,106.078858,112.7283785,112.7283785,106.078858,89.56600597,53.04295834,0.03191398989,0,0,0,0,0,0,0,0]

# EXCEL JUNE
#TASKS_ID = [0, 1, 2, 3, 4]
#TASKS_EC = [1, 250, 500, 750, 1000]
#TASKS_QoS = [1, 70, 80, 90, 100]
#EP = [0,0,0,0,290.7913766,669.1017023,852.2712673,950.2838577,1006.010737,1036.997496,1050.972538,1050.972538,1036.997496,1006,950.2838577,852.2712673,669.1017023,290.7913766,0,0,0,0,0,0]

# ITA VALUES
TASKS_ID = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
TASKS_EC = [0, 22, 32.2, 43.4, 52.6, 62.8, 73, 83.2, 93.4, 103.6]
TASKS_QoS = [0, 7, 23, 31, 46, 58, 66, 81, 90, 100]
#EP = [0,0,0,0,0,75,256,436,520,520,520,520,520,520,520,520,520,436,256,75,0,0,0,0]  # JUNE
#EP = [0,0,0,0,0,0,0,38,118,186,239,272,283,272,239,186,118,38,0,0,0,0,0,0]           # OCTOBRE
#EP = [0,0,0,0,0,0,0,0,22,57,84,100,106,100,84,57,22,0,0,0,0,0,0,0]                  # DECEMBER

# JANUARY
#EP = [0,0,0,0,0,0,7.93,70.24,97.48,109.84,114.63,114.63,109.84,97.48,70.24,7.93,0,0,0,0,0,0,0,0]
# FEBRUARY
#EP = [0,0,0,0,0,0,35.61,86.85,107.98,117.67,122.18,122.18,117.67,107.98,86.85,35.61,0,0,0,0,0,0,0,0]
# MARCH
#EP = [0,0,0,0,0,0,73.16,105.18,120.26,127.6,131.03,131.03,127.6,120.26,105.18,73.16,0,0,0,0,0,0,0,0]
# APRIL
#EP = [0,0,0,0,0,58.58,99.7,119.82,130.52,136.01,138.65,138.65,136.01,130.52,119.82,99.7,58.58,0,0,0,0,0,0,0]
# MAY
#EP = [0,0,0,0,22.85,87.4,113.14,127.77,136.12,140.56,142.81,142.81,140.56,136.12,127.77,113.14,87.4,22.85,0,0,0,0,0,0]
# JUNE
#EP = [0,0,0,0,56.07,99.25,119.18,131.36,138.6,142.53,144.49,144.49,142.53,138.6,131.36,119.18,99.25,56.07,0,0,0,0,0,0]
# JULY
#EP = [0,0,0,0,59.96,100.72,119.95,131.81,138.91,142.81,144.63,144.63,142.81,138.91,131.81,119.95,100.72,59.96,0,0,0,0,0,0]
# AUGUST
#EP = [0,0,0,0,38.59,92.89,115.9,129.41,137.28,141.55,143.51,143.51,141.55,137.28,129.41,115.9,92.89,38.59,0,0,0,0,0,0]
# SEPTEMBER
#EP = [0,0,0,0,0,70.42,105.01,122.94,132.71,137.82,140.28,140.28,137.82,132.82,122.94,105.01,70.42,0,0,0,0,0,0,0]
# OCTOBER
#EP = [0,0,0,0,0,20.42,83.94,110.93,124.26,130.87,133.99,133.99,130.87,124.26,110.93,83.94,20.42,0,0,0,0,0,0,0]
# NOVEMBER
#EP = [0,0,0,0,0,0,46.56,91.98,111.35,120.38,124.5,124.5,120.38,111.35,91.98,46.56,0,0,0,0,0,0,0,0]
# DECEMBER
EP = [0,0,0,0,0,0,8.21,73.4,99.43,110.89,115.99,115.99,110.89,99.43,73.4,8.21,0,0,0,0,0,0,0,0]

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
    print("Slots: {:.2f} mA".format(N_SLOTS))
    print("Tasks: {:.2f} mA".format(N_TASKS))
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
