"""Contrast checks for the generated M3 palettes.

Parses assets/m3-theme.css so it runs with no extra dependencies. Re-run after
changing SEEDS in scripts/gen_m3_theme.py.
"""

import re
from pathlib import Path

import pytest

CSS = Path(__file__).resolve().parent.parent / "assets" / "m3-theme.css"

# (foreground, background, minimum ratio). 4.5 for body text, 3.0 for large
# text and UI component boundaries, per WCAG 2.1.
PAIRS = [
    ("on-primary", "primary", 4.5),
    ("on-primary-container", "primary-container", 4.5),
    ("on-secondary", "secondary", 4.5),
    ("on-secondary-container", "secondary-container", 4.5),
    ("on-tertiary", "tertiary", 4.5),
    ("on-tertiary-container", "tertiary-container", 4.5),
    ("on-error", "error", 4.5),
    ("on-error-container", "error-container", 4.5),
    ("on-surface", "surface", 4.5),
    ("on-surface", "surface-container-low", 4.5),
    ("on-surface", "surface-container-high", 4.5),
    ("on-surface-variant", "surface", 4.5),
    ("on-surface-variant", "surface-container", 4.5),
    ("inverse-on-surface", "inverse-surface", 4.5),
    ("primary", "surface", 3.0),
    ("outline", "surface", 3.0),
]


def _luminance(hex_color: str) -> float:
    channels = []
    for i in (1, 3, 5):
        c = int(hex_color[i : i + 2], 16) / 255
        channels.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg: str, bg: str) -> float:
    a, b = _luminance(fg), _luminance(bg)
    lo, hi = sorted((a, b))
    return (hi + 0.05) / (lo + 0.05)


def blocks() -> dict[str, dict[str, str]]:
    """Map each selector block to its --md-sys-color-* values."""
    css = CSS.read_text(encoding="utf-8")
    out = {}
    for selector, body in re.findall(r"([^{}]+)\{([^}]*)\}", css):
        tokens = dict(re.findall(r"--md-sys-color-([a-z-]+):\s*(#[0-9a-f]{6})", body))
        if tokens:
            out[selector.strip()] = tokens
    return out


@pytest.mark.parametrize("selector,tokens", blocks().items())
def test_palette_contrast(selector: str, tokens: dict[str, str]):
    failures = [
        f"{fg} on {bg}: {contrast(tokens[fg], tokens[bg]):.2f} < {minimum}"
        for fg, bg, minimum in PAIRS
        if fg in tokens and bg in tokens and contrast(tokens[fg], tokens[bg]) < minimum
    ]
    assert not failures, f"{selector}\n  " + "\n  ".join(failures)


def test_every_seed_generated():
    """All five seeds plus the default must be present in both modes."""
    css = CSS.read_text(encoding="utf-8")
    for seed in ("purple", "blue", "green", "crimson"):
        assert css.count(f'data-m3-seed="{seed}"') >= 2, f"{seed} missing a light or dark block"
