# symposium-curate-data — lint <- build
#
#   make lint                          frontmatter, links, orphans, VERSION
#   make build                         lint, then the release zip
#   make build RELEASE_VERSION=1.0.0   also check VERSION matches

SKILL   := symposium-curate-data
ZIP     := dist/$(SKILL)_skill.zip
STAGE   := dist/stage
SHIPPED := SKILL.md VERSION reference
EPOCH   := 198001010000

RELEASE_VERSION ?=

.PHONY: lint build clean

lint:
	@./lint.sh $(RELEASE_VERSION)

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
