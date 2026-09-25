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
  Supports single-line (`//`) and multi-line (`/* */`, `(* *)` and nestable `{}`) comments.

- **Custom Types**:
  Highlights CKSP's `int`, `real`, `string`, `bool`, `void`, and user-defined types, including generic types like `List<T>`, type annotations and `as` casts.

- **Macros, Structs and Namespaces**:
  Syntax support for macros, structs, namespaces, const blocks, imports with `as` aliases and `#pragma` directives.

- **Operators**:
  String concatenation (`&`), optional chaining (`?.`), nullish coalescing (`??`), the ternary operator and bitwise operators like `.and.`.

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

Since the amount of builtin-in functions and constants directly accessing **Kontakt's** engine features might change, they are loaded dynamically from text files located in the `cksp_builtins/` directory. Each file contains one entry per line, optionally with comments (`//`).

### Updating the Built-ins

The files are copies of the ones in `cksp-compiler/Builtins`, so updating them is a copy:

```bash
for f in engine_functions engine_variables engine_constants engine_fx_enums engine_widgets; do
    cp ../cksp-compiler/Builtins/$f.txt pygments_lexers/cksp_builtins/
done
```

<!-- ## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. -->