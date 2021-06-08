CREATE OR REPLACE PROCEDURE results.alert_merge(deduplication_offset STRING)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
USING TEMPLATE 'results-alert-merge.js'
;

CREATE OR REPLACE TASK results.alert_merge
  WAREHOUSE=snowalert_warehouse
  SCHEDULE='USING CRON * * * * * UTC'
AS
CALL results.alert_merge('30m')
;
