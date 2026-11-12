#!/bin/sh
# Checks that make this skill loadable and whole. Repository only; not shipped.
#
# Usage: ./lint.sh
set -eu

cd "$(dirname "$0")"

SKILL="symposium-curate-data"
SHIPPED="SKILL.md reference"
fail=0

say() { printf '%s\n' "$*" >&2; }
bad() { say "FAIL: $*"; fail=1; }

# Every file that ships, as a newline-separated list of paths relative to here.
shipped_files() {
	find $SHIPPED -type f | LC_ALL=C sort
}

is_shipped() {
	case " $(shipped_files | tr '\n' ' ') " in
	*" $1 "*) return 0 ;;
	*) return 1 ;;
	esac
}

# ---------------------------------------------------------------- frontmatter

if [ "$(head -n 1 SKILL.md)" != "---" ]; then
	bad "SKILL.md does not open with a frontmatter fence"
else
	fm=$(awk 'NR>1 && /^---$/ {exit} NR>1 {print}' SKILL.md)
	printf '%s\n' "$fm" | grep -q '^name:[[:space:]]*[^[:space:]]' ||
		bad "SKILL.md frontmatter has no name"
	printf '%s\n' "$fm" | grep -q '^description:[[:space:]]*[^[:space:]]' ||
		bad "SKILL.md frontmatter has no description"
	name=$(printf '%s\n' "$fm" | sed -n 's/^name:[[:space:]]*//p')
	[ "$name" = "$SKILL" ] ||
		bad "SKILL.md frontmatter name is '$name', expected '$SKILL'"
fi

# ----------------------------------------------------------------- the links
#
# A shipped document links only to shipped documents: README.md and REHEARSAL.md
# live in this folder and stay out of the zip, so a link to one of them from
# SKILL.md resolves here and dangles for everyone who installed the release.

for doc in $(find . -name '*.md' -not -path './dist/*' | sed 's|^\./||' | LC_ALL=C sort); do
	dir=$(dirname "$doc")
	# Markdown inline links, minus absolute URLs and pure anchors.
	targets=$(sed -n 's/.*](\([^)#][^)]*\)).*/\1/p' "$doc" |
		grep -v '^[a-z][a-z0-9+.-]*://' || true)
	for t in $targets; do
		t=${t%%#*}
		[ -n "$t" ] || continue
		case "$t" in
		/*) bad "$doc links to an absolute path: $t" ; continue ;;
		esac
		resolved=$(cd "$dir" && readlink -f "$t" 2>/dev/null || true)
		here=$(pwd -P)
		repo=$(cd .. && pwd -P)
		if [ -z "$resolved" ] || [ ! -e "$resolved" ]; then
			bad "$doc links to a file that does not exist: $t"
			continue
		fi
		if is_shipped "$doc"; then
			# A shipped document reaches only shipped documents: anything
			# else resolves here and dangles for whoever installed the zip.
			case "$resolved" in
			"$here"/*) rel=${resolved#"$here"/} ;;
			*) bad "$doc ships, and links outside the skill folder: $t" ; continue ;;
			esac
			is_shipped "$rel" ||
				bad "$doc ships, and links to $rel, which does not"
		else
			# A repository-only document may reach anywhere in the repository.
			case "$resolved" in
			"$repo"/*) ;;
			*) bad "$doc links outside the repository: $t" ;;
			esac
		fi
	done
done

# ------------------------------------------------- no reach into another skill
#
# Shipped prose reaches Symposium by saying what it is doing, in the record's
# own vocabulary, and lets Symposium's documents route from there. Two things
# break that: a path into Symposium's folder, which freezes a layout this
# repository does not own, and an instruction to use the Symposium skill by
# name, which couples to a skill rather than to the work. The install message
# is the one place the skill is named, and it is named to the user.

foreign_paths='toolchain/|~/\.claude/skills|\.claude/skills/|~/\.symposium/'
by_name='[Ss]ymposium skill'
install_section='## Before you start'

for doc in $(shipped_files | grep '\.md$'); do
	hits=$(grep -nE "$foreign_paths" "$doc" || true)
	[ -z "$hits" ] || {
		bad "$doc ships, and holds a path into another skill:"
		printf '%s\n' "$hits" | sed 's/^/        /' >&2
	}

	# The skill may be named in its own section, which tells the user to
	# install it. Anywhere else is an instruction to the agent.
	named=$(awk -v pat="$by_name" -v sec="$install_section" '
		/^## / { inside = (index($0, sec) == 1) }
		!inside && $0 ~ pat { printf "%d:%s\n", NR, $0 }
	' "$doc")
	[ -z "$named" ] || {
		bad "$doc ships, and names the Symposium skill outside the install section:"
		printf '%s\n' "$named" | sed 's/^/        /' >&2
	}
done

# -------------------------------------------------------------- no orphans

for ref in reference/*.md; do
	grep -q "$ref" SKILL.md || bad "$ref is not linked from SKILL.md"
done

# ---------------------------------------------------------------------- done

[ "$fail" -eq 0 ] || exit 1
say "lint: frontmatter, foreign references, links, orphans"
