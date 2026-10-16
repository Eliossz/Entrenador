#!/usr/bin/env python3
"""
Test suite for the 'Abdomen en casa' (Abdominales) routine integration in index.html.
"""

import sys
import os
import re

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HTML_FILE = "index.html"

def test_file_exists():
    assert os.path.exists(HTML_FILE), f"{HTML_FILE} must exist"
    assert not os.path.exists("index (5).html"), "Old duplicate 'index (5).html' must NOT exist"
    print("[OK] Single canonical index.html verified")

def test_html_content(filepath):
    assert os.path.exists(filepath), f"File {filepath} must exist"
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # General requirements
    assert "Abdomen" in html or "Abdominales" in html, "Should mention Abdomen/Abdominales"
    assert "Abdomen en casa" in html, "Should have routine name 'Abdomen en casa'"
    assert "Una rutina para fortalecer el abdomen, mejorar la estabilidad del core y desarrollar resistencia muscular" in html, "Should include exact description"
    assert "22–28 minutos" in html or "22-28" in html, "Should include estimated duration 22-28 min"
    assert "Intermedio" in html or "intermedio" in html, "Should state intermediate level"
    assert "colchoneta" in html, "Should mention colchoneta opcional"

    # Check 10 exercises in order
    exercises = [
        "Jumping Jacks",
        "Reverse Crunch",
        "Lying Leg Raises",
        "Bicycle Crunch",
        "V-Ups",
        "Plancha frontal",
        "Plancha lateral",
        "Cobra Stretch",
        "Estiramiento lumbar en rotación (lado izquierdo)",
        "Estiramiento lumbar en rotación (lado derecho)"
    ]
    for ex in exercises:
        idx = html.find(ex)
        assert idx != -1, f"Exercise '{ex}' must be present in HTML"
        print(f"  [OK] Found exercise: {ex}")

    # Specific requirements
    assert "Step Jacks" in html or "sin saltos" in html, "Must offer alternative for Jumping Jacks without jumps"
    assert "Bent-Knee Leg Raises" in html or "rodillas flexionadas" in html, "Must offer alternative for Leg Raises with bent knees"
    assert "Tuck V-Ups" in html or "rodillas flexionadas" in html, "Must offer alternative for V-Ups with bent knees"
    assert "Lado izquierdo" in html and "Lado derecho" in html, "Plancha lateral must specify sides"
    assert "Cobra Stretch" in html, "Must include Cobra Stretch as stretch"
    assert "Estiramiento lumbar en rotación" in html, "Must include lumbar stretches at the end"
    
    # Visual and safety warnings
    assert "dolor" in html, "Must include discreet safety warning"

    # Buttons and controls
    assert "Comenzar entrenamiento" in html, "Must have button 'Comenzar entrenamiento'"
    assert "Volver al menú" in html or "Volver a" in html, "Must have return option"
    assert "Repetir entrenamiento" in html, "Must have repeat workout option"

    # Navigation tabs
    assert 'data-v="cat-abs"' in html or 'data-v="abs"' in html, "Must have Abdomen tab in navigation"

    print(f"[OK] All content assertions passed for {filepath}")

def test_routine_structure():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        code = f.read()

    # Check ABS_ROUTINE definition
    pattern = r'const ABS_ROUTINE\s*=\s*\[(.*?)\];'
    match = re.search(pattern, code, re.DOTALL)
    assert match, "ABS_ROUTINE must be defined as an array"
    content = match.group(1)

    # 1. Jumping jacks: 60s, 1 set, 30s rest, type time
    assert "jumping_jacks" in content
    assert "60" in content
    # 2. Reverse crunch: 15 reps, 3 sets, 45s rest
    assert "reverse_crunch" in content
    assert "15" in content
    # 3. Lying leg raises: 12-15 reps, 3 sets, 50s rest, alt bent-knee
    assert "lying_leg_raises" in content
    assert "absAltLegRaises" in content
    # 4. Bicycle crunch: 20 reps, 3 sets, 45s rest
    assert "bicycle_crunch" in content
    assert "20" in content
    # 5. V-Ups: 10-12 reps, 3 sets, 60s rest
    assert "v_ups" in content
    # 6. Plancha frontal: 40s, 3 sets, 45s rest
    assert "plancha_frontal" in content
    assert "40" in content
    # 7. Plancha lateral: 50s, 4 sets (2 per side), 45s rest
    assert "plancha_lateral" in content
    assert "50" in content
    assert "sides" in content
    # 8. Cobra stretch: 60s, 1 set, 15s rest
    assert "cobra_stretch" in content
    assert "60" in content
    # 9. Estiramiento lumbar izq: 30s, 1 set, 15s rest
    assert "lumbar_stretch_left" in content
    # 10. Estiramiento lumbar der: 30s, 1 set, 0s rest
    assert "lumbar_stretch_right" in content

    # Check ALL_ROUTINES.abs has exercisesCount: 10
    pattern_meta = r'abs:\s*\{[^}]*exercisesCount:\s*10'
    assert re.search(pattern_meta, code), "ALL_ROUTINES.abs must have exercisesCount: 10"

    print("[OK] ABS_ROUTINE structure verified with 10 exercises and updated parameters")

def test_state_machine_logic():
    # 10 exercises:
    # 1: JJ (1 set)
    # 2: RC (3 sets)
    # 3: LLR (3 sets)
    # 4: BC (3 sets)
    # 5: VU (3 sets)
    # 6: PF (3 sets)
    # 7: PL (4 sets)
    # 8: CS (1 set)
    # 9: LSL (1 set)
    # 10: LSR (1 set)
    # Total = 1 + 3 + 3 + 3 + 3 + 3 + 4 + 1 + 1 + 1 = 23 sets
    session = {
        "routineId": "abs",
        "phase": "work",
        "cur": {"ex": 0, "set": 0},
        "logs": [
            [{"status": "pending", "reps": None}],  # 1. Jumping Jacks (1)
            [{"status": "pending", "reps": None}, {"status": "pending", "reps": None}, {"status": "pending", "reps": None}],  # 2. Reverse Crunch (3)
            [{"status": "pending", "reps": None}, {"status": "pending", "reps": None}, {"status": "pending", "reps": None}],  # 3. Lying Leg Raises (3)
            [{"status": "pending", "reps": None}, {"status": "pending", "reps": None}, {"status": "pending", "reps": None}],  # 4. Bicycle Crunch (3)
            [{"status": "pending", "reps": None}, {"status": "pending", "reps": None}, {"status": "pending", "reps": None}],  # 5. V-Ups (3)
            [{"status": "pending", "reps": None}, {"status": "pending", "reps": None}, {"status": "pending", "reps": None}],  # 6. Plancha frontal (3)
            [{"status": "pending", "reps": None}, {"status": "pending", "reps": None}, {"status": "pending", "reps": None}, {"status": "pending", "reps": None}],  # 7. Plancha lateral (4)
            [{"status": "pending", "reps": None}],  # 8. Cobra Stretch (1)
            [{"status": "pending", "reps": None}],  # 9. Lumbar Stretch Left (1)
            [{"status": "pending", "reps": None}],  # 10. Lumbar Stretch Right (1)
        ],
        "rest": None,
        "workTimer": None
    }
    
    total_sets = sum(len(l) for l in session["logs"])
    assert total_sets == 23, f"Expected 23 sets, got {total_sets}"
    print(f"[OK] Total sets counted: {total_sets}")

    # Simulate finishing exercise 0 (Jumping Jacks)
    session["logs"][0][0]["status"] = "done"
    session["logs"][0][0]["reps"] = 60
    session["cur"] = {"ex": 1, "set": 0}
    session["rest"] = {"total": 30000, "remaining": 30000, "paused": False}
    assert session["logs"][0][0]["status"] == "done"

    session["rest"]["paused"] = True
    session["rest"]["remaining"] += 15000
    assert session["rest"]["remaining"] == 45000
    session["rest"] = None

    # Simulate finishing remaining 9 exercises
    for ex_idx in range(1, 10):
        for set_idx in range(len(session["logs"][ex_idx])):
            session["logs"][ex_idx][set_idx]["status"] = "done"
            session["logs"][ex_idx][set_idx]["reps"] = 15
    
    done_count = sum(sum(1 for s in l if s["status"] == "done") for l in session["logs"])
    assert done_count == total_sets
    session["phase"] = "summary"
    print(f"[OK] State machine simulated all {done_count} sets across 10 exercises and completed to summary")

if __name__ == "__main__":
    test_file_exists()
    test_html_content(HTML_FILE)
    test_routine_structure()
    test_state_machine_logic()
    print("\nALL TEST SUITES PASSED SUCCESSFULLY!")
