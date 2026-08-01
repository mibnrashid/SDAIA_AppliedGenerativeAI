#!/usr/bin/env python3
"""
verify.py — checks every notebook before it goes near a projector.

Run:  python notebooks/verify.py

Eight checks:
  1. valid JSON and nbformat 4
  2. every code cell parses with ast.parse()
  3. every third-party import appears in cell 1's pip install
  4. every function called is defined earlier, imported, or a builtin
  5. no hardcoded API key; the userdata.get('GEMINI_API_KEY') pattern is used
  6. gemini-2.5-flash-lite and gemini-embedding-001 are the only model strings
  7. a reflection cell and an "If this breaks" cell are both present
  8. every "# TODO" cell has surrounding structure, not an empty cell

Exit code is 0 only if nothing failed.
"""

import ast
import builtins
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

ALLOWED_MODELS = {"gemini-2.5-flash-lite", "gemini-embedding-001"}

# Modules that ship with Python or with Colab's base image, so they do not
# need to appear in a pip install line.
STDLIB_OK = {
    "os", "json", "time", "re", "io", "sys", "math", "random", "pathlib",
    "hashlib", "functools", "itertools", "collections", "datetime",
    "textwrap", "typing", "dataclasses", "string", "base64", "csv",
    "google",             # google.colab / google.genai, installed via google-genai
    "IPython", "matplotlib", "numpy", "pandas",   # preinstalled in Colab
}

# import name -> pip package name, where they differ
IMPORT_TO_PIP = {
    "genai": "google-genai",
    "google": "google-genai",
    "chromadb": "chromadb",
    "rank_bm25": "rank-bm25",
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "PIL": "pillow",
}

findings = []


def finding(nb, cell, kind, message):
    findings.append((nb, cell, kind, message))


def source(cell):
    return "".join(cell["source"])


def strip_magics(text):
    """Colab shell/magic lines are not Python. Blank them for parsing."""
    out = []
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("!") or s.startswith("%"):
            # Keep the indentation: a magic inside an if-block is legal in
            # IPython, and blanking it at column 0 invents a syntax error.
            indent = line[:len(line) - len(line.lstrip())]
            out.append(indent + "pass  # shell/magic line")
        else:
            out.append(line)
    return "\n".join(out)


def check_notebook(path):
    name = os.path.basename(path)

    # --- 1 · valid JSON, nbformat 4 -------------------------------
    try:
        with io.open(path, encoding="utf-8") as fh:
            nb = json.load(fh)
    except Exception as e:
        finding(name, "-", "json", "does not parse: %s" % e)
        return
    if nb.get("nbformat") != 4:
        finding(name, "-", "nbformat", "nbformat is %r, expected 4" % nb.get("nbformat"))

    cells = nb["cells"]
    code_cells = [(i + 1, c) for i, c in enumerate(cells) if c["cell_type"] == "code"]
    all_text = "\n".join(source(c) for c in cells)

    # --- 2 · every code cell parses -------------------------------
    trees = {}
    for n, cell in code_cells:
        text = strip_magics(source(cell))
        try:
            trees[n] = ast.parse(text)
        except SyntaxError as e:
            finding(name, n, "syntax", "%s (line %s)" % (e.msg, e.lineno))

    # --- 3 · imports vs the cell-1 pip install --------------------
    first = source(code_cells[0][1]) if code_cells else ""
    pip_line = " ".join(re.findall(r"pip install[^\n]*", first))
    for n, tree in trees.items():
        for node in ast.walk(tree):
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                mods = [node.module.split(".")[0]]
            for mod in mods:
                if mod in STDLIB_OK:
                    continue
                pkg = IMPORT_TO_PIP.get(mod, mod)
                if pkg not in pip_line:
                    finding(name, n, "import",
                            "imports %r but %r is not in the cell-1 pip install" % (mod, pkg))

    # --- 4 · undefined names --------------------------------------
    defined = set(dir(builtins))
    defined |= {"client", "MODEL", "EMBED_MODEL", "API_KEY", "userdata",
                "genai", "types", "get_ipython"}
    undefined = []
    for n in sorted(trees):
        tree = trees[n]
        # Collect what this cell defines, and what it uses.
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                defined.add(node.name)
                defined |= {a.arg for a in node.args.args}
                defined |= {a.arg for a in node.args.kwonlyargs}
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                defined.add(node.id)
            elif isinstance(node, ast.arg):
                defined.add(node.arg)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for a in node.names:
                    defined.add(a.asname or a.name.split(".")[0])
            elif isinstance(node, ast.ExceptHandler) and node.name:
                defined.add(node.name)
            elif isinstance(node, ast.comprehension):
                for t in ast.walk(node.target):
                    if isinstance(t, ast.Name):
                        defined.add(t.id)
            elif isinstance(node, (ast.For, ast.AsyncFor)):
                for t in ast.walk(node.target):
                    if isinstance(t, ast.Name):
                        defined.add(t.id)
            elif isinstance(node, ast.withitem) and node.optional_vars:
                for t in ast.walk(node.optional_vars):
                    if isinstance(t, ast.Name):
                        defined.add(t.id)

        # A call inside `try: ... except NameError:` is a DOCUMENTED
        # cross-notebook dependency, not an accident. Collect those first.
        guarded = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                handles_nameerror = any(
                    isinstance(h.type, ast.Name) and h.type.id == "NameError"
                    for h in node.handlers)
                if handles_nameerror:
                    for sub in ast.walk(node):
                        if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name):
                            guarded.add(sub.func.id)

        # Now check calls in this cell against everything defined so far.
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id not in defined and node.func.id not in guarded:
                    undefined.append((n, node.func.id))

    for n, fn in undefined:
        finding(name, n, "undefined", "calls %r which is not defined earlier, "
                                      "imported, or a builtin" % fn)

    # --- 5 · key handling -----------------------------------------
    if not re.search(r"userdata\.get\(\s*'GEMINI_API_KEY'\s*\)", first):
        finding(name, code_cells[0][0] if code_cells else 1, "key",
                "the first code cell does not use userdata.get('GEMINI_API_KEY')")
    for pattern in (r"AIza[0-9A-Za-z_\-]{20,}", r"sk-[0-9A-Za-z]{20,}"):
        if re.search(pattern, all_text):
            finding(name, "-", "key", "looks like a hardcoded API key in the notebook")

    # --- 6 · model strings ----------------------------------------
    for model in set(m.rstrip(".,;:'\"`)") for m in
                     re.findall(r"gemini-[0-9a-zA-Z.\-]+", all_text)):
        if model not in ALLOWED_MODELS:
            finding(name, "-", "model", "uses model string %r" % model)

    # --- 7 · reflection and "if this breaks" ----------------------
    lower = all_text.lower()
    if "## reflection" not in lower:
        finding(name, "-", "reflection", "no reflection cell found")
    if "if this breaks" not in lower:
        finding(name, "-", "breaks", "no 'If this breaks' cell found")

    # --- 8 · TODO cells have structure ----------------------------
    for n, cell in code_cells:
        text = source(cell)
        if "TODO" not in text:
            continue
        body = [ln for ln in text.split("\n")
                if ln.strip() and not ln.strip().startswith("#")]
        if len(body) < 3:
            finding(name, n, "todo",
                    "TODO cell has only %d non-comment lines - a student would be "
                    "staring at an almost-empty cell" % len(body))

    return len(cells), len(code_cells)


def main():
    names = sorted(f for f in os.listdir(HERE) if f.endswith(".ipynb"))
    if not names:
        print("No notebooks found. Run build.py first.")
        return 1

    print("Checking %d notebooks\n" % len(names))
    for n in names:
        result = check_notebook(os.path.join(HERE, n))
        if result:
            print("  %-28s %2d cells (%d code)" % (n, result[0], result[1]))

    print()
    if not findings:
        print("PASS - all eight checks clean.")
        return 0

    print("%d finding(s):\n" % len(findings))
    for nb, cell, kind, msg in findings:
        print("  [%s] %s cell %s: %s" % (kind.upper(), nb, cell, msg))
    return 1


if __name__ == "__main__":
    sys.exit(main())
