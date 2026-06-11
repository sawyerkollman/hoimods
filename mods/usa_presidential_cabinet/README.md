# Wings of the Eagle — Presidential Cabinet USA Overhaul (HOI4) v0.3.0

A complete 1936–1956 national focus tree for the United States in Hearts of Iron IV that replaces the vanilla US tree with a **186-focus** "Wings of the Eagle" layout — a cabinet-and-elections trunk down the center, four ideology wings fanning outward, and one shared military pillar that all paths share.

## Wings at a Glance

### Democratic Wing
Historical Roosevelt → Truman → Eisenhower/Stevenson spine, gated on cabinet appointments and era flags.

- **1936–44:** New Deal legislation, Hull's foreign policy ladder (Cash-and-Carry → Destroyers for Bases → Lend-Lease), and the wartime mobilization arc (WPB, OSRD, Tehran, Yalta)
- **1945–48:** Bretton Woods, the United Nations, the Truman Doctrine, and Marshall Plan as separate focuses
- **1949–52:** NATO, NSC-68 rearmament, Korea, and the managed Red Scare (gated on the AG's civil-libertarian flag)
- **1953–56:** New Look strategy, Atoms for Peace, the St. Lawrence Seaway, and the Interstate Highway capstone

### Republican Wing
America First isolationism vs. Eastern Establishment internationalism — the player's fork at "Dewey for President" (1944).

- **Isolationist line:** America First → Neutrality Acts with Teeth → Fortress America → Armed Neutrality; gated on the isolationist State seat flag
- **Taft postwar:** Mr. Republican → Fortress Doctrine → Bring the Boys Home → Hemisphere Imperium → McCarthy Unleashed (gated on security-hawk AG flag)
- **Establishment postwar:** Eastern Establishment → Vandenberg Moment → Draft Eisenhower → Dynamic Conservatism → McCarthy Censured
- **Shared gate:** both postwar lines feed into Rollback vs. Containment, reflecting the 1952 foreign-policy debate

### Radical Wing
Share Our Wealth / Popular Front → Workers' Democracy vs. Vanguard — two mutually exclusive capstones.

- **Opening arc:** Voices of Discontent → fork to Long's SOW or CPUSA Popular Front → Sit-Down Wave → Labor Bill of Rights
- **Mid-game:** Radical Commitment → seizure of government → Third Camp neutrality or Comintern pivot
- **Democratic path:** Workers' Parliament → Economic Democracy → Red Half-Century (democratic)
- **Vanguard path:** Smash the Reaction → Comintern Pivot → Atomic Secrets Shared → Red Half-Century (vanguard)

### Authoritarian Wing
Business Plot / Silver Legion → Pax Americana → Imperium — Caesar's ascent.

- **Rise:** Business Plot → Silver Legion Rises → Crush Labor; press control and loyalty oaths gated on security-hawk AG
- **Consolidation:** New Order at Home (surveillance state), Hemisphere Destiny, Tribune of the People
- **Expansion:** Pax Americana → Tribute System → Legions Overseas; Atomic Diplomacy gated on War Department loyalist
- **Endgame:** The Imperium (ideology locked to fascism) + The Succession Question flavor capstone

### Military Pillar (shared by all wings)
All ideologies can take this pillar; no wing prerequisite.

- **Industry:** War Resources Board (gated on war-loyalist War Dept.) → Synthetic Rubber → Willow Run → Liberty Fleet
- **Navy:** Two-Ocean Navy → Carrier Doctrine → Essex Program → Fleet Train
- **Air:** Air Corps Expansion → Very Long Range → Strategic Air Command → Jet Transition → Century Series
- **Atomic:** Uranium Committee → Manhattan Project → Trinity → The Super → Atoms Underwater
- **Korea-era:** Rotation System → Helicopter Age → Continental Defense

## Cabinet System

Five election focuses act as chapter breaks: **1936, 1940, 1944, 1948, 1952**. Each election fires a campaign event and sets an era flag (`USA_era_1940`, etc.) that gates later focuses. After each election the player assembles (or reassembles) **four cabinet seats**:

| Seat | Progressive / Internationalist pick | Conservative / Hawk pick |
|------|--------------------------------------|--------------------------|
| Secretary of State | Cordell Hull / Stettinius / Byrnes | Isolationist appointee / Taftman |
| Secretary of the Treasury | Henry Morgenthau / Vinson / Snyder | Business Treasury / Banker |
| Secretary of War / Defense | Henry Stimson / Forrestal / Wilson | Harry Woodring / MacArthur |
| Attorney General | Frank Murphy / Clark / Brownell | Security Hawk / McGrath appointee |

Each appointment sets a **country flag** (`USA_cab_state_internationalist`, `USA_cab_state_isolationist`, `USA_cab_war_loyalist`, `USA_cab_ag_civil_libertarian`, `USA_cab_ag_security_hawk`). Those flags gate 25 later focuses across all five wings — a civil-libertarian AG is required to manage the Red Scare, an internationalist State Department is required to reach Bretton Woods and NATO, a war-loyalist Defense secretary is required to pursue NSC-68 and Atomic Diplomacy.

Cabinet appointments also track a **Progressive ⟷ Old Guard power balance** (`USA_cabinet_power_balance`) and fill `USA_cabinet_seats_filled`, which the 1936 election focus reads before unlocking the wing anchors.

## Requirements

- **Hearts of Iron IV** (tested against current Paradox launcher)
- **Road to 56** — place this mod **above** Road to 56 in your playset load order so R56 loads first

The mod will load without R56, but the extended Cold War tech trees (jet aircraft, nuclear doctrine, late electronics) will be absent.

## Installation

### Linux / macOS
From the repository root:
```bash
./install.sh usa_presidential_cabinet
```
This copies the mod folder and writes the launcher pointer file to your HOI4 mod directory.

### Windows
```powershell
.\install.ps1 usa_presidential_cabinet
```

### Manual
Copy both of these from `mods/` into your HOI4 mod directory
(`Documents\Paradox Interactive\Hearts of Iron IV\mod\`):
- the `usa_presidential_cabinet/` folder
- the `usa_presidential_cabinet.mod` pointer file

Then enable both Road to 56 and this mod in a Playset, with Road to 56 above this mod.
