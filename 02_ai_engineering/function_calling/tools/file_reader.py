import os
import tempfile

MAX_CHARS = 2000


def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.splitlines()
        truncated = len(content) > MAX_CHARS
        preview = content[:MAX_CHARS]
        suffix = (
            f"\n\n[truncated — {len(lines)} lines total, showing first {MAX_CHARS} chars]"
            if truncated
            else f"\n\n[{len(lines)} lines]"
        )
        return preview + suffix
    except FileNotFoundError:
        return f"File not found: {path}"
    except PermissionError:
        return f"Permission denied: {path}"
    except UnicodeDecodeError:
        return f"Cannot read '{path}': not a text file"
    except Exception as e:
        return f"Error reading '{path}': {e}"


SCHEMA = {
    "name": "read_file",
    "description": "Read contents of a file",
    "parameters": {
        "type": "object",
        "properties": {"path": {"type": "string", "description": "File path"}},
        "required": ["path"],
    },
}

if __name__ == "__main__":
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("line1\nline2\nline3\n")
        tmp = f.name

    print(read_file(tmp))
    print(read_file("/nonexistent/path.txt"))
    os.unlink(tmp)
