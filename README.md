# CKSP Pygments Lexer

A **Pygments Lexer** for the **CKSP scripting language**, designed to provide syntax highlighting for `.cksp`, `.ksp`, and `.txt` files. This lexer supports CKSP's custom syntax, including keywords, built-in functions, macros, types, and comments.

`CKSP` is a higher-level dialect for the vanilla version of the Kontakt scripting language (`KSP`) used by the **Kontakt** sampler from **Native Instruments**. It is used to create custom scripts for **Kontakt** instruments, allowing users to create complex instruments with custom behaviors.

---

## Features

- **Keywords and Control Structures**:
  Highlighting for CKSP keywords like `declare`, `function`, `if`, `while`, `for`, etc.

- **Built-in Functions and Constants**:
  Dynamically loads CKSP built-in functions from files for highlighting.

- **Comments**:
  Supports single-line (`//`) and multi-line (`/* */` and `{}`) comments.

- **Custom Types**:
  Highlights CKSP's `int`, `real`, `string`, `bool`, `void`, and user-defined types.

- **Macros and Structs**:
  Syntax support for macros and struct definitions.

- **Function Calls**:
  Highlights functions with or without the `call` keyword.

---

## Installation

### Using `pip`

You can install the lexer directly via `pip` after cloning this repository:

```bash
pip install .
```

---

## Usage

### Using `pygmentize`

You can test the lexer using `pygmentize` to highlight CKSP code:

```bash
pygmentize -l cksp -f terminal -O style=monokai test.cksp
```

Replace the code inside `test.cksp` with your custom code in CKSP Syntax.

---

## How to Add Built-in Functions and Constants

### File Structure

Since the amount of builtin-in functions and constants directly accessing **Kontakt's** engine features might change, they are loaded dynamically from text files located in the `cksp_builtins/` directory. Each file contains one function per line, optionally with comments (`//`).

### Adding new Built-ins

Modify the `cksp_builtins/engine_functions.txt` file by adding new functions. Each function should be on a new line, with an optional comment after `//`.
New NI constants or variables can be added to the `cksp_builtins/engine_constants.txt` file in the same way.

<!-- ## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. -->