# Rail Logistics Company (HOI4)

A new **support company** that improves your divisions' supply situation —
and finally gives you a reason to keep producing **locomotives** late game.

Requires the **No Step Back** DLC (trains don't exist without it). Works
with Road to 56 and everything else in this repo.

## What it does

**Rail Logistics Company** (support slot, available from game start):

| | Base | + Wartime Trains | + Armored Trains |
|---|---|---|---|
| Supply consumption | **−5%** | −10% | **−15%** |
| Supply grace | **+24h** | +48h | **+72h** |
| Out-of-supply penalty | **−10%** | −20% | **−30%** |

- **Costs 10 trains + 10 support equipment** per company — locomotives
  become divisional equipment, so your train production lines matter even
  after the rail network is built out.
- **Scales with locomotive tech:** researching **Wartime Trains**
  (`wartime_train`) and **Armored Trains** (`armored_train`) each
  automatically upgrade every rail logistics company via hidden bonus
  technologies (granted silently the moment the research finishes).
- Add it to your big expensive divisions — that's where the supply savings
  and the grace hours count.

## Design notes

- Modelled directly on the vanilla `logistics_company` sub-unit (same
  manpower, training time, org profile), so it slots into the game's
  balance rather than around it.
- The hidden techs have **no research-tree position at all**, so they can't
  collide with vanilla or Road to 56 tech-tree layouts. Grants happen via
  `on_startup` / `on_research_complete` (with a monthly idempotent
  fallback), so it also works when added to an **existing save** — already
  researched train techs are detected and applied at load.
- Uses the generic infantry support icon (no custom art). If you later want
  a train icon, drop a sprite in `gfx/` and point `sprite` at it.

## Tuning

`common/units/ocr_rail_logistics.txt`: base stats and the `need` block
(train cost per company). `common/technologies/ocr_rail_logistics_techs.txt`:
the per-tier boosts.

## Installation

From the repo root: `.\install.ps1 -Mod rail_logistics_company` (Windows)
or `./install.sh rail_logistics_company` (Linux/macOS), then enable it in
your Playset. Safe to add mid-save.
