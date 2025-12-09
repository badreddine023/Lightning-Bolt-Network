# Python Coding Standards for Lightning Bolt Network

This document outlines the required coding standards for all Python code contributed to the Lightning Bolt Network project. Adherence to these standards ensures code readability, maintainability, and consistency.

## 1. General Principles

*   **Readability:** Code should be easy to read and understand. Clarity is more important than conciseness.
*   **Consistency:** Be consistent with the style used throughout the project. If a standard is not defined here, follow the existing code style.
*   **Simplicity:** Prefer simple, straightforward solutions over overly complex or clever ones.

## 2. Style Guide (PEP 8)

All Python code **MUST** adhere to the official [PEP 8 Style Guide for Python Code](https://peps.python.org/pep-0008/). Key points include:

*   **Indentation:** Use 4 spaces per indentation level.
*   **Line Length:** Limit all lines to a maximum of 79 characters.
*   **Blank Lines:** Use two blank lines to separate top-level function and class definitions. Use one blank line to separate methods within a class.
*   **Imports:** Imports should be on separate lines and grouped in the following order:
    1.  Standard library imports.
    2.  Third-party related imports.
    3.  Local application/library specific imports.

## 3. Naming Conventions

| Type | Convention | Example |
| :--- | :--- | :--- |
| **Modules** | Short, all lowercase. Underscores can be used if it improves readability. | `ssi_resolver.py` |
| **Classes** | CapWords (CamelCase). | `DidResolver`, `VerifiableCredential` |
| **Functions/Methods** | all_lowercase_with_underscores (snake_case). | `resolve_did`, `verify_credential` |
| **Variables** | all_lowercase_with_underscores (snake_case). | `holder_did`, `did_document` |
| **Constants** | ALL_CAPS_WITH_UNDERSCORES. | `DID_REGISTRY_ADDRESS`, `PHI_CHAIN_NEXUS` |

## 4. Documentation and Typing

*   **Docstrings:** All modules, classes, and public functions/methods **MUST** have docstrings following the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
*   **Type Hinting:** Use [PEP 484 type hints](https://peps.python.org/pep-0484/) for all function arguments and return values. This improves static analysis and code clarity.

## 5. Error Handling

*   **Exceptions:** Use specific exceptions (e.g., `ValueError`, `IOError`) instead of catching the generic `Exception` class.
*   **Logging:** Use the standard `logging` module for all application output instead of `print()`. `print()` should only be used for debugging during development.
