-- ---
-- params:
--   name: database
--   name: role
--   name: user
--   name: user_defaults
--   name: warehouse

CREATE WAREHOUSE IF NOT EXISTS {warehouse}
WAREHOUSE_SIZE=XSMALL
WAREHOUSE_TYPE=STANDARD
AUTO_SUSPEND=60
AUTO_RESUME=TRUE
INITIALLY_SUSPENDED=TRUE
;
CREATE DATABASE IF NOT EXISTS {database};
CREATE ROLE IF NOT EXISTS {role};
CREATE USER IF NOT EXISTS {user} {user_defaults};

GRANT ROLE {role} TO USER {user};
GRANT ALL PRIVILEGES ON DATABASE {database} TO ROLE {role};
GRANT ALL PRIVILEGES ON WAREHOUSE {warehouse} TO ROLE {role};

CREATE SCHEMA IF NOT EXISTS data;
CREATE SCHEMA IF NOT EXISTS rules;
CREATE SCHEMA IF NOT EXISTS results;

CREATE TABLE IF NOT EXISTS results.raw_alerts(
  run_id STRING,
  alert VARIANT,
  alert_time TIMESTAMP_LTZ(9),
  event_time TIMESTAMP_LTZ(9),
  ticket STRING,
  suppressed BOOLEAN,
  suppression_rule STRING DEFAULT NULL,
  counter INTEGER DEFAULT 1,
  correlation_id STRING,
  handled VARIANT
);

CREATE STREAM IF NOT EXISTS results.raw_alerts_stream
ON TABLE results.raw_alerts
;

CREATE TABLE IF NOT EXISTS results.alerts(
  alert_id STRING,
  alert VARIANT,
  alert_time TIMESTAMP_LTZ(9),
  event_time TIMESTAMP_LTZ(9),
  ticket STRING,
  suppressed BOOLEAN,
  suppression_rule STRING DEFAULT NULL,
  counter INTEGER DEFAULT 1,
  correlation_id STRING,
  handled VARIANT
);

CREATE TABLE IF NOT EXISTS results.violations(
  result VARIANT,
  id STRING,
  alert_time TIMESTAMP_LTZ(9),
  ticket STRING,
  suppressed BOOLEAN,
  suppression_rule STRING DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS results.query_metadata(
  event_time TIMESTAMP_LTZ,
  v VARIANT
);
CREATE TABLE IF NOT EXISTS results.run_metadata(
  event_time TIMESTAMP_LTZ,
  v VARIANT
);
CREATE TABLE IF NOT EXISTS results.ingestion_metadata(
  event_time TIMESTAMP_LTZ,
  v VARIANT
);

