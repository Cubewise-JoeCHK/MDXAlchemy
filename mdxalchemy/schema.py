"""MDX Schema: Defines reserved keywords, symbols, and token types for TM1 MDX."""

from enum import Enum

class TokenType(Enum):
    # Keywords
    SELECT = "SELECT"
    FROM = "FROM"
    WHERE = "WHERE"
    AS = "AS"
    ON = "ON"
    AXIS = "AXIS"
    COLUMNS = "COLUMNS"
    ROWS = "ROWS"
    PAGES = "PAGES"
    CHAPTERS = "CHAPTERS"
    SECTIONS = "SECTIONS"
    NON = "NON"
    EMPTY = "EMPTY"
    HAVING = "HAVING"
    WITH = "WITH"
    SET = "SET" # Also a function/keyword for defining named sets
    MEMBER = "MEMBER" # Keyword for calculated members
    CALCULATED = "CALCULATED"
    DIMENSION = "DIMENSION"
    PROPERTIES = "PROPERTIES"

    # Functions (Common - this list will grow significantly)
    FILTER = "FILTER"
    ORDER = "ORDER"
    DESCENDANTS = "DESCENDANTS"
    CHILDREN = "CHILDREN"
    MEMBERS = "MEMBERS" # e.g. [Dimension].Members
    HIERARCHIZE = "HIERARCHIZE"
    DRILLDOWNLEVEL = "DRILLDOWNLEVEL"
    DRILLUPLEVEL = "DRILLUPLEVEL"
    CURRENTMEMBER = "CURRENTMEMBER"
    PARENT = "PARENT"
    ANCESTOR = "ANCESTOR"
    AGGREGATE = "AGGREGATE"
    COUNT = "COUNT"
    SUM = "SUM"
    AVG = "AVG"
    MAX = "MAX"
    MIN = "MIN"
    MEDIAN = "MEDIAN"
    IIF = "IIF"
    CASE = "CASE"
    WHEN = "WHEN"
    THEN = "THEN"
    ELSE = "ELSE"
    END = "END"
    USERNAME = "USERNAME"
    STRTOMEMBER = "STRTOMEMBER"
    STRTOSET = "STRTOSET"
    STRTOTUPLE = "STRTOTUPLE"
    GENERATE = "GENERATE"
    CROSSJOIN = "CROSSJOIN"
    NONEMPTYCROSSJOIN = "NONEMPTYCROSSJOIN"
    EXISTS = "EXISTS"
    HEAD = "HEAD"
    TAIL = "TAIL"
    SUBSET_FUNC = "SUBSET" # Function, distinct from SET keyword
    TOPCOUNT = "TOPCOUNT"
    BOTTOMCOUNT = "BOTTOMCOUNT"
    PERIODSTODATE = "PERIODSTODATE"
    LASTPERIODS = "LASTPERIODS"
    MEMBERS_FUNC = "MEMBERS" # e.g. Dimension.MEMBERS
    ALLMEMBERS = "ALLMEMBERS" # e.g. Dimension.ALLMEMBERS
    ITEM = "ITEM"

    # TM1 Specific Functions (Examples)
    TM1SUBSETALL = "TM1SUBSETALL"
    TM1SORT = "TM1SORT"
    TM1FILTERBYPATTERN = "TM1FILTERBYPATTERN"
    TM1FILTERBYLEVEL = "TM1FILTERBYLEVEL"
    TM1DRILLDOWNMEMBER = "TM1DRILLDOWNMEMBER"
    TM1CUBEVALUE = "TM1CUBEVALUE"
    TM1USER = "TM1USER"

    # Operators
    PLUS = "+"
    MINUS = "-"
    ASTERISK = "*" # Multiplication or AllMembers shorthand
    SOLIDUS = "/" # Division
    PERCENT = "%"
    AMPERSAND = "&"
    COLON = ":" # Range operator
    CARET = "^" # Power

    # Logical Operators
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    XOR = "XOR"
    IS = "IS"
    IN = "IN"

    # Comparison Operators
    EQ = "="
    NE = "<>"
    GT = ">"
    LT = "<"
    GE = ">="
    LE = "<="

    # Symbols / Punctuation
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    LBRACE = "{"
    RBRACE = "}"
    COMMA = ","
    DOT = "."
    SEMICOLON = ";" # Statement separator (rare in MDX but possible)

    # Literals
    STRING_LITERAL = "STRING_LITERAL"
    NUMBER_LITERAL = "NUMBER_LITERAL"
    BOOLEAN_LITERAL = "BOOLEAN_LITERAL" # TRUE, FALSE (often treated as keywords/identifiers)

    # Identifier
    IDENTIFIER = "IDENTIFIER"

    # Whitespace (typically ignored or used to separate tokens)
    WHITESPACE = "WHITESPACE"

    # End-of-File/Input
    EOF = "EOF"

    # For errors or unrecognized tokens
    MISMATCH = "MISMATCH"

# --- Collections of Keywords/Token Types for easier checking ---

KEYWORDS = {
    TokenType.SELECT, TokenType.FROM, TokenType.WHERE, TokenType.AS, TokenType.ON, TokenType.AXIS,
    TokenType.COLUMNS, TokenType.ROWS, TokenType.PAGES, TokenType.CHAPTERS, TokenType.SECTIONS,
    TokenType.NON, TokenType.EMPTY, TokenType.HAVING, TokenType.WITH, TokenType.SET, TokenType.MEMBER,
    TokenType.CALCULATED, TokenType.DIMENSION, TokenType.PROPERTIES, TokenType.CASE, TokenType.WHEN,
    TokenType.THEN, TokenType.ELSE, TokenType.END, TokenType.IS, TokenType.IN, TokenType.AND,
    TokenType.OR, TokenType.NOT, TokenType.XOR
}

FUNCTIONS = {
    TokenType.FILTER, TokenType.ORDER, TokenType.DESCENDANTS, TokenType.CHILDREN, TokenType.MEMBERS_FUNC,
    TokenType.HIERARCHIZE, TokenType.DRILLDOWNLEVEL, TokenType.DRILLUPLEVEL, TokenType.CURRENTMEMBER,
    TokenType.PARENT, TokenType.ANCESTOR, TokenType.AGGREGATE, TokenType.COUNT, TokenType.SUM, TokenType.AVG,
    TokenType.MAX, TokenType.MIN, TokenType.MEDIAN, TokenType.IIF, TokenType.USERNAME, TokenType.STRTOMEMBER,
    TokenType.STRTOSET, TokenType.STRTOTUPLE, TokenType.GENERATE, TokenType.CROSSJOIN, TokenType.NONEMPTYCROSSJOIN,
    TokenType.EXISTS, TokenType.HEAD, TokenType.TAIL, TokenType.SUBSET_FUNC, TokenType.TOPCOUNT, TokenType.BOTTOMCOUNT,
    TokenType.PERIODSTODATE, TokenType.LASTPERIODS, TokenType.ALLMEMBERS, TokenType.ITEM,
    # TM1 Specific
    TokenType.TM1SUBSETALL, TokenType.TM1SORT, TokenType.TM1FILTERBYPATTERN, TokenType.TM1FILTERBYLEVEL,
    TokenType.TM1DRILLDOWNMEMBER, TokenType.TM1CUBEVALUE, TokenType.TM1USER
}

OPERATORS = {
    TokenType.PLUS, TokenType.MINUS, TokenType.ASTERISK, TokenType.SOLIDUS, TokenType.PERCENT,
    TokenType.AMPERSAND, TokenType.COLON, TokenType.CARET, TokenType.EQ, TokenType.NE, TokenType.GT,
    TokenType.LT, TokenType.GE, TokenType.LE
}

# Note: Some tokens like AND, OR, NOT, IS, IN are both keywords and logical operators.
# They are included in KEYWORDS for general keyword recognition, but their specific role
# (e.g., as a logical operator in an expression) is determined by the parser based on context.

# You might also want a mapping from string value to TokenType for keywords
# to aid in the lexing process.
KEYWORD_MAP = {kw.value: kw for kw in KEYWORDS}
FUNCTION_MAP = {fn.value: fn for fn in FUNCTIONS}
# Add other maps if needed, e.g., for operators that are words like AND, OR, NOT

# Reserved characters that have special meaning or are part of multi-character operators
# This can help the lexer identify potential tokens more easily.
SPECIAL_CHARACTERS = {
    '(', ')', '[', ']', '{', '}', ',', '.', ';', 
    '+', '-', '*', '/', '%', '&', ':', '^', '=', '<', '>'
}

# Characters that TM1 reserves in object names (and thus are important for identifiers)
# From: https://www.ibm.com/docs/en/planning-analytics/2.0.0?topic=development-tm1-object-naming-conventions
# Note: Some of these are also in SPECIAL_CHARACTERS. This list is more about what *cannot* be in an unescaped identifier.
TM1_RESERVED_NAME_CHARS = {
    '\\', '/<', ':', '*', '?', '"', '<', '>', '|', '\'', ';', ','
    # Also, leading/trailing spaces, and names consisting only of spaces are problematic.
    # Control characters (ASCII 0-31) are also generally disallowed.
}

if __name__ == '__main__':
    # Example: Print all token types
    for token_type in TokenType:
        print(f"{token_type.name}: {token_type.value}")

    print("\nKeywords:")
    for kw in KEYWORDS:
        print(kw.value)

    print("\nFunctions (sample from map):")
    for i, (name, token_val) in enumerate(FUNCTION_MAP.items()):
        if i < 5:
            print(f"{name} -> {token_val}")
        else:
            break
