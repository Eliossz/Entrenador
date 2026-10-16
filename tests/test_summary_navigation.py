#!/usr/bin/env python3
"""
Test suite verifying that navigation out of the summary view works properly
and that users are never trapped in 'phase: summary'.
"""

import sys
import os
import re

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HTML_FILE = "index.html"

def test_summary_exit_logic():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    # 1. Unfinished summaries offer explicit save, discard, or stay choices.
    assert "async function exitSummaryIfActive()" in code, "exitSummaryIfActive must await the user's choice"
    assert "session = null" in code, "exitSummaryIfActive must clear session"
    assert "saveSession()" in code, "exitSummaryIfActive must persist session clearing"
    exit_match = re.search(r'async function exitSummaryIfActive\(\)\s*\{(.*?)\n\}', code, re.DOTALL)
    assert exit_match, "exitSummaryIfActive body must be present"
    exit_body = exit_match.group(1)
    assert "Salir sin guardar" in exit_body and "Guardar y salir" in exit_body and "Seguir aquí" in exit_body
    assert "if(choice==='save') saveToHistory(true)" in exit_body, "Only the explicit save choice may write the summary to history"

    # 2. Navigation handlers call exitSummaryIfActive
    nav_match = re.search(r'nav\(el\)\s*\{([^}]+)\}', code)
    assert nav_match and "exitSummaryIfActive()" in nav_match.group(1), "A.nav must call exitSummaryIfActive"

    go_home_match = re.search(r"'go-home'\(\)\s*\{([^}]+)\}", code)
    assert go_home_match and "exitSummaryIfActive()" in go_home_match.group(1), "A['go-home'] must call exitSummaryIfActive"

    go_cat_match = re.search(r"'go-category'\(el\)\s*\{([^}]+)\}", code)
    assert go_cat_match and "exitSummaryIfActive()" in go_cat_match.group(1), "A['go-category'] must call exitSummaryIfActive"

    # 3. render() checks ui.view before defaulting to summary
    render_idx = code.find("function render()")
    assert render_idx != -1, "render() must be defined"
    render_body = code[render_idx:render_idx+1200]
    
    pos_home = render_body.find("ui.view==='home'")
    pos_summary = render_body.find("session.phase==='summary'")
    assert pos_home != -1, "ui.view==='home' check must exist in render"
    assert pos_summary != -1, "session.phase==='summary' check must exist in render"
    assert pos_home < pos_summary, "ui.view==='home' must take priority over session.phase==='summary' in render()"

    # 4. sanitizeSession discards already-saved summary sessions
    assert "raw.phase==='summary' && raw.saved" in code, "sanitizeSession must discard already-saved summary sessions"

    print("[OK] Summary exit and navigation integrity verified!")

if __name__ == "__main__":
    test_summary_exit_logic()
    print("ALL SUMMARY NAVIGATION TESTS PASSED!")
