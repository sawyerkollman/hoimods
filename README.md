# hoimods

A collection of mods for **Hearts of Iron IV**. Each mod lives in its own
self-contained folder under [`mods/`](mods/), so this single repo can hold
several independent mods.

## Mods in this repo

| Mod | Folder | Summary |
|-----|--------|---------|
| **Presidential Cabinet — A USA Overhaul** | [`mods/usa_presidential_cabinet`](mods/usa_presidential_cabinet) | Standalone US focus tree with a Götterdämmerung-style inner-circle cabinet and a layered historical / alt-history spine beyond 1942. Road to 56 submod. |
| **More Dockyards Per Ship — Naval Blitz** | [`mods/more_dockyards_per_line`](mods/more_dockyards_per_line) | Raises the per-line naval dockyard caps (capital 5→50, screens/subs 10→50, convoys 15→50) so you can mass-produce a fleet. Standalone defines override. |

See each mod's own `README.md` for its features, requirements, and design notes.

## Installing

### Windows (recommended)

From the repo root, in PowerShell:

```powershell
# install every mod in the repo
powershell -ExecutionPolicy Bypass -File .\install.ps1

# or just one
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Mod usa_presidential_cabinet
```

The script copies the mod folder(s) into
`Documents\Paradox Interactive\Hearts of Iron IV\mod\` and writes the matching
launcher pointer (`.mod`) file next to each — then it shows up in the HOI4
launcher's mod list. (It honours OneDrive-redirected Documents folders.)

### macOS / Linux

```bash
./install.sh                          # all mods
./install.sh usa_presidential_cabinet # one mod
```

### Manual install

Copy, from this repo's `mods/` folder into your HOI4 `mod/` directory, **both**:

- the mod's folder (e.g. `usa_presidential_cabinet/`), and
- its sibling pointer file (e.g. `usa_presidential_cabinet.mod`).

The pointer's `path="mod/<folder>"` line is what the launcher reads to locate
the files. HOI4 mod directories:

| OS | Path |
|----|------|
| Windows | `Documents\Paradox Interactive\Hearts of Iron IV\mod\` |
| macOS | `~/Documents/Paradox Interactive/Hearts of Iron IV/mod/` |
| Linux | `~/.local/share/Paradox Interactive/Hearts of Iron IV/mod/` |

After installing, open the launcher, refresh the mod list, add the mod(s) to a
Playset, and mind any load-order notes in the individual mod's README.

## Repo layout

```
hoimods/
  install.ps1                         # Windows installer
  install.sh                          # macOS / Linux installer
  mods/
    usa_presidential_cabinet/         # <- a mod (its own folder)
      descriptor.mod                  #    Workshop/in-folder descriptor
      common/  events/  localisation/ #    the mod's content
      README.md                       #    that mod's documentation
    usa_presidential_cabinet.mod      # <- launcher pointer (path=mod/<folder>)
```

## Adding a new mod to this repo

The installer and layout are convention-based, so adding another mod is
mechanical:

1. Create a new folder under `mods/`, e.g. `mods/my_new_mod/`, and put the
   mod's content inside it (`descriptor.mod`, `common/`, `events/`,
   `localisation/`, etc.). Give `descriptor.mod` a unique `name="..."`.
2. Add a sibling pointer file `mods/my_new_mod.mod` — copy an existing one and
   change `name=` and the final `path="mod/my_new_mod"` line to match the
   folder. (Optional: if you skip this, the installer auto-generates the
   pointer from `descriptor.mod`.)
3. Run `install.ps1` / `install.sh` — the new mod is picked up automatically.
4. Add a row to the **Mods in this repo** table above.

Keep each mod's files entirely within its own folder so the mods stay
independent and never collide.

### Gotcha: localisation files must be UTF-8 **with BOM**

HOI4 `.yml` localisation files have to be saved as **UTF-8 with a byte-order
mark**. Without the BOM the game may load only part of the file and silently
drop entries — focus titles and some text show up while other descriptions
render blank. If you add or edit a `localisation/` file, make sure it keeps
the BOM (most editors call this "UTF-8 with BOM"; VS Code shows it in the
status bar as `UTF-8 with BOM`).
