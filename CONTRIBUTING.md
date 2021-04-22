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

Functionality of the compiler engine

---
The sqlpack engine uses two stages:

1. *The template-substitution stage*, which replaces variables provided by the user,
1. *The macro expansion stage*, which adds useful shorthands to the SQL and not currently present in SnowSQL.

Files Used
---

Every ETL is put as a separate directory in the [packs](packs) directory and has 2 files in it

1. The templated SQL file with the ``.sql.fmt`` extension
1. The yaml file with the ``yaml`` extension
1. An optional .js file for packs that use inline JS code

Structure of the Templated SQL file
---

The templated SQL file should have the extension `.sql.fmt`

The templated SQL file starts with a yaml header. The paramaters and variable map are extracted from this header and are used throughout the compiled SQL code.

The header is divided into 2 parts:

1. `params` - include the params required to make the template work and the default values for those that are not required for the user to specify. For example:

    ```python
    -- params:
    -- - name: parameter_name
            default: default_value
    -- - name: parameter_name
    ```

2. `varmap` - maps the variables to their extended values/names. For example:

    ```python
    -- varmap:
    --   table_name: 'table_{connection_name}'
    --   landing_log_table: '{table_name}_logs'
    ```

Here is an example of what the yaml header looks like:

```python
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

NOTE: This is an SQL comment as it appears in an SQL file but isn't executed and is only used to allude to the variables in the templated SQL file.

After this header, the templated SQL code follows.

All the parameters and keys mentioned in the params and varmap sections of the the header can be referenced in the templated sql inside curly brackets, e.g.

Here is an example:

```sql
SET url='https://{domain}/api/v2/users'

CREATE OR REPLACE TABLE {landing_log_table} ...

WAREHOUSE={snowflake_warehouse} ...
```

Structure of the data file
---

This yaml file has to have the same parameters as the parameters mentioned in the [templated SQL file header](#Structure-of-the-Templated-SQL-file). The structure of this yaml file is like a dictionary with the parameters as the key and the actual value of the parameters as the value, or a list of such dictionaries to apply one after the other.

Here is an example:

```yaml
connection_name: connection_name
snowflake_warehouse: warehouse_name
api_gateway_id: api_gateway_id_value
subdomain: subdomain_name
```

Developing
---

Once you are ready to contribute, run the following shell commands:

```bash
git clone git@github.com:Snowflake-Labs/sqlpacks.git
cd sqlpacks
pipx install -e .
```

The [sqlpack](https://pypi.org/project/sqlpack) module will be installed on your machine in an "editable" mode.

Then, to compile the templated SQL file you can run the print-sql command by either:

(1) passing the pack name (folder in which the templated sql file and data file are stored), the data file is by default included like so:

```bash
sqlpack print-sql pack_name
```

or (2) passing the application name followed by the params via the terminal if you want to overwrite the parameter values ingested from the data file like so:

```bash
sqlpack print-sql pack_name --parameter_1 val_1 --parameter_2 val_2
```

The above commands will print the results in the terminal. To pipe the results directly to [SnowSQL](#Install-SnowSQL), use your favorite shell's pipe, like so:

```bash
sqlpack print-sql pack_name | snowsql
```
