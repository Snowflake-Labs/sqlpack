Introduction
---

SQLPacks is an open source project which has —

 - A CLI utility used for compiling templated SQL files with macros into SnowSQL  
 - A Python module that can be used to ship SQL components with your code
 - A repository of standard SQL templates for ETL operations with Snowflake 

Before You Contribute
---

Before you start contributing, you'll need a snowflake account which you can create [here](https://signup.snowflake.com). You'll need this account to verify the creation of the components of the SQL code like API Integrations, External Functions, Tasks, Streams, Views, Tables, etc, and also to check if the correct data is ingested from the third party app into the appropriate tables.

Install SnowSQL (optional)
---

SnowSQL is the command line client for connecting to Snowflake to execute SQL, including loading data into and unloading data out of database tables. Click [here](https://docs.snowflake.com/en/user-guide/snowsql-install-config.html) to learn how to install SnowSQL.

How To Contribute
---

You can contribute to this project -

- by creating new SQL modules (e.g. ETLs of the third-party appplication) in the `packs` directory
- by improving the runtime engine in the `sqlpack` directory, e.g. extending the `expand_macros` functionality
- by filing issues or enhancement requests

Create a new branch for all your contributions and send us a PR with a description of how you tested your change.

File Structure
---

Every ETL is put as a separate directory in the [packs](packs) directory and has 2 files in it

1. The templated SQL file with the ``.sql.fmt`` extension
2. The yaml file with the ``yaml`` extension

Structure of the Templated SQL file
---

The templated SQL file should have the extension `.sql.fmt`

The templated SQL file starts with a yaml header. The paramaters and variable map are extracted from this header and are used throughout the compiled SQL code.

The header is divided into 2 parts:

1. `params` - include the params required to make make the template work and the default values for those that are not required for the user to specify
#### SYNTAX
    -- params:
    -- - name: parameter_name
         default: default_value
    -- - name: parameter_name   

2. `varmap` - maps the variables to their extended values/names
#### SYNTAX
    -- varmap:
    --   table_name: 'table_{connection_name}'
    --   landing_log_table: '{table_name}_logs'

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

After this header, the templated SQL code follows.

### All the parameters and keys mentioned in the params and varmap sections of the the header will be referenced in the templated sql inside curly {} brackets 

Here is an example 

~~~
CREATE OR REPLACE TABLE {landing_log_table} ...

WAREHOUSE={snowflake_warehouse} ...
~~~

Structure of the data file
---
This yaml file has to have the same parameters as the parameters mentioned in the [templated SQL file header](#Structure-of-the-Templated-SQL-file).The structure of this yaml file is like a dictionary with the parameters as the key and the actual value of the parameters as the value

Here is an example:

~~~
connection_name: connection_name
snowflake_warehouse: warehouse_name
api_gateway_id: api_gateway_id_value
subdomain: subdomain_name
~~~

Developing
---

Once you are ready to contribute, run —

```zsh
git clone git@github.com:Snowflake-Labs/sqlpacks.git
cd sqlpacks
pipx install -e .
```

The [sqlpack](https://pypi.org/project/sqlpack) module will be installed on your machine 

Then, to compile the templated SQL file you can run the print-sql command by either

Passing the params via the terminal like so:

```zsh
sqlpack print-sql template.sql.fmt --parameter_1 val_1 --parameter_2 val_2
```

or passing the [yaml file](#Structure-of-the-yaml-file) containing the parameters like so:

```zsh
sqlpack print-sql template.sql.fmt parmameters.yaml
```

The above commands will print the results in the terminal. To pipe the results directly to [SnowSQL](#Install-SnowSQL), use your favorite shell's pipe, like so:

```zsh
sqlpack print-sql template.sql.fmt parmameters.yaml | snowsql
```
