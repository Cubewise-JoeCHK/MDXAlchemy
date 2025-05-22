from mdxalchemy.lark.mdx.export import export_query_statement_to_json
from mdxalchemy.lark.mdx import analyze

case = """
SELECT
  NON EMPTY
   {[M Bus ETA].[M Bus ETA].Members}
  ON COLUMNS ,
  NON EMPTY
   {[KMB Stop].[KMB Stop].Members}
  ON ROWS
FROM [Bus ETA]
WHERE
  (
   [Bus Route].[Bus Route].[74D],
   [Bus Bound].[Bus Bound].[I],
   [Bus Service].[Bus Service].[All Service]
  )
"""

export_query_statement_to_json("./tmp/temp.json", analyze(case))
