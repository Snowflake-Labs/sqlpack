-- CREATE OR REPLACE PROCEDURE results.alert_suppressions_runner(queries_like STRING)
-- RETURNS VARIANT
-- LANGUAGE JAVASCRIPT
-- EXECUTE AS CALLER
-- USING TEMPLATE 'results-alert-suppressions-runner.js'
-- ;

CREATE OR REPLACE PROCEDURE results.alert_suppressions_runner()
RETURNS VARIANT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
USING TEMPLATE 'results-alert-suppressions-runner.js'
;

CREATE OR REPLACE TASK results.suppressions_merge 
  WAREHOUSE={snowalert_warehouse}
  AFTER results.alerts_merge
AS
CALL results.alert_suppressions_runner()
;
