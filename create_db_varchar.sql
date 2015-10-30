# sql script for generating YCSB database

##############################################
# tested with cassandra 2.0.15
##############################################
# use cassandra cql (cqlsh) 
##############################################
# create db
create keyspace ycsb WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor': 1 };
use ycsb;

# create table
create table usertable (y_id text primary key,field0 varchar,field1 varchar,field2 varchar,field3 varchar,field4 varchar,field5 varchar,field6 varchar,field7 varchar,field8 varchar,field9 varchar);

# empty table
truncat tablename

# delete keyspace or table
drop keyspace/table name

##############################################
# use cassandra-cli
##############################################

# create db
create keyspace ycsb WITH placement_strategy = 'org.apache.cassandra.locator.SimpleStrategy' and strategy_options = {replication_factor:1};

# create table
create column family usertable with column_type = 'Standard' and comparator = 'UTF8Type';

