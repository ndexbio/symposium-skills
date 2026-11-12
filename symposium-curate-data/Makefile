# symposium-curate-data — lint <- build
#
#   make lint    frontmatter, foreign references, links, orphans
#   make build   lint, then the release zip
#
# The version lives in the release tag and nowhere else, so there is nothing
# here to keep in step with it.

SKILL   := symposium-curate-data
ZIP     := dist/$(SKILL)_skill.zip
STAGE   := dist/stage
SHIPPED := SKILL.md reference
EPOCH   := 198001010000

.PHONY: lint build clean

lint:
	@./lint.sh

build: lint
	@rm -rf $(STAGE) $(ZIP)
	@mkdir -p $(STAGE)/$(SKILL)
	@for p in $(SHIPPED); do cp -R "$$p" $(STAGE)/$(SKILL)/; done
	@find $(STAGE) -exec touch -t $(EPOCH) {} +
	@cd $(STAGE) && find . -type f | LC_ALL=C sort | sed 's|^\./||' | \
		zip -X -q ../$(SKILL)_skill.zip -@
	@unzip -Z1 $(ZIP) | LC_ALL=C sort > $(STAGE)/.got
	@cd $(STAGE) && find $(SKILL) -type f | LC_ALL=C sort > .want
	@diff -u $(STAGE)/.want $(STAGE)/.got >/dev/null || { \
		echo "FAIL: the zip does not hold exactly the shipped set" >&2; \
		diff -u $(STAGE)/.want $(STAGE)/.got >&2; exit 1; }
	@rm -rf $(STAGE)
	@echo "build: $(ZIP)"

clean:
	@rm -rf dist
