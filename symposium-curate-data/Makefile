# symposium-curate-data — lint ← build
#
#   make lint                  frontmatter, foreign references, links, orphans
#   make build                 lint, then dist/<skill>_skill-0.0.0-dev.zip
#   make build VERSION=0.1.0   dist/<skill>_skill-0.1.0.zip, stamped 0.1.0 — what release.yml
#                              passes from the tag
#   make deploy-local          build, then install the skill from the zip into $(SKILLS)
#   make deploy-local SKILLS=<dir>   the same, into another skills directory
#
# The zip holds one folder, <skill>/: SKILL.md, README.md, LICENSE and reference/. The version
# lives in the release tag; it names the zip, and the copy in SKILL.md's frontmatter
# (metadata.version) is written here, from VERSION.

SKILL   := symposium-curate-data
VERSION ?= 0.0.0-dev
ZIP     := dist/$(SKILL)_skill-$(VERSION).zip
SKILLS  ?= $(HOME)/.claude/skills

.PHONY: lint build deploy-local clean

lint:
	@./lint.sh

build: lint
	@rm -rf dist && mkdir -p dist/$(SKILL)
	@cp -R reference dist/$(SKILL)/
	@cp README.md ../LICENSE dist/$(SKILL)/
	@awk -v v='$(VERSION)' '/^---$$/ { fence++ } fence == 1 && /^  version:/ { print "  version: \"" v "\""; next } { print }' \
		SKILL.md > dist/$(SKILL)/SKILL.md
	@cd dist && zip -qr $(SKILL)_skill-$(VERSION).zip $(SKILL) && rm -rf $(SKILL)
	@echo "build: $(ZIP) ($(VERSION))"

# Installs from the built zip, not the working copy, so what runs locally is what ships. It
# removes before extracting, so a file dropped from the zip does not live on in the install.
# The build's checks print only when one fails, and then nothing is installed.
deploy-local:
	@test -n "$(SKILLS)" || { echo "deploy-local: SKILLS is empty; refusing"; exit 1; }
	@log=$$(mktemp) && trap 'rm -f "$$log"' EXIT && \
		$(MAKE) --no-print-directory build VERSION=$(VERSION) > "$$log" 2>&1 || \
		{ cat "$$log"; echo "deploy-local: the checks failed; the skill was not installed"; exit 1; }
	@staging=$$(mktemp -d) && trap 'rm -rf "$$staging"' EXIT && \
		python3 -m zipfile -e $(ZIP) "$$staging" && \
		rm -rf "$(SKILLS)/$(SKILL)" && \
		mkdir -p "$(SKILLS)" && \
		mv "$$staging/$(SKILL)" "$(SKILLS)/$(SKILL)"
	@echo "$(SKILL) skill installed in $(SKILLS)/$(SKILL) ($(VERSION))"

clean:
	@rm -rf dist
