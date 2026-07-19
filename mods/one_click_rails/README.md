# One-Click Rail Upgrades (HOI4)

Tired of upgrading railways line by line? This mod adds a single decision —
**Modernize the Rail Network** — that upgrades **every existing railway
between your own adjacent states by one level** in one click.

Find it in the **Economy** decisions tab (requires the **No Step Back** DLC,
since railways don't exist without it).

## How it works

HOI4's script engine cannot insert railways into the real construction queue
(nothing can — the queue isn't exposed to mods), so the decision simulates
construction the way major mods (e.g. Kaiserreich) do:

1. Click the decision: costs **50 political power** and reserves
   **3 civilian factories** for **45 days** (the "construction" period).
2. When the timer completes, every existing rail connection between your own
   adjacent states gains **+1 level** (up to the level-5 cap).
3. The decision goes on a 90-day cooldown, then you can run another pass.

Under the hood it sweeps every owned state, finds each neighboring owned
state with an existing rail connection (`has_railway_connection`), and fires
the game's `build_railway` effect once per unique pair — a visited-flag pass
guarantees no segment is double-upgraded in a single activation.

## Limitations (honest ones)

- **Owned states only.** Lines crossing into allied or occupied foreign
  territory aren't touched (this also prevents spending your PP upgrading
  someone else's network).
- **Existing connections only** — it never builds brand-new lines.
- The upgrade path between two states is chosen by the game's own
  rail-pathing (same logic the construction UI uses between hub provinces),
  which follows the existing line in virtually all adjacent-state cases.
- Player-only: the AI never uses it (`is_ai = no` + `ai_will_do = 0`).
- Not Ironman/achievement compatible (like all script mods).

## Tuning it

Open `common/decisions/one_click_rails_decisions.txt` and adjust:
- `cost = 50` — political power price
- `days_remove = 45` — construction time
- `civilian_factory_use = 3` — factories reserved while working
- `days_re_enable = 90` — cooldown between passes

## Installation

From the repo root: `.\install.ps1 -Mod one_click_rails` (Windows) or
`./install.sh one_click_rails` (Linux/macOS), then enable it in a Playset.
Standalone — no dependencies, compatible with everything in this repo and
with Road to 56. Works mid-save (it's just a decision).
