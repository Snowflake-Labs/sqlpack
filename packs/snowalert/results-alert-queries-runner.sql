CREATE OR REPLACE PROCEDURE results.alert_queries_runner(query_name STRING, from_time_sql STRING, to_time_sql STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
USING TEMPLATE 'results-alert-queries-runner.js'
;

CREATE OR REPLACE PROCEDURE results.alert_queries_runner(query_name STRING, offset STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
USING TEMPLATE 'results-alert-queries-runner.js'
;

CREATE OR REPLACE PROCEDURE results.alert_queries_runner(query_name STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
USING TEMPLATE 'results-alert-queries-runner.js'
;
