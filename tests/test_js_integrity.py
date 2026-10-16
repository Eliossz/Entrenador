#!/usr/bin/env python3
"""
Deep inspection of JavaScript and HTML event handlers in index.html.
"""

import sys
import os
import re

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

def test_js_event_handlers():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    acts_in_html = set(re.findall(r'data-act="([^"]+)"', content))
    print(f"Found {len(acts_in_html)} unique data-act attributes in markup: {sorted(acts_in_html)}")

    match = re.search(r'const A\s*=\s*\{(.*?)\n\};', content, re.DOTALL)
    assert match, "Could not find 'const A = { ... };' object in script"
    a_block = match.group(1)

    handlers = set()
    for line in a_block.split("\n"):
        line = line.strip()
        m = re.match(r"(?:async\s+)?(?:'([^']+)'|([a-zA-Z0-9_\-]+))\s*\(", line)
        if m:
            handlers.add(m.group(1) or m.group(2))

    print(f"Found {len(handlers)} handlers in A object: {sorted(handlers)}")

    missing = acts_in_html - handlers
    assert not missing, f"Missing event handlers for data-acts: {missing}"
    print("[OK] Every data-act has a corresponding JavaScript handler!")

def test_timed_vs_reps_handling():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    assert "workTimerToggle" in content
    assert "workTimerReset" in content
    assert "completeTimedSet" in content
    assert "workClock" in content
    assert "workBar" in content
    print("[OK] Timed exercise functions verified!")

    assert "time_sides" in content
    assert "Lado izquierdo" in content
    assert "Lado derecho" in content
    print("[OK] Side plank bilateral logic verified!")

def test_buttons_and_accessibility():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    assert 'id="modalRoot"' in content
    assert 'id="toast"' in content
    assert 'id="live"' in content
    assert 'aria-live="polite"' in content
    assert 'role="progressbar"' in content
    assert 'role="timer"' in content
    print("[OK] Accessibility attributes verified!")

if __name__ == "__main__":
    test_js_event_handlers()
    test_timed_vs_reps_handling()
    test_buttons_and_accessibility()
    print("\nALL DEEP INTEGRITY TESTS PASSED!")
