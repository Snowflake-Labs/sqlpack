CREATE OR REPLACE TASK results.violation_scheduler
  WAREHOUSE=SNOWALERT_WAREHOUSE
  SCHEDULE='USING CRON 0 */3 * * * UTC'
AS
CALL results.violation_scheduler('SNOWALERT_WAREHOUSE')
;
