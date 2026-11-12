# symposium-curate-data — lint ← build
#
#   make lint                  frontmatter, foreign references, links, orphans
#   make build                 lint, then the release zip, stamped 0.0.0-dev
#   make build VERSION=0.1.0   stamped 0.1.0 — what release.yml passes from the tag
#
# What ships is SKILL.md and reference/. The version lives in the release tag;
# the copy in SKILL.md's frontmatter is written here, from VERSION.

SKILL   := symposium-curate-data
ZIP     := dist/$(SKILL)_skill.zip
VERSION ?= 0.0.0-dev

.PHONY: lint build clean

lint:
	@./lint.sh

build: lint
	@rm -rf dist && mkdir -p dist/$(SKILL)
	@cp -R reference dist/$(SKILL)/
	@awk -v v='$(VERSION)' '/^---$$/ { fence++ } fence == 1 && /^version:/ { print "version: " v; next } { print }' \
		SKILL.md > dist/$(SKILL)/SKILL.md
	@cd dist && zip -qr $(SKILL)_skill.zip $(SKILL) && rm -rf $(SKILL)
	@echo "build: $(ZIP) ($(VERSION))"

clean:
	@rm -rf dist
