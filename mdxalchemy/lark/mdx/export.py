from .schema import QueryStatement 
import json 

def export_query_statement_to_json(export_path: str, query_statement: QueryStatement) -> None:
    """Export a QueryStatement object to a JSON file.

    Args:
        path (str): The path where the JSON file will be saved.
        query_statement (QueryStatement): The QueryStatement object to export.

    Raises:
        AssertionError: If the path is not a string or if the QueryStatement is None.
    """
    assert isinstance(export_path, str), "Path must be a string"
    assert query_statement is not None, "QueryStatement cannot be None"
    with open(export_path, 'w') as f:
        json.dump(query_statement.to_json(), f, indent=4)
        
