CREATE OR REPLACE PROCEDURE results.alert_scheduler(warehouse STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
USING TEMPLATE 'results-alert-scheduler.js'
;

CREATE OR REPLACE TASK results.schedule_alerts
WAREHOUSE=snowalert_warehouse
SCHEDULE='USING CRON 1/15 * * * * UTC'
AS CALL results.alert_scheduler('snowalert_warehouse')
;
