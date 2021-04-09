// args

var HANDLER_TYPE;

// library

function exec(sqlText, binds=[]) {
  let retval = []
  const stmnt = snowflake.createStatement({sqlText, binds})
  const result = stmnt.execute()
  const columnCount = stmnt.getColumnCount();
  const columnNames = []
  for (let i = 1 ; i < columnCount + 1 ; i++) {
    columnNames.push(stmnt.getColumnName(i))
  }

  while(result.next()) {
    let o = {};
    for (let c of columnNames) {
      o[c] = result.getColumnValue(c)
    }
    retval.push(o)
  }
  return retval
}

// business logic

HANDLE = `
MERGE INTO results.alerts d
USING (
  SELECT
    id,
    ARRAY_AGG(
      ${HANDLER_TYPE}_handler(handler_args)
    ) handled
  FROM (

    SELECT
      id,
      value handler_args
    FROM (
      SELECT
        id,
        IFF(
          IS_OBJECT(handlers),
          ARRAY_CONSTRUCT(handlers),
          handlers
        ) handlers_array
      FROM alerts
      WHERE handled IS NULL
   ), LATERAL FLATTEN(input => handlers_array)
   WHERE handler_args['type'] = '${HANDLER_TYPE}'

  )
  GROUP BY id
) s
ON d.alert['ALERT_ID'] = s.id
WHEN MATCHED
THEN UPDATE
  SET d.handled = s.handled
`

return {
  'handled': exec(HANDLE)
}
