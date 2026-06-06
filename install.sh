#!/usr/bin/env bash
# Installs the HOI4 mods in this repo into your local Hearts of Iron IV mod
# folder, generating the launcher pointer (.mod) files automatically.
#
# Usage:
#   ./install.sh                          # install every mod in ./mods
#   ./install.sh usa_presidential_cabinet # install just that mod
#
# (Windows users: use install.ps1 instead.)

set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mods_src="$repo/mods"
target_mod="${1:-}"

if [ ! -d "$mods_src" ]; then
	echo "Could not find a 'mods' folder next to this script ($mods_src)." >&2
	exit 1
fi

case "$(uname -s)" in
	Darwin) hoi_dir="$HOME/Documents/Paradox Interactive/Hearts of Iron IV/mod" ;;
	*)      hoi_dir="$HOME/.local/share/Paradox Interactive/Hearts of Iron IV/mod" ;;
esac

mkdir -p "$hoi_dir"

found=0
for dir in "$mods_src"/*/; do
	name="$(basename "$dir")"
	if [ -n "$target_mod" ] && [ "$target_mod" != "$name" ]; then
		continue
	fi
	found=1

	rm -rf "$hoi_dir/$name"
	cp -R "$dir" "$hoi_dir/$name"

	if [ -f "$mods_src/$name.mod" ]; then
		cp -f "$mods_src/$name.mod" "$hoi_dir/$name.mod"
	else
		# Generate a pointer from the mod's descriptor.mod.
		{ cat "$dir/descriptor.mod"; printf '\npath="mod/%s"\n' "$name"; } > "$hoi_dir/$name.mod"
	fi

	echo "Installed '$name'"
	echo "    files   -> $hoi_dir/$name"
	echo "    pointer -> $hoi_dir/$name.mod"
done

if [ "$found" -eq 0 ]; then
	echo "No mod folder named '$target_mod' under ./mods." >&2
	echo "Available: $(ls -1 "$mods_src" | tr '\n' ' ')" >&2
	exit 1
fi

echo ""
echo "Done. Open the HOI4 launcher, refresh mods, add them to a Playset,"
echo "and (for the USA cabinet mod) put Road to 56 ABOVE it in the load order."
