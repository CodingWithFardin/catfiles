#!/usr/bin/env python3
"""catfiles - concatenate source files with language-aware fences."""
import argparse
import os
import sys

LANG = {".py": "python", ".js": "javascript", ".ts": "typescript", ".go": "go",
        ".rs": "rust", ".sh": "bash", ".sql": "sql", ".md": "markdown",
        ".json": "json", ".yml": "yaml", ".yaml": "yaml", ".c": "c", ".h": "c"}
SKIP = {".git", "node_modules", "__pycache__", ".venv", "dist", "target"}


def collect(root, include_hidden=False, ext=None):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP)
        for name in sorted(filenames):
            if not include_hidden and name.startswith("."):
                continue
            if ext and os.path.splitext(name)[1] not in ext:
                continue
            out.append(os.path.join(dirpath, name))
    return out


def render(paths, root, fence=True):
    chunks = []
    for path in paths:
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        lang = LANG.get(os.path.splitext(path)[1].lower(), "")
        try:
            body = open(path, encoding="utf-8").read().rstrip("\n")
        except (OSError, UnicodeDecodeError):
            continue
        header = "### %s" % rel
        if fence:
            chunks.append("%s\n\`\`\`%s\n%s\n\`\`\`" % (header, lang, body))
        else:
            chunks.append("%s\n%s" % (header, body))
    return "\n\n".join(chunks)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="catfiles", description=__doc__)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--no-fence", action="store_true")
    ap.add_argument("--hidden", action="store_true")
    ap.add_argument("--ext", nargs="*")
    args = ap.parse_args(argv)
    ext = {e if e.startswith(".") else "." + e for e in args.ext} if args.ext else None
    print(render(collect(args.root, args.hidden, ext), args.root, not args.no_fence))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
