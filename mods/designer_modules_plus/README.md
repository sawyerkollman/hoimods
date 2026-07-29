# Designer Modules Plus (HOI4)

New modules for all three equipment designers — tanks (NSB), ships (MtG),
and aircraft (BBA) — spanning wacky-but-unreliable early-game gear to
overpowered late-game weaponry gated behind advanced platforms.

Each designer's modules only appear if you own the matching DLC; the mod
degrades gracefully if you're missing one.

## The modules

### Aircraft (By Blood Alone)
| Module | Slot | Unlocks with | Character |
|---|---|---|---|
| **Unguided A2A Rocket Battery** | weapon | Basic Small Airframe (1936) | Early burst damage; ruins agility & defence |
| **Rocket Booster Pods** | small special | Basic Small Airframe (1936) | +50 km/h, drinks fuel, fragile |
| **Rotary Gatling Cannon** | weapon | Advanced Small Airframe + Cannon II | Late; huge air attack, heavy |
| **Guided A2A Missiles** | weapon | Advanced Small Airframe + Improved Rocket Engines | Endgame; the deadliest A2A weapon |
| **All-Guns Buzzsaw Nose** | weapon | Improved Small Airframe + HMGs | Mid; 50 air attack, turns like a freight train |
| **Drop-Tank Overload** | small special | Basic Small Airframe | +35% range, −4 defence: a flying fireball |
| **Armored Bathtub Cockpit** | small special | Basic Small Airframe | +6 defence, slower and heavier |
| **Pulsejet Booster** | small special | Rocket Engines | +80 km/h of droning terror |
| **Parasite Fighter Cradle** | large special | Improved Large Airframe | Bombers carry their own escort (+18 air attack) |

### Tanks (No Step Back)
| Module | Slot | Unlocks with | Character |
|---|---|---|---|
| **Hull Rocket Rack** | special | Basic Medium Tank (1939) | Early soft-attack barrage, −20% reliability |
| **Boiler-Plate Applique** | special | Basic Medium Tank (1939) | Dirt-cheap armor, −15% reliability, slower |
| **Reactive Armor Blocks** | special | Advanced Medium Tank (1943) | +12 armor — armor skirts' big sibling |
| **Mechanical Autoloader** | special | Main Battle Tank | Endgame; +10% attacks, +6 breakthrough |
| **Governor Removal** | special | Basic Medium Tank | +20% speed, −25% reliability, nearly free |
| **Concrete Cladding** | special | Basic Medium Tank | +8 armor that is technically armor |
| **Reinforced Ram Prow** | special | Basic Medium Tank | +8 breakthrough; the vehicle is the weapon |
| **Sprint Rocket Boosters** | special | Basic Medium Tank + Rocket Engines | +30% speed, −30% reliability |

### Ships (Man the Guns)
| Module | Slot | Unlocks with | Character |
|---|---|---|---|
| **Overpressured Boilers** | destroyer engine | game start | +25% speed, gluttonous fuel use |
| **Guided Anti-Ship Missiles** | torpedo slots (DD/CL) | Improved Rocket Engines | Endgame; massive accurate torpedo attack |
| **Naval SAM Battery** | anti-air slots | Improved Rocket Engines | Endgame fleet air defence |
| **Torpedo Broadside Racks** | torpedo slots | game start | Cheap massive salvo, −5% hit chance |
| **Deck-Mounted Field Artillery** | light battery slots | game start | Army guns at sea; the navy is appalled |
| **Depth Charge Carpet Launcher** | depth charge slot | game start | Saturation ASW |

## How unlocking works

No new research-tree entries (so no layout conflicts with Road to 56 or
anything else). Hidden technologies grant each module automatically the
moment you finish the gating vanilla research — e.g. finish **Advanced
Small Airframe** with **Improved Rocket Engines** and guided missiles just
appear in the designer. Works mid-save: already-researched gates are
detected on load.

## Tuning

All numbers live in `common/units/equipment/modules/ocr_*_modules.txt`;
gating requirements in `common/scripted_effects/ocr_modules_effects.txt`.

## Installation

From the repo root: `.\install.ps1 -Mod designer_modules_plus` (Windows) or
`./install.sh designer_modules_plus` (Linux/macOS). Safe to add mid-save.
