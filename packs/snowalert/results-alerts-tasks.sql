-- 1. Runs the alert queries merge
CREATE OR REPLACE TASK results.alert_merge -- TODO: Alter rename task
  WAREHOUSE=snowalert_warehouse
  SCHEDULE='USING CRON * * * * * UTC'
AS
CALL results.alert_merge('30m')
;

-- 2. Runs the alerts supressions merge
CREATE OR REPLACE TASK results.suppresions_merge 
  WAREHOUSE=snowalert_warehouse
  AFTER results.alert_merge
AS
CALL results.alert_suppressions_runner()
;
