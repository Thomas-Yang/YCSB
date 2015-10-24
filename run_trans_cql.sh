#!/bin/bash

# workloadb: read heavily
#numactl --physcpubind=16-31 --membind=1 ./bin/ycsb run cassandra-cql -P workloads/workloadb -P settings_trans.dat -s > trans.out 2>&1

# workloada: read/update even
# ./bin/ycsb run cassandra-cql -P workloads/workloada -P settings_trans.dat -s > trans.out 2>&1

# workloadg: update heavily

# cassandra_vmid=`jps | grep CassandraDaemon | cut -d ' ' -f 1`

# numactl --physcpubind=8-15 --membind=1 ./bin/ycsb run cassandra-cql -P workloads/workloadb -P settings_trans_cql.dat -p jvm.identity=$cassandra_vmid -s > trans-cql.out 2>&1

# workloads=(workloada workloadb workloadc workloadd workloade workloadf)
workloads=(workloadc workloadd workloade workloadf)

cassandra_vmid=`jps | grep CassandraDaemon | cut -d ' ' -f 1`

for workload in "${workloads[@]}"
do
    echo "running ${workload} ..."
    numactl --physcpubind=8-15 --membind=1 ./bin/ycsb run cassandra-cql -P workloads/${workload} -P settings_trans_cql.dat -p jvm.identity=$cassandra_vmid -s > trans-cql-${workload}.out 2>&1
    echo "finish ${workload} and sleep 5 seconds ..."
    sleep 5
done
