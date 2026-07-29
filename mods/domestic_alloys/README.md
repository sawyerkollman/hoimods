# Domestic Alloys Program (HOI4)

Stop importing half of Turkey's chromium. This mod adds tiered **domestic
chromium and tungsten production** keyed to the excavation technologies —
in the spirit of Road to 56's steel mills and aluminium refineries, and
fully compatible with them (it keys off the vanilla excavation techs that
both vanilla and R56 keep).

## How it works

Research the excavation line and the alloys program grows automatically,
adding permanent resources to your **capital state** (a notification event
fires at each tier):

| Tier | Unlocks with | Chromium | Tungsten |
|---|---|---|---|
| I | Excavation II | +8 | +8 |
| II | Excavation III | +8 | +8 |
| III | Excavation IV | +12 | +12 |
| **Total** | | **+28** | **+28** |

- Works for **every country** (the AI benefits too, so the world economy
  stays fair). To make it player-only, add `is_ai = no` to each `limit`
  block in `common/scripted_effects/ocr_alloys_effects.txt`.
- **Mid-save safe**: already-researched excavation tiers are detected and
  granted on load.
- No DLC required; no tech-tree entries (nothing to collide with R56's
  layouts).

## Tuning

Amounts and gating techs are all in
`common/scripted_effects/ocr_alloys_effects.txt` — one obvious block per
tier.

## Installation

From the repo root: `.\install.ps1 -Mod domestic_alloys` (Windows) or
`./install.sh domestic_alloys` (Linux/macOS), then enable it in your
Playset.
