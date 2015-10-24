#!/usr/bin/python

import matplotlib.pyplot as plt
import sys
import numpy as np

if len(sys.argv) < 2:
    print 'No latency log file is specified'
    sys.exit()

fig = plt.figure()
ax = fig.add_subplot(111)

colors = ['blue', 'green', 'red', 'cyan', 'yellow', 'black', 'orange', 'gray', 'pink', 'purple']
index = 0
symbols = ['o', '^', 's', '>', '<']

filename = sys.argv[1]
datafile = open(filename)
time_data = []
latency_data = []
for line in datafile:
    if ("[READ]," in line and line.split(" ")[1].split(",")[0].split("_")[0].isdigit()) or ("[UPDATE]," in line and line.split(" ")[1].split(",")[0].split("_")[0].isdigit()):
        # time scale (sec)
        # time_data.append(float(line.split(" ")[1].split(":")[0]))
        # latency scale (ms)
        latency_data.append(float(line.split(" ")[-1].strip()) / 1000)
    elif "[OVERALL], Throughput(ops/sec)," in line:
        print 'Throughput(ops/sec): ' + line.split(" ")[-1].strip()

sorted_data = np.sort(latency_data)
yvals = np.arange(len(sorted_data)) / float(len(sorted_data))

plt.plot(sorted_data, yvals, label='Cassandra' + '-' + filename.split(".")[0].split("-")[-1])

print '50th percentile latency: ' + str(sorted_data[len(yvals) / 2])
print '99th percentile latency: ' + str(sorted_data[int(len(yvals) * 0.99)])

# plt.scatter(time_data, latency_data, color=colors[index], marker=symbols[index])
# index += 1

ax.hlines(y=0.5, xmin=0, xmax=sorted_data[len(yvals) / 2], color='red', linestyles='dotted')
ax.vlines(x=sorted_data[len(yvals) / 2], ymin=0, ymax=0.5, color='red', linestyles='dotted')
ax.text(0, 0.5, '0.5')
ax.text(sorted_data[len(yvals) / 2], 0.5 / 2, str(sorted_data[len(yvals) / 2]))

# print int(len(yvals) * 0.99)
ax.hlines(y=0.99, xmin=0, xmax=sorted_data[int(len(yvals) * 0.99)], color='red', linestyles='dotted')
ax.vlines(x=sorted_data[int(len(yvals) * 0.99)], ymin=0, ymax=0.99, color='red', linestyles='dotted')
ax.text(0, 0.98, '0.99')
ax.text(sorted_data[int(len(yvals) * 0.99)], 0.99 / 2, str(sorted_data[int(len(yvals) * 0.99)]))

plt.ylabel('Cumulative Distribution')
plt.xlabel('End-to-End Latency (ms)')
plt.legend(bbox_to_anchor=(0., 1., 1., .102), loc=1, ncol=45000, mode="expand", borderaxespad=0.)
plt.savefig('latency-cdf.pdf', bbox_inches='tight')
plt.show()
