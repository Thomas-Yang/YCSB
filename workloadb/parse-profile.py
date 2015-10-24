#!/usr/bin/python

import sys
import csv

import matplotlib.collections as mc
# import pylab as plt
import matplotlib.pyplot as plt

workload_file = open(sys.argv[1])

# (timline, latency)
read_latency = []

# (timeline, minor_gc_count, minor_gc_time, major_gc_count, major_time_count)
read_gc_latency = []

# (timeline, delay, minor_gc_count)
read_minor_gc = []

# (timeline, delay, major_gc_count)
read_major_gc = []

# (timline, latency)
update_latency = []

# (timeline, minor_gc_count, minor_gc_time, major_gc_count, major_time_count)
update_gc_latency = []

# (timeline, delay, minor_gc_count)
update_minor_gc = []

# (timeline, delay, major_gc_count)
update_major_gc = []


#######################################################
# read the workload log
#######################################################

for line in workload_file:
    if "[READ]," in line:
        if line.split(" ")[1].split(",")[0].split("_")[0].isdigit():
            timeline = int(line.split(" ")[1].split(",")[0].split("_")[0])
            latency = float(line.split(" ")[-1].strip()) / 1000
            minor_gc_count = int(line.split(" ")[1].split(",")[0].split("_")[1])
            minor_gc_time = float(line.split(" ")[1].split(",")[0].split("_")[2])
            major_gc_count = int(line.split(" ")[1].split(",")[0].split("_")[3])
            major_gc_time = float(line.split(" ")[1].split(",")[0].split("_")[4])
            if len(read_gc_latency) != 0:
                pre_minor_gc_count = read_gc_latency[-1][1]
                pre_minor_gc_time = read_gc_latency[-1][2]
                pre_major_gc_count = read_gc_latency[-1][3]
                pre_major_gc_time = read_gc_latency[-1][4]

                if minor_gc_count > pre_minor_gc_count:
                    read_minor_gc.append((timeline, (minor_gc_time - pre_minor_gc_time) * 1000, minor_gc_count))
                if major_gc_count > pre_major_gc_count:
                    read_major_gc.append((timeline, (major_gc_time - pre_major_gc_time) * 1000, major_gc_count))

            read_latency.append((timeline, latency))
            read_gc_latency.append((timeline, minor_gc_count, minor_gc_time, major_gc_count, major_gc_time))

    elif "[UPDATE]," in line:
        if line.split(" ")[1].split(",")[0].split("_")[0].isdigit():
            timeline = int(line.split(" ")[1].split(",")[0].split("_")[0])
            latency = float(line.split(" ")[-1].strip()) / 1000
            minor_gc_count = int(line.split(" ")[1].split(",")[0].split("_")[1])
            minor_gc_time = float(line.split(" ")[1].split(",")[0].split("_")[2])
            major_gc_count = int(line.split(" ")[1].split(",")[0].split("_")[3])
            major_gc_time = float(line.split(" ")[1].split(",")[0].split("_")[4])
            if len(update_gc_latency) != 0:
                pre_minor_gc_count = update_gc_latency[-1][1]
                pre_minor_gc_time = update_gc_latency[-1][2]
                pre_major_gc_count = update_gc_latency[-1][3]
                pre_major_gc_time = update_gc_latency[-1][4]

                if minor_gc_count > pre_minor_gc_count:
                    update_minor_gc.append((timeline, (minor_gc_time - pre_minor_gc_time) * 1000, minor_gc_count))
                if major_gc_count > pre_major_gc_count:
                    update_major_gc.append((timeline, (major_gc_time - pre_major_gc_time) * 1000, major_gc_count))

            update_latency.append((timeline, latency))
            update_gc_latency.append((timeline, minor_gc_count, minor_gc_time, major_gc_count, major_gc_time))

# print 'len of read: ' + str(len(read_latency))
# print 'len of read gc: ' + str(len(read_gc_latency))
print 'len of read minor gc: ' + str(len(read_minor_gc))
print 'len of read major gc: ' + str(len(read_major_gc))
# print read_minor_gc

# print read_latency
# print 'len of update: ' + str(len(update_latency))
# print 'len of update gc: ' + str(len(update_gc_latency))
print 'len of update minor gc: ' + str(len(update_minor_gc))
print 'len of update major gc: ' + str(len(update_major_gc))
# print update_minor_gc


minor_gc_latency = []
major_gc_latency = []

########################################################
# determine the earliest timeline for GC experienced
# by different type of query
########################################################
for read_record, update_record in zip(read_minor_gc, update_minor_gc):
    if read_record[0] < update_record[0]:
        minor_gc_latency.append((read_record[0], read_record[1]))
    else:
        minor_gc_latency.append((update_record[0], update_record[1]))

for read_record, update_record in zip(read_major_gc, update_major_gc):
    if read_record[0] < update_record[0]:
        major_gc_latency.append((read_record[0], read_record[1]))
    else:
        major_gc_latency.append((update_record[0], update_record[1]))

# print minor_gc_latency

###############################################
# draw the graph
###############################################

read_lines = []
for record in read_latency:
     start_point = record[0], 0
     end_point = record[0], record[1]
     read_lines.append([start_point, end_point])

update_lines = []
for record in update_latency:
     start_point = record[0], 0
     end_point = record[0], record[1]
     update_lines.append([start_point, end_point])

minor_gc_lines = []
for record in minor_gc_latency:
     start_point = record[0], 0
     end_point = record[0], record[1]
     minor_gc_lines.append([start_point, end_point])

fig = plt.figure()

ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

read_lc = mc.LineCollection(read_lines, colors='red', label='read qeury', linewidths=2)
update_lc = mc.LineCollection(update_lines, colors='blue', label='update query', linewidths=2)
minor_lc = mc.LineCollection(minor_gc_lines, colors='green', label='minor GC', linewidths=2)

ax1.add_collection(read_lc)
ax2.add_collection(update_lc)
ax3.add_collection(minor_lc)

ax1.autoscale()
ax1.margins(0.1)
ax1.set_xlim(left=0, right=8000)
ax1.set_ylim(bottom=0, top=250)
ax1.set_title(sys.argv[1].split(".")[0].split("-")[-1], fontsize='16')

ax2.autoscale()
ax2.margins(0.1)
ax2.set_xlim(left=0, right=8000)
ax2.set_ylim(bottom=0, top=250)

ax3.autoscale()
ax3.margins(0.1)
ax3.set_xlim(left=0, right=8000)
ax3.set_ylim(bottom=0, top=250)

ax3.set_xlabel('Elapsed Time (ms)', fontsize='16')
ax2.set_ylabel('Latency (ms)', fontsize='16')

# ax.set_xlim(left=0, right=3300)
# ax.set_ylim(bottom=0)

ax1.legend(loc='upper right')
ax2.legend(loc='upper right')
ax3.legend(loc='upper right')
plt.savefig('timing.pdf', bbox_inches='tight')
plt.show()

