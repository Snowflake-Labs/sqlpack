CREATE OR REPLACE VIEW rules.AQ_SAOP_OPENVPN_LOGIN_FAIL_ALERT_QUERY COPY GRANTS
  COMMENT='Users failing to log into OpenVPN
  @id 5GFXV6ETQ4X
  @schedule USING CRON * * * * * UTC
  @lookback -10d
  '
AS
SELECT 'E' AS environment
     , ARRAY_CONSTRUCT('S') AS sources
     , 'Predicate' AS object
     , 'slack alert for failed VPN-MFA login' AS title
     , start_time AS event_time
     , CURRENT_TIMESTAMP AS alert_time
     , (
         'Potential VPN password compromise:'
         || 'MFA failure for user ' || username
         || ' at ' || alert_time
       ) AS description
     , username AS actor
     , 'Verb' AS action
     , 'SnowAlert' AS detector
     , OBJECT_CONSTRUCT(*) AS event_data
     , ARRAY_CONSTRUCT(
        OBJECT_CONSTRUCT(
          'type', 'slack',
          'channel', '#snowalert-sec-test',
          'message', description
        )
     ) AS handlers
     , 'low' AS severity
     , '5GFXV6ETQ4X' AS query_id
     , '-10d' AS lookback
     , 'USING CRON */5 * * * * UTC' AS schedule
FROM data.openvpn_dev_auth
WHERE error ILIKE '%Incorrect passcode. Please try again.%'
;

CREATE OR REPLACE VIEW rules.AS_OPENVPN_PAT_FILTER_ALERT_SUPPRESSION COPY GRANTS
  COMMENT='Suppress anything not on our team, as it should go through TD'
AS
SELECT id
FROM data.alerts
WHERE suppressed IS NULL
  AND query_id = '5GFXV6ETQ4X'
  AND actor NOT IN (
    'user-of-interest-1',
    'user-of-interest-2'
  )
;
