"""Generate assets/m3-theme.css: M3 color tokens + the Radix Themes variable bridge.

Run once after changing SEEDS (needs no runtime dependency):

    uv run --with materialyoucolor python scripts/gen_m3_theme.py

The generated file is committed. Nothing imports materialyoucolor at runtime.
"""

from pathlib import Path

from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from materialyoucolor.hct import Hct
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot

OUT = Path(__file__).resolve().parent.parent / "assets" / "m3-theme.css"

# First entry is the default (applies with no data-m3-seed attribute).
SEEDS = {
    "teal": 0xFF00696E,
    "purple": 0xFF6750A4,
    "blue": 0xFF0061A4,
    "green": 0xFF386A20,
    "crimson": 0xFFA4143C,
}

# M3 roles emitted as --md-sys-color-*. camelCase attr on MaterialDynamicColors -> kebab token.
ROLES = [
    "primary",
    "onPrimary",
    "primaryContainer",
    "onPrimaryContainer",
    "secondary",
    "onSecondary",
    "secondaryContainer",
    "onSecondaryContainer",
    "tertiary",
    "onTertiary",
    "tertiaryContainer",
    "onTertiaryContainer",
    "error",
    "onError",
    "errorContainer",
    "onErrorContainer",
    "surface",
    "onSurface",
    "onSurfaceVariant",
    "surfaceVariant",
    "surfaceContainerLowest",
    "surfaceContainerLow",
    "surfaceContainer",
    "surfaceContainerHigh",
    "surfaceContainerHighest",
    "surfaceDim",
    "surfaceBright",
    "surfaceTint",
    "outline",
    "outlineVariant",
    "inverseSurface",
    "inverseOnSurface",
    "inversePrimary",
    "scrim",
    "shadow",
]

# Radix's 1-12 scale is perceptual: 1 app bg, 2 subtle bg, 3 element bg, 4 hover,
# 5 active, 6 subtle border, 7 border, 8 strong border, 9 solid, 10 solid hover,
# 11 low-contrast text, 12 high-contrast text. These tones land each step on the
# M3 role that carries the same meaning (3 == primary-container, 9 == primary,
# 11 == accent text, 12 == on-primary-container).
ACCENT_TONES_LIGHT = [99, 95, 90, 86, 82, 76, 68, 58, 40, 32, 40, 10]
ACCENT_TONES_DARK = [10, 14, 30, 34, 38, 44, 52, 62, 80, 86, 80, 90]
# Neutral steps 1-5/12 come from the neutral palette (surfaces, on-surface),
# 6-11 from neutral-variant (outline, on-surface-variant) as M3 specifies.
NEUTRAL_TONES_LIGHT = [98, 96, 94, 92, 90, 80, 70, 60, 50, 44, 30, 10]
NEUTRAL_TONES_DARK = [6, 10, 12, 17, 22, 30, 40, 50, 60, 70, 80, 90]

# Radix's alpha scale drives hover/pressed fills, so a1-a8 are just M3
# state-layer opacities over the "on" color. a9-a12 alias the solid steps -- they
# back solid fills where the alpha never showed. Exact Radix alpha math if it ever shows.
STATE_LAYER_ALPHA = [3, 5, 8, 12, 16, 20, 28, 38]


def hexes(scheme) -> dict[str, str]:
    out = {}
    for role in ROLES:
        r, g, b = getattr(MaterialDynamicColors, role).get_hct(scheme).to_rgba()[:3]
        out[role] = f"#{r:02x}{g:02x}{b:02x}"
    return out


def tone_hex(palette, tone: int) -> str:
    r, g, b = Hct.from_int(palette.tone(tone)).to_rgba()[:3]
    return f"#{r:02x}{g:02x}{b:02x}"


def kebab(name: str) -> str:
    return "".join(f"-{c.lower()}" if c.isupper() else c for c in name)


def block(seed: int, dark: bool) -> list[str]:
    scheme = SchemeTonalSpot(Hct.from_int(seed), dark, 0.0)
    c = hexes(scheme)
    accent = [tone_hex(scheme.primary_palette, t) for t in (ACCENT_TONES_DARK if dark else ACCENT_TONES_LIGHT)]
    neutral_tones = NEUTRAL_TONES_DARK if dark else NEUTRAL_TONES_LIGHT
    neutral = [
        tone_hex(scheme.neutral_variant_palette if 5 <= i <= 10 else scheme.neutral_palette, t)
        for i, t in enumerate(neutral_tones)
    ]

    lines = [f"  --md-sys-color-{kebab(r)}: {v};" for r, v in c.items()]
    lines.append("")
    lines += [f"  --accent-{i + 1}: {v};" for i, v in enumerate(accent)]
    lines += [f"  --gray-{i + 1}: {v};" for i, v in enumerate(neutral)]
    lines.append("")
    lines += [
        f"  --accent-a{i + 1}: color-mix(in srgb, {c['primary']} {a}%, transparent);"
        for i, a in enumerate(STATE_LAYER_ALPHA)
    ]
    lines += [f"  --accent-a{i}: var(--accent-{i});" for i in range(9, 13)]
    lines += [
        f"  --gray-a{i + 1}: color-mix(in srgb, {c['onSurface']} {a}%, transparent);"
        for i, a in enumerate(STATE_LAYER_ALPHA)
    ]
    lines += [f"  --gray-a{i}: var(--gray-{i});" for i in range(9, 13)]
    lines.append("")
    lines += [
        f"  --accent-contrast: {c['onPrimary']};",
        f"  --accent-surface: {c['primaryContainer']};",
        f"  --accent-indicator: {c['primary']};",
        f"  --accent-track: {c['primary']};",
        f"  --gray-contrast: {c['surface']};",
        f"  --gray-surface: {c['surfaceContainerLow']};",
        f"  --color-background: {c['surface']};",
        f"  --color-surface: {c['surfaceContainerLow']};",
        f"  --color-panel-solid: {c['surfaceContainerLow']};",
        f"  --color-panel-translucent: {c['surfaceContainerLow']};",
        f"  --color-overlay: color-mix(in srgb, {c['scrim']} 32%, transparent);",
        f"  --focus-8: {c['primary']};",
        f"  --focus-a3: color-mix(in srgb, {c['primary']} 12%, transparent);",
    ]
    return lines


def selectors(name: str, dark: bool) -> str:
    """Build the selector for one seed/mode block.

    Radix's own sheet loads after ours and sits at (0,1,0) behind :where(), so
    doubling .radix-themes puts every override above it without !important.

    Seed blocks are anchored at :root rather than at the themed element itself.
    Dialogs, drawers and tooltips render through React portals attached to
    <body>, so their .radix-themes wrapper is a *sibling* of the app tree and
    never a descendant of the element carrying data-m3-seed. Matching from the
    root means any .radix-themes in the document picks up the active seed.

    Resulting specificity, in ascending order so each layer wins correctly:
    light default (0,2,0) < dark default (0,3,0) < light seed (0,4,0) < dark seed (0,5,0).
    """
    themed = ".radix-themes.radix-themes"
    if name == next(iter(SEEDS)):
        return f":is(.dark, .dark-theme) {themed}" if dark else themed

    seeded = f':root:has([data-m3-seed="{name}"])'
    if not dark:
        return f"{seeded} {themed}"
    # Two arms so dark matching is exactly as permissive as the default rule
    # above: .dark can sit on <html> itself (first arm) or on any element below
    # it (second arm, which is how Radix marks a dark subtree).
    return f"{seeded}:is(.dark, .dark-theme) {themed}, {seeded} :is(.dark, .dark-theme) {themed}"


def swatches(dark: bool) -> list[str]:
    """Each seed's primary, so the settings picker can preview every palette."""
    lines = []
    for name, seed in SEEDS.items():
        scheme = SchemeTonalSpot(Hct.from_int(seed), dark, 0.0)
        r, g, b = MaterialDynamicColors.primary.get_hct(scheme).to_rgba()[:3]
        lines.append(f"  --m3-seed-{name}: #{r:02x}{g:02x}{b:02x};")
    return lines


def main() -> None:
    out = [
        "/* GENERATED by scripts/gen_m3_theme.py -- do not edit by hand. */",
        "/* M3 color roles + Radix Themes variable bridge. */",
    ]
    for name, seed in SEEDS.items():
        for dark in (False, True):
            out.append("")
            out.append(f"/* {name} / {'dark' if dark else 'light'} */")
            out.append(f"{selectors(name, dark)} {{")
            out += block(seed, dark)
            out.append("}")
    for dark in (False, True):
        out.append("")
        out.append(f"/* seed swatches / {'dark' if dark else 'light'} */")
        out.append(f"{':is(.dark, .dark-theme) ' if dark else ''}.radix-themes.radix-themes {{")
        out += swatches(dark)
        out.append("}")
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(out)} lines)")


if __name__ == "__main__":
    main()
