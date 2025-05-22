from mdxalchemy.lark.mdx.export import export_query_statement_to_json
from mdxalchemy.lark.mdx import analyze

case = """SELECT {TM1SubsetToSet([Expense Measures].[Expense Measures],"Default","public")} ON 0, {TM1SubsetToSet([Cost Centre].[Cost Centre],"Default","public")} * {TM1SubsetToSet([Reporting Currency].[Reporting Currency],"Default","public")} ON 1 FROM [Expense]
"""

export_query_statement_to_json("./tmp/temp.json", analyze(case))
