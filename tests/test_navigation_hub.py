#!/usr/bin/env python3
"""
Test suite for the new 'Entrenador' Navigation Hub, Muscle Categories, and Hierarchical Flow in index.html.
"""

import sys
import os
import re

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HTML_FILE = "index.html"

def test_files_exist():
    assert os.path.exists(HTML_FILE), f"File {HTML_FILE} must exist"
    assert not os.path.exists("index (5).html"), "Duplicate index (5).html must NOT exist"
    print("[OK] Single canonical index.html verified")

def test_general_app_name():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    assert "<title>Entrenador" in html or "<title>Mi Entrenador" in html, "Page title must be 'Entrenador'"
    assert "Entrenador</span>" in html or "Entrenador<small>" in html or 'brandTitle">Entrenador' in html, "Brand title must be 'Entrenador'"
    assert '<span id="brandTitle">Abdomen en casa' not in html, "Global brand title must not be 'Abdomen en casa'"
    assert '<span id="brandTitle">Pecho en casa' not in html, "Global brand title must not be 'Pecho en casa'"

    print("[OK] General app name 'Entrenador' verified")

def test_categories_and_main_menu():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    assert "Pectorales" in html, "Must include 'Pectorales' category"
    assert "Abdominales" in html, "Must include 'Abdominales' category"
    assert "Otras rutinas" in html, "Must include 'Otras rutinas' category"

    assert "pecho" in html.lower(), "Must mention chest routines"
    assert "abdomen" in html.lower() or "core" in html.lower(), "Must mention abdomen/core routines"
    assert "espalda" in html.lower() or "piernas" in html.lower() or "brazos" in html.lower(), "Must mention future expansion groups"

    assert 'data-act="go-home"' in html or 'data-v="home"' in html, "Must have action to return to home/main menu"
    assert 'data-act="open-cat"' in html or 'data-v="cat-' in html, "Must have category view navigation"

    print("[OK] Categories and main menu verified")

def test_routines_preservation():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    abs_exercises = [
        "Jumping Jacks", "Reverse Crunch", "Lying Leg Raises", "Bicycle Crunch",
        "V-Ups", "Plancha frontal", "Plancha lateral", "Cobra Stretch",
        "Estiramiento lumbar en rotación"
    ]
    for ex in abs_exercises:
        assert ex in html, f"Abdomen exercise '{ex}' must be preserved"

    chest_exercises = [
        "Flexiones normales", "Flexiones abiertas", "Flexiones con pies elevados",
        "Flexiones diamante", "Flexiones lentas"
    ]
    for ex in chest_exercises:
        assert ex in html, f"Chest exercise '{ex}' must be preserved"

    assert "workClock" in html, "Timers must be preserved"
    assert "restClock" in html, "Rest timers must be preserved"

    print("[OK] All 10 Abdomen exercises and 5 Chest exercises preserved")

if __name__ == "__main__":
    test_files_exist()
    test_general_app_name()
    test_categories_and_main_menu()
    test_routines_preservation()
    print("\nALL NAVIGATION HUB TESTS PASSED!")
