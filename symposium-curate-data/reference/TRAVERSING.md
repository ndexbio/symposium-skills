# Traversing

How to expand one hop from the origins, and what "one hop" means operationally.

You arrive here with the origins from [searching](SEARCHING.md). You leave with the corpus: the
origins plus everything one hop reached that earned its place, up to Max Sources.

## Three directions

Most people traverse one. Run all three — they find different things.

**Backward**, into an origin's reference list. These are the foundations it rests on: older,
better vetted, and often the source of the measurement an origin merely cites. When a hypothesis
turns on a value somebody established twenty years ago, this is the direction that finds the paper
that established it.

**Forward**, into the works citing an origin. This is what happened since — the replications, the
extensions, and the refutations. An origin from 2019 with forty citations has had its claim tested
by some of them, and those are among the most valuable works in the corpus.

**Sideways**, through co-citation: the works that keep appearing alongside the origins in other
people's reference lists. This is the direction most often skipped, and it is frequently the
richest, because it is the field's own clustering rather than yours. **Two works co-cited by many
others are related whether or not either cites the other** — which is how you find the parallel
literature that uses different vocabulary for the same thing, the one a facet query will never
reach.

## The threshold is what makes the hop one hop

Score everything the three directions reach against the same facets used for the origins, and
**keep what scores at or above the lowest-scoring origin.**

Citation adjacency is necessary rather than sufficient. A paper your origin cited in passing for a
reagent is adjacent and irrelevant. Without that threshold, "one hop" means "everything these
papers touched", which for ten origins is several thousand works and no corpus at all.

## Weigh where a reference is cited

Where full text is open, look at **where** in the citing paper a reference appears. It is a strong
signal and it costs one read.

A reference cited in **Methods or Results** — as the source of a protocol, a reagent, a comparison
value, a threshold — is doing real work in that paper, and is very often the source of a datum
this corpus wants. A reference cited once in the **introduction** is furniture: it establishes
that the field exists.

When the hop returns more than the budget allows, this is the better way to choose.

## Reviews are bridges, not destinations

A review's reference list is a bibliography an expert already curated for exactly this topic,
which makes it the highest-yield traversal input available. **Harvest its references hard** — more
thoroughly than any primary paper's.

The review itself is a secondary source: it reports other people's findings rather than making
measurements. Keep it, mark it as a review, and expect what it contributes to the record to come
from its reasoning rather than from preserved passages of its results.

## Hubs override the threshold, once

A work cited by several of the origins is a landmark the field treats as foundational, even when
its own facet score is middling — it is often older and broader, and its abstract uses the
vocabulary of its own decade.

**Count in-degree inside the origin set.** It is cheap, and a work cited by three or more origins
earns its place whatever it scored. This is the one principled exception to the threshold; make no
others, or the threshold stops meaning anything.

## Know when to stop

**Saturation is a result.** When the hop returns mostly works you already hold, the field around
this hypothesis is covered. Say so — it is evidence the corpus is complete, and it is the most
reassuring thing a user can hear about a literature search.

**The opposite is also a result.** When the hop keeps returning new work scoring above the
threshold after Max Sources is reached, the budget is too small for the question. Tell the user,
with how much is being left behind, so they can raise it or accept a sample knowingly. Silent
truncation at the budget hands them a corpus that looks complete and is not.

## One hop means one

The frontier of a frontier is the literature. Relevance decays across a hop while volume
multiplies, so a second hop buys a great deal of noise for a little signal.

Where coverage comes up short, the answer is **a higher Max Origins**, not another hop. More
starting points reach more of the literature at the same relevance; another hop reaches further at
worse relevance. Take that back to the user as a question rather than deciding it.

---

Next: [access](ACCESS.md), which resolves each source to something you can actually read.
