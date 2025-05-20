TEST_CASE = """
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

