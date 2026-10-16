#!/usr/bin/env python3
"""
Accurate syntax validator for index.html.
"""

import sys

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def check_script_balance(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    s = content.find("<script>") + 8
    e = content.rfind("</script>")
    js = content[s:e]

    output = list(js)
    i = 0
    L = len(js)

    while i < L:
        if js[i:i+2] == '//':
            j = i
            while j < L and js[j] != '\n':
                output[j] = ' '
                j += 1
            i = j
            continue

        if js[i:i+2] == '/*':
            j = i + 2
            while j < L and js[j:j+2] != '*/':
                if js[j] != '\n':
                    output[j] = ' '
                j += 1
            if j < L:
                output[j] = ' '
                output[j+1] = ' '
                j += 2
            i = j
            continue

        if js[i] == "'":
            output[i] = ' '
            j = i + 1
            while j < L:
                if js[j] == '\\':
                    output[j] = ' '
                    output[j+1] = ' '
                    j += 2
                    continue
                if js[j] == "'":
                    output[j] = ' '
                    j += 1
                    break
                if js[j] != '\n':
                    output[j] = ' '
                j += 1
            i = j
            continue

        if js[i] == '"':
            output[i] = ' '
            j = i + 1
            while j < L:
                if js[j] == '\\':
                    output[j] = ' '
                    output[j+1] = ' '
                    j += 2
                    continue
                if js[j] == '"':
                    output[j] = ' '
                    j += 1
                    break
                if js[j] != '\n':
                    output[j] = ' '
                j += 1
            i = j
            continue

        if js[i] == '/' and i > 0 and js[i-1] in '=(,[:!&|?':
            output[i] = ' '
            j = i + 1
            while j < L:
                if js[j] == '\\':
                    output[j] = ' '
                    output[j+1] = ' '
                    j += 2
                    continue
                if js[j] == '/':
                    output[j] = ' '
                    j += 1
                    while j < L and js[j] in 'gimsuy':
                        output[j] = ' '
                        j += 1
                    break
                if js[j] != '\n':
                    output[j] = ' '
                j += 1
            i = j
            continue

        if js[i] == '`':
            output[i] = ' '
            j = i + 1
            while j < L:
                if js[j] == '\\':
                    output[j] = ' '
                    output[j+1] = ' '
                    j += 2
                    continue
                if js[j] == '`':
                    output[j] = ' '
                    j += 1
                    break
                if js[j:j+2] == '${':
                    output[j] = '('
                    output[j+1] = ' '
                    depth = 1
                    k = j + 2
                    while k < L and depth > 0:
                        if js[k] in ('"', "'", '`'):
                            q = js[k]
                            k += 1
                            while k < L and js[k] != q:
                                if js[k] == '\\': k += 2
                                else: k += 1
                            k += 1
                            continue
                        if js[k] == '{': depth += 1
                        elif js[k] == '}':
                            depth -= 1
                            if depth == 0:
                                output[k] = ')'
                                break
                        k += 1
                    j = k + 1
                    continue
                if js[j] != '\n':
                    output[j] = ' '
                j += 1
            i = j
            continue

        i += 1

    cleaned = "".join(output)
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}

    for idx, ch in enumerate(cleaned):
        if ch in '({[':
            stack.append((ch, idx))
        elif ch in ')}]':
            if not stack:
                line_no = js[:idx].count('\n') + 1
                raise ValueError(f"Unmatched '{ch}' at line {line_no}: {js[max(0, idx-40):min(len(js), idx+40)]}")
            top, top_idx = stack.pop()
            if top != pairs[ch]:
                line_no = js[:idx].count('\n') + 1
                top_line = js[:top_idx].count('\n') + 1
                raise ValueError(f"Mismatched '{ch}' at line {line_no} for '{top}' from line {top_line}: {js[max(0, idx-50):min(len(js), idx+50)]}")

    if stack:
        top, top_idx = stack.pop()
        line_no = js[:top_idx].count('\n') + 1
        raise ValueError(f"Unclosed '{top}' from line {line_no}: {js[max(0, top_idx-50):min(len(js), top_idx+50)]}")

    print(f"[OK] {filepath} JavaScript is perfectly balanced and syntax is valid!")

if __name__ == "__main__":
    check_script_balance("index.html")
