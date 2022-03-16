CREATE OR REPLACE FUNCTION results.array_set(xs VARIANT, i VARIANT, x VARIANT)
RETURNS VARIANT
LANGUAGE JAVASCRIPT
AS $$
  XS = XS || []
  XS[I] = X
  // map null and undefined value to proper JSON null
  return Array.from(XS).map(_ => _ == null ? null : _)
$$
;

CREATE OR REPLACE PROCEDURE results.alert_dispatcher()
RETURNS VARIANT
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
USING TEMPLATE 'results-alert-dispatcher.js'
;

CREATE OR REPLACE TASK results.alert_dispatcher
  WAREHOUSE=snowalert_warehouse
  SCHEDULE='USING CRON * * * * * UTC'
AS
CALL results.alert_dispatcher()
;
ALTER TASK alert_dispatcher RESUME;
