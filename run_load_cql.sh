#!/bin/bash

./bin/ycsb load cassandra-cql -P workloads/workloadb -P settings_load_cql.dat -s > load-cql.out 2>&1
