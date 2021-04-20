# Introduction
Sqlpacks is an open source project which has 
 - A CLI utility used for compiling templated SQL files with macros into standard SQL  
 - A Python module that can be used to ship SQL components with your code
 - A repository of standard SQL templates for ETL operations with Snowflake 

# Before You Contribute
Before you start contributing , you'll need a snowflake account which you can create [here](https://signup.snowflake.com) . You'll need this account to verify the creation of the components of the sql code like api integrations , external functions , tasks , streams , views , tables etc and also to check if the correct data is ingested from the third party app
into the appropriate tables

## Install SnowSQL (Recommended)
SnowSQL is the next-generation command line client for connecting to Snowflake to execute SQL queries and perform all DDL and DML operations, including loading data into and unloading data out of database tables.
Click [here](https://docs.snowflake.com/en/user-guide/snowsql-install-config.html) to install SnowSQL



## How To Contribute
You can contribute to this project 
1. By creating new ETLs' of the third-party appplication from where you would like to ingest data into snowflake by writing templated SQL files.
2. By suggesting enhancements to the existing ETLs'  

## File Structure
Every ETL is put as a separate directory in the [packs](packs) directory and has 2 files in it
1. The templated SQL file with the ``.sql.fmt`` extension
2. The yaml file with the ``yaml`` extension

## Structure of templated SQL files
The templated sql file should have the extension `.sql.fmt`

The `.sql.fmt` file starts with a yaml header . The paramaters and variable map are extracted from this header and are used throughout the compiled SQL code . 
The header is divided into 2 parts 
1. `params` - includes the required parameters with the default values for some of them 
    ### SYNTAX
    ```
    -- params:
    -- - name: parameter_name
            default: default_value (optional) 
    -- - name: parameter_name 
    ```

2. `varmap` - maps the variables to their extended values/names
    ### SYNTAX
    ```
    -- varmap:
    --   table_name: 'table_{connection_name}'
    --   landing_log_table: '{table_name}_logs'
    ```

Here is an example of what the yaml header looks like
```
-- ---
-- params:
-- - name: connection_name
--   default: 'default_connection'
-- - name: api_gateway_id
-- - name: subdomain
-- - name: snowflake_warehouse
-- varmap:
--   table_name: 'table_{connection_name}'
--   landing_log_table: '{table_name}_logs'
--   landing_user_table: '{table_name}_users'
--   landing_group_table: '{table_name}_groups'
--   domain: '{subdomain}.xyz.com'
```

### All the parameters and keys mentioned in the params and varmap sections of the the header will be referenced in the templated sql inside curly {} brackets 

Here is an example 
```
CREATE OR REPLACE TABLE {landing_log_table}

WAREHOUSE={snowflake_warehouse}
```

## Structure of the yaml file
This yaml file has to have the same parameters as the parameters mentioned in the `sql.fmt` file header . The structure of this yaml file is like a dictionary with the parameters as the key and the actual value of the parameters as the value

Here is an example
```
connection_name: connection_name
snowflake_warehouse: warehouse_name
api_gateway_id: api_gateway_id_value
subdomain: subdomain_name
```

Once you have the above mentioned files and installations ready , you can refer to the [README.md](README.md) on how to compile and produce the SQL code
