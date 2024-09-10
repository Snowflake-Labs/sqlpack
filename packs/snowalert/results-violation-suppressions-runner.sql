CREATE OR REPLACE PROCEDURE results.violation_suppressions_runner()
RETURNS VARIANT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
USING TEMPLATE 'results-violation-suppressions-runner.js'
;
