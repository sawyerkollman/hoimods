# More Dockyards Per Ship — "Naval Blitz" (HOI4)

A tiny, highly-compatible mod that **raises the cap on how many dockyards you
can assign to a single naval production line**, so you can concentrate your
shipyards and pump out a big navy fast.

## What it changes

It overrides four `NProduction` defines. Vanilla limits → this mod:

| Line type | Vanilla cap | This mod |
|-----------|-------------|----------|
| Capital ships (battleships, carriers, cruisers…) | 5 | **50** |
| Screens & submarines (destroyers, subs…) | 10 | **50** |
| Convoys | 15 | **50** |
| Overall per-line ceiling | 15 | **50** |

The overall ceiling (`MAX_NAV_FACTORIES_PER_LINE`) has to be raised too,
because the per-type limits are clamped to it.

## Want a different number?

Open `common/defines/naval_dockyard_limits.lua` and change the `50`s to
whatever you like. A very large number effectively removes the limit.

## Compatibility

- **Standalone** — no dependencies. Works with vanilla, Road to 56, the
  Presidential Cabinet mod, and most other mods.
- The only conflict is with another mod that overrides these *same* defines;
  in that case load order decides (whichever loads last wins).
- Pure define override — it does not touch focus trees, units, or events.

## Installation

**Windows (recommended):** from the repo root, run the installer:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Mod more_dockyards_per_line
```

**Manual:** copy both `more_dockyards_per_line\` and
`more_dockyards_per_line.mod` from the repo's `mods\` folder into your HOI4
mod directory (`Documents\Paradox Interactive\Hearts of Iron IV\mod\`).

Then enable it in the launcher Playset. Define changes take effect when a
game loads, so start a new game (or reload a save) to see the new caps.

## File layout

```
descriptor.mod
common/defines/naval_dockyard_limits.lua
```
