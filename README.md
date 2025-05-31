# TM1Alchemy

TM1Alchemy is a Python-based TM1 MDX query compiler. It parses TM1-flavored MDX and emits Python code for execution against IBM Planning Analytics (TM1) via TM1py. The project is designed for developers and analysts who need to analyze, transform, or generate TM1 MDX queries programmatically.

## Features
- Parses TM1-specific MDX, including TM1 extensions and standard MDX clauses (SELECT, FROM, WHERE)
- Converts MDX queries into Python objects and JSON representations
- Integrates with TM1py for TM1 REST API compatibility
- Extensible grammar using Lark parser

## Project Structure

```
TM1Alchemy/
├── mdxalchemy/        # Core compiler and parser logic
│   └── lark/          # Lark grammar, parser, and AST schema
├── scripts/           # Example scripts and utilities
├── config/            # Configuration templates
├── tests/             # Test cases and assertions
├── README.md          # Project documentation
├── pyproject.toml     # Build and dependency configuration
└── ...
```

- `mdxalchemy/`: Main source code for parsing and compiling TM1 MDX.
- `scripts/`: Example scripts for using the compiler.
- `config/`: Example configuration files.
- `tests/`: Automated tests and test cases.

## Quickstart

1. **Install dependencies**
   ```bash
   pip install -e .[dev]
   ```
2. **Run a sample script**
   ```bash
   python scripts/build_mdx_test_case.py
   ```
3. **Run tests**
   ```bash
   pytest
   ```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License
MIT License. See [LICENSE](LICENSE).

---

# Project Plan (for reference)

Developing a TM1 MDX query compiler in Python requires a structured approach, covering requirements capture, grammar design, AST creation, semantic validation, code generation, and testing. The following project plan outlines phases, deliverables, and a high-level timeline to build a robust compiler that parses TM1-flavored MDX and emits Python code for execution against TM1.

## Phase 1: Requirements & Research
- Define MDX dialect scope  
  -  List standard MDX clauses (SELECT, FROM, WHERE) and functions to support.  
  -  Identify TM1-specific functions (e.g. TM1FILTERBYLEVEL, TM1FILTERBYPATTERN) and note forthcoming deprecation in Next Gen in favor of standard properties like ELEMENT_LEVEL[1].  
- Analyze existing libraries  
  -  MDXpy on PyPI for programmatic query building via Member, MdxTuple, MdxHierarchySet, MdxBuilder[2].  
  -  Cubewise MDXpy offering TM1-specific set operators and escaping logic[7].  
- Capture non-functional requirements  
  -  Performance targets for large queries.  
  -  Extensibility to new MDX functions.  
  -  Compatibility with TM1 REST API or TM1py calls.

## Phase 2: Architecture & Design
**Compiler Architecture**  
- Front end: Lexer & parser  
- Middle end: Abstract Syntax Tree (AST) & semantic analyzer  
- Back end: Code generator emitting Python modules  
- Module boundaries and interfaces  

**Tool Selection**  
- Use Lark for parsing and tokenization.  
- Define AST node classes in Python  

**Data Model**  
- Design AST nodes for MDX constructs: Query, Axis, Set, Tuple, FunctionCall  
- Plan symbol table for hierarchy and member resolution  

## Phase 3: Implementation
**3.1 Lexical & Syntax Analysis**  
- Write MDX grammar for Lark, covering SELECT, FROM, WHERE, standard functions, TM1 extensions  
- Implement tokenizer using Lark to emit tokens: identifiers, literals, brackets, commas  
- Build parser rules in Lark to construct AST  

**3.2 AST & Semantic Analysis**  
- Develop AST node classes with validation methods  
- Implement semantic checks:  
  -  Validate function arguments and arity  
  -  Ensure hierarchies and members exist in TM1 (optionally using a mock metadata store)  
- Support rewriting deprecated functions to standard MDX (e.g. translate TM1FILTERBYLEVEL to use ELEMENT_LEVEL filtering)[1]  

**3.3 Code Generation**  
- Create a back end that walks the AST and emits Python code strings  
- Integrate with MDXpy to build queries programmatically, e.g.:  
  ```python
  from mdxpy import MdxBuilder, Member
  query = (
    MdxBuilder.from_cube("Sales")
      .add_hierarchy_set_to_axis(0, Member.of("Measures","SalesAmount"))
      .add_hierarchy_set_to_axis(1, MdxHierarchySet.all_leaves("Product"))
      .to_mdx()
  )
  ```
- Or generate direct calls to TM1 REST API using HTTP client  
- Ensure escaping of special characters and proper quoting  

## Phase 4: Testing & Validation
- Unit tests for lexer, parser, AST transformations  
- Semantic tests using sample TM1 metadata (mock hierarchies)  
- Integration tests: run compiled Python code against a TM1 instance, compare results to direct MDX execution in Architect  
- Performance benchmarking with large hierarchies and deep levels  

## Phase 5: Documentation & Deployment
- Write developer guide covering architecture, extension points, and adding new MDX functions  
- Provide user guide on invoking the compiler and integrating generated code into TM1 processes or TM1py scripts  
- Set up CI/CD pipeline for linting (flake8), testing (pytest), and packaging (wheel upload to PyPI)  

## Timeline & Milestones
- Month 1: Requirements gathering, research on TM1 MDX dialect and existing libraries[6]  
- Month 2: Grammar specification, prototype lexer/parser  
- Month 3: AST design, semantic analyzer  
- Month 4: Code generator and MDXpy integration  
- Month 5: Testing suite development, sample TM1 integration  
- Month 6: Documentation, CI/CD setup, release of v1.0  

This phased plan ensures incremental delivery of a Python-based TM1 MDX compiler, starting from core parsing capabilities through to end-to-end execution and deployment.
