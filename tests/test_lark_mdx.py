import pytest
from lark import Lark
import os
import logging
import sys
import json
from mdxalchemy.lark.mdx import analyze
import tempfile
from mdxalchemy.lark.mdx.export import export_query_statement_to_json

# Define paths at the module level
# Assumes the script is in the 'tests' directory and 'mdxalchemy' and 'case' are structured as shown.
BASE_DIR = os.path.dirname(__file__)
GRAMMAR_FILE = os.path.join(BASE_DIR, '../mdxalchemy/lark/mdx/grammar.lark')
TEST_CASE_DIR = os.path.join(BASE_DIR, 'case')
ASSERT_DIR = os.path.join(BASE_DIR, 'assert') # Define ASSERT_DIR at module level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)

def get_mdx_files():
    """Reads all .mdx files from the test case directory.

    Returns:
        list: A list of absolute paths to .mdx files.
              Returns an empty list if the directory doesn't exist or contains no .mdx files.
    """
    # Assertion: Check if TEST_CASE_DIR is a directory
    assert os.path.isdir(TEST_CASE_DIR), f"Test case directory not found: {TEST_CASE_DIR}"

    mdx_files = []
    for filename in os.listdir(TEST_CASE_DIR):
        if filename.endswith(".mdx"):
            mdx_files.append(os.path.join(TEST_CASE_DIR, filename))
    
    # Assertion: Check if any .mdx files were found (if the directory is expected to have them)
    # This can be adjusted if an empty directory is a valid scenario for some tests.
    logging.info(f"Scanning directory for .mdx files: {TEST_CASE_DIR}")
    logging.info(f"Found .mdx files: {mdx_files}")
    assert len(mdx_files) > 0, f"No .mdx files found in {TEST_CASE_DIR}"
    return mdx_files

def get_assert_json_path(mdx_file_path):
    """Constructs the path to the corresponding .json assert file."""
    # Assertion: Check if mdx_file_path is a string
    assert isinstance(mdx_file_path, str), "mdx_file_path must be a string."
    # Assertion: Check if ASSERT_DIR is a directory
    assert os.path.isdir(ASSERT_DIR), f"Assert directory not found: {ASSERT_DIR}"

    base = os.path.basename(mdx_file_path)
    json_path = os.path.join(ASSERT_DIR, base + ".json")
    
    # Assertion: Check if the constructed path is a string (basic sanity check)
    assert isinstance(json_path, str), "Constructed JSON path is not a string."
    return json_path

@pytest.fixture(scope="module")
def mdx_parser():
    """Fixture to provide a Lark parser instance.

    Returns:
        Lark: An instance of the Lark parser.
    
    Raises:
        AssertionError: If the grammar file is not found or is empty.
    """
    # Assertion: Check if GRAMMAR_FILE exists
    assert os.path.isfile(GRAMMAR_FILE), f"Grammar file not found: {GRAMMAR_FILE}"

    with open(GRAMMAR_FILE, "r") as f:
        grammar_content = f.read()
    
    # Assertion: Check if grammar content is not empty
    assert grammar_content, "Grammar file is empty."
    
    parser = Lark(grammar_content)
    
    # Assertion: Check if parser was created successfully
    assert parser is not None, "Lark parser could not be initialized."
    return parser

@pytest.mark.parametrize("mdx_file_path", get_mdx_files())
def test_parse_mdx_file(mdx_parser, mdx_file_path):
    """Tests parsing of a given MDX file.

    Args:
        mdx_parser (Lark): The Lark parser instance from the fixture.
        mdx_file_path (str): The path to the .mdx file to be tested.
    
    Raises:
        AssertionError: If parameters are invalid or file issues occur.
        pytest.fail: If parsing the MDX query fails.
    """
    logging.info(f"--- Starting test for MDX file: {os.path.basename(mdx_file_path)} ---")
    # Parameter validation assertions
    assert mdx_parser is not None, "mdx_parser parameter cannot be None."
    assert isinstance(mdx_file_path, str), "mdx_file_path parameter must be a string."
    
    # Assertion: Check if mdx_file_path points to an existing file
    assert os.path.isfile(mdx_file_path), f"MDX test file not found: {mdx_file_path}"
    logging.debug(f"Reading content from {mdx_file_path}")

    with open(mdx_file_path, "r") as f:
        mdx_query = f.read()

    assert mdx_query, f"MDX query is empty in file: {mdx_file_path}"
    logging.debug(f"Read {len(mdx_query)} characters from {mdx_file_path}.")

    try:
        logging.info(f"Attempting to parse MDX query from {os.path.basename(mdx_file_path)}")
        tree = mdx_parser.parse(mdx_query)
        # Assertion: Check if parsing returned a tree
        assert tree is not None, f"Parsing MDX query from {mdx_file_path} returned None instead of a tree."
        logging.info(f"Successfully parsed MDX query from {os.path.basename(mdx_file_path)}")
        logging.debug(f"Parsed tree for {os.path.basename(mdx_file_path)} is of type: {type(tree)}")
    except Exception as e:
        logging.error(f"Parsing MDX query from {os.path.basename(mdx_file_path)} failed.", exc_info=True)
        pytest.fail(f"Parsing MDX query from {mdx_file_path} failed with error: {e}")

@pytest.mark.parametrize("mdx_file_path", get_mdx_files())
def test_parse_and_compare_json(mdx_file_path):
    """
    Arrange: Read MDX and expected JSON.
    Act: Parse MDX and convert to JSON using analyze and export_query_statement_to_json.
    Assert: Compare output JSON with expected JSON.
    """

    assert isinstance(mdx_file_path, str)
    assert os.path.isfile(mdx_file_path)
    assert_dir_json = get_assert_json_path(mdx_file_path)
    assert os.path.isfile(assert_dir_json), f"Assert JSON file not found: {assert_dir_json}"

    with open(mdx_file_path, "r") as f:
        mdx_query = f.read()
    assert mdx_query, "MDX query is empty"

    with open(assert_dir_json, "r") as f:
        expected_json = json.load(f)
    assert isinstance(expected_json, dict)

    query_statement = analyze(mdx_query)
    assert query_statement is not None

    with tempfile.NamedTemporaryFile("w+", delete=False) as tmpfile:
        export_query_statement_to_json(tmpfile.name, query_statement)
        tmpfile.seek(0)
        actual_json = json.load(tmpfile)
    assert isinstance(actual_json, dict)
    assert actual_json == expected_json, f"Actual JSON does not match expected for {mdx_file_path}"

