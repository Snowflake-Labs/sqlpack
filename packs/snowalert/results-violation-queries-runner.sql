CREATE OR REPLACE PROCEDURE results.violation_queries_runner()
RETURNS VARIANT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
USING TEMPLATE 'results-violation-queries-runner.js'
;
