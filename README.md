<!-- README.md -->
# sqlpack

The sqlpack module provides —

1. A CLI utility used for compiling templated SQL files with macros into standard SQL.
2. A Python module that can be used to ship SQL components with your code.
3. A repository of standard SQL templates for ETL operations with Snowflake.


### If you want to contribute to the project, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

### For using the ETLs present in the project, follow the steps mentioned below

## Install
```zsh
pipx install sqlpack
```

## Using at the CLI

Use the `print-sample-data` command to see the required parameters for the templated SQL for a built in pack like so:
```zsh
sqlpack print-sample-data pack_name

# To store these parameters into a yaml file , run :
sqlpack print-sample-data pack_name > parameters.yaml

# Update the parameter values in the yaml file with the the editor of your choice. If you use VSCode , run :
code parameters.yaml
```

To compile a built-in template at the CLI, use the `print-sql` sub-command —

```zsh

sqlpack print-sql <pack_name> [parameters.yaml] [--params ...]

```

### Providing Parameter Values

Paramater values are read from —

1. default paramater values set by the template author
2. a param file provided at the CLI
3. values passed into the call.

If a parameter is missing from all three, the following error will be printed —

```
MISSING VALUE for <parameter_name>
```

### Example

#### Parameter File
```yaml
parameter_1: val_1
parameter_2: val_2
```

#### Template
```sql
simple_replace = {parameter_1}
simple_replace_with_additional_text = {parameter_2}_name
nested_replace = schema_{simple_replace}_end
```

#### Execute via Terminal
```zsh
sqlpack print-sql pack_name --parameter_1 val_1 --parameter_2 val_2
```
or
```zsh
sqlpack print-sql pack_name parameters.yaml

```

#### Output
```sql
simple_replace = val_1
simple_replace_with_additional_text = val_2_name
nested_replace = schema_val_1_name_end
```

## Using as a module

To accomplish the same thing as above in your Python script, you can —

```python
from sqlpack import print_sql

print_sql('pack_name', parameter_1='val1', parameter_2='val2')
```
or 
```python
print_sql('pack_name', 'parameters.yaml')
```
