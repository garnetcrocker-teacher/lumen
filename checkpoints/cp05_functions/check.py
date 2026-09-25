"""
Checkpoint 5 auto-check.   Run:  python check.py

Imports the two functions from main.py (draw_dashboard, handle_controls)
and exercises them directly.
No window opens. Paste the final score into Canvas.
"""

import os
import sys

os.environ["LUMEN_HEADLESS"] = "1"

TOTAL_CHECKS = 13

results = []


def check(label, passed, detail=""):
    results.append(bool(passed))
    flag = "[PASS]" if passed else "[FAIL]"
    print(f"  {flag} {label}" + ("" if passed or not detail else f"   ({detail})"))


def _hull(depth_m, rated_m):
    """Independent copy of the Checkpoint 3 rule."""
    if depth_m < rated_m:
        return "OK"
    elif depth_m < 1.5 * rated_m:
        return "CAUTION"
    return "BREACH"


def _oxy(oxygen_pct):
    if oxygen_pct > 50:
        return "GOOD"
    elif oxygen_pct > 15:
        return "LOW"
    return "CRITICAL"


_EXPECTED_ALERT_COLOR = {"DANGER": (230, 90, 80), "WARNING": (230, 190, 90), "SAFE": (90, 200, 150)}


def main():
    try:
        import main as student
    except Exception as exc:
        print(f"  [FAIL] could not import main.py: {exc!r}")
        return _report(0, TOTAL_CHECKS)

    needed = ("draw_dashboard", "handle_controls")
    for fn in needed:
        if not hasattr(student, fn):
            print(f"  [FAIL] main.py has no function called {fn}()")
            return _report(0, TOTAL_CHECKS)

    import engine

    def make_sub(depth=0.0, oxygen=100.0, rated=1000.0, ballast=40.0, power=100.0, hull=100.0):
        sub = engine.Submarine(engine.DEFAULT_DIVEPLAN)
        sub.depth = depth
        sub.oxygen = oxygen
        sub.rated_depth = rated
        sub.ballast = ballast
        sub.power = power
        sub.hull = hull
        return sub

    # --- handle_controls -------------------------------------------------------
    real_down, real_pressed = engine.key_down, engine.key_pressed

    def call_controls(sub, down=(), pressed=()):
        engine.key_down = lambda name: name.upper() in down
        engine.key_pressed = lambda name: name.upper() in pressed
        try:
            student.handle_controls(sub)
        finally:
            engine.key_down, engine.key_pressed = real_down, real_pressed

    try:
        sub = make_sub(ballast=40, power=100, hull=100)
        call_controls(sub, down=("DOWN",))
        check("handle_controls: DOWN held + can_descend True -> sub.descending True",
              sub.descending is True, f"sub.descending = {sub.descending!r}")
    except Exception as exc:
        check("handle_controls: DOWN + can_descend True", False, repr(exc))

    try:
        sub = make_sub(power=0)
        call_controls(sub, down=("DOWN",))
        check("handle_controls: DOWN held but power is 0 -> sub.descending stays False",
              sub.descending is False, f"sub.descending = {sub.descending!r}")
    except Exception as exc:
        check("handle_controls: DOWN blocked by can_descend", False, repr(exc))

    try:
        sub = make_sub()
        call_controls(sub, down=("UP",))
        check("handle_controls: UP held -> sub.ascending True",
              sub.ascending is True, f"sub.ascending = {sub.ascending!r}")
    except Exception as exc:
        check("handle_controls: UP held", False, repr(exc))

    try:
        sub = make_sub()
        sub.light_on = True
        call_controls(sub, pressed=("L",))
        check("handle_controls: L pressed -> light_on True becomes False",
              sub.light_on is False, f"sub.light_on = {sub.light_on!r}")
    except Exception as exc:
        check("handle_controls: L pressed (True -> False)", False, repr(exc))

    try:
        sub = make_sub()
        sub.light_on = False
        call_controls(sub, pressed=("L",))
        check("handle_controls: L pressed -> light_on False becomes True",
              sub.light_on is True, f"sub.light_on = {sub.light_on!r}")
    except Exception as exc:
        check("handle_controls: L pressed (False -> True)", False, repr(exc))

    try:
        sub = make_sub()
        sub.light_on = True
        call_controls(sub)
        check("handle_controls: no keys -> nothing changes",
              sub.descending is False and sub.ascending is False and sub.light_on is True,
              f"descending={sub.descending!r} ascending={sub.ascending!r} light_on={sub.light_on!r}")
    except Exception as exc:
        check("handle_controls: no keys", False, repr(exc))

    # --- draw_dashboard ------------------------------------------------------
    real_hull_status_draw = engine.draw_hull_status
    real_hud_text = engine.draw_hud_text
    hull_calls = []
    text_calls = []
    engine.draw_hull_status = lambda screen, status: hull_calls.append(status)
    engine.draw_hud_text = lambda text, pos, size=16, color=(198, 216, 232), anchor="topleft": \
        text_calls.append({"text": text, "pos": tuple(pos), "size": size, "color": tuple(color), "anchor": anchor})

    try:
        sub = make_sub(depth=1200, oxygen=40, rated=1000)
        alert = "WARNING"
        student.draw_dashboard(None, sub, alert)
    except Exception as exc:
        check("draw_dashboard runs without error", False, repr(exc))
    finally:
        engine.draw_hull_status = real_hull_status_draw
        engine.draw_hud_text = real_hud_text

    expected_hull = _hull(1200, 1000)
    expected_oxy = _oxy(40)
    expected_color = _EXPECTED_ALERT_COLOR["WARNING"]

    check("draw_dashboard calls engine.draw_hull_status once with the current hull status",
          hull_calls == [expected_hull], f"got {hull_calls}")

    o2_line = next((c for c in text_calls if c["text"].startswith("O2: ")), None)
    check("draw_dashboard draws the O2 line correctly (text, position, size, color)",
          o2_line == {"text": "O2: " + expected_oxy, "pos": (480, 46), "size": 15,
                      "color": (150, 190, 210), "anchor": "midtop"},
          f"got {o2_line}")

    status_line = next((c for c in text_calls if c["text"].startswith("STATUS: ")), None)
    check("draw_dashboard draws the STATUS line with the matching alert color",
          status_line == {"text": f"STATUS: {alert}", "pos": (480, 66), "size": 14,
                           "color": expected_color, "anchor": "midtop"},
          f"got {status_line}")

    hint_line = next((c for c in text_calls if c["text"].startswith("DOWN dive")), None)
    check("draw_dashboard draws the controls-hint line",
          hint_line is not None
          and hint_line["text"] == "DOWN dive   UP rise   L light   ESC quit"
          and hint_line["pos"] == (16, engine.HEIGHT - 26)
          and hint_line["size"] == 13
          and hint_line["color"] == (120, 140, 155),
          f"got {hint_line}")

    check("draw_dashboard draws exactly 3 lines of HUD text (no extras, none missing)",
          len(text_calls) == 3, f"got {len(text_calls)}: {[c['text'] for c in text_calls]}")

    for alert_case, depth, rated, oxygen in [("SAFE", 500, 1000, 80), ("DANGER", 1500, 1000, 80)]:
        calls = []
        engine.draw_hud_text = lambda text, pos, size=16, color=(198, 216, 232), anchor="topleft": \
            calls.append({"text": text, "color": tuple(color)})
        engine.draw_hull_status = lambda screen, status: None
        try:
            sub = make_sub(depth=depth, oxygen=oxygen, rated=rated)
            student.draw_dashboard(None, sub, alert_case)
        except Exception as exc:
            check(f"draw_dashboard STATUS line color for alert={alert_case!r}", False, repr(exc))
            continue
        finally:
            engine.draw_hud_text = real_hud_text
            engine.draw_hull_status = real_hull_status_draw

        status_line = next((c for c in calls if c["text"].startswith("STATUS: ")), None)
        check(f"draw_dashboard STATUS line color for alert={alert_case!r}",
              status_line == {"text": f"STATUS: {alert_case}", "color": _EXPECTED_ALERT_COLOR[alert_case]},
              f"got {status_line}")

    _report(sum(results), len(results))


def _report(score, total):
    points = round(score / total * 100) if total else 0
    print()
    print(f"  SCORE: {score} / {total}      POINTS: {points} / 100")
    if score == total:
        print("  All checks passed. Submit this output to Canvas.")
    else:
        print("  Some checks failed - see the [FAIL] lines above.")


if __name__ == "__main__":
    main()
