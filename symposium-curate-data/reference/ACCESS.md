# Access

Paywalls, login walls, and what each one costs the corpus.

You arrive here with the corpus from [traversal](TRAVERSING.md). You leave with each source
carrying a **status**, a **note**, and the location that answered.

## Settle access before curation, in one pass

A wall discovered halfway through publishing strands the run. The same wall discovered here is
just a property of a source — one the user can act on when the review table reaches them.

The pass is cheap: a metadata lookup, and at most a head request per source. Do it for every
source before fetching anything in bulk.

## The ladder

Six rungs. The first four are alternative routes to the same document, so take the first that
answers. The fifth is a different object and is worth checking **even when the first rung
answered**. The sixth is what you are left holding.

**1. The publisher's open full text.** Where the index says the work is open, it names the licence
too. Record both.

**2. The PMC or Europe PMC mirror.** Frequently open where the publisher is closed, and often the
*better* copy: structured JATS rather than publisher HTML, and structure is what makes passages
and tables extractable later.

**3. The preprint** — bioRxiv, medRxiv, arXiv. The same work in an earlier version, which makes
this the one rung that changes what you hold. A preprint's numbers can differ from the version of
record, and a quotation taken from a preprint is a quotation from that preprint. Record which
version the source holds.

**4. An author-deposited copy** in an institutional repository. The open-access indexes list
these; they are lawful copies the authors put there themselves.

**5. The deposited data.** Often open while the article is closed, and frequently what the corpus
actually needed — the measurements rather than the prose about them. **A closed article is no
reason to skip its data availability statement.** Check this rung for every source.

**6. The abstract and metadata.** Enough to make a publication artifact and nothing more.

## Triage: what came back, and what it means

| What you got | What it is | What to do |
|---|---|---|
| `402` or `403` with a publisher landing page | closed access | next rung |
| `200` with a sign-in form or an "institutional access" interstitial | account required | next rung |
| `302` to a login or SSO host | account required | next rung |
| `429`, or a `Retry-After` header | rate limited — the one temporary failure here | back off, honour the header, try again |
| `503`, a bot-mitigation interstitial, a captcha | the host is declining automated requests | leave that host alone, next rung |
| a `robots.txt` exclusion covering the path | the host has asked you not to | next rung, or the host's own API |
| `404` on a DOI | link rot | re-resolve through the DOI resolver and look for a replacement |
| a PDF with no text layer | retrievable, not yet quotable | a rendering question for [taking](TAKING.md), not an access one |

## The `200` is the trap

A login wall returns a complete, valid HTML page. **A fetch that succeeded is not a document that
arrived.**

Before treating a body as an article, check that it carries what an article carries: sections, a
Methods or Results heading, a length consistent with what the abstract promised. A short body
containing "sign in", "purchase", "get access" or "institutional login" is a wall, whatever its
status code said.

Publishing a paywall page as a preserved passage is the worst outcome in this document, because it
is wrong in a way the gate cannot see: the quote verifies, the hash is real, and the record now
holds a publisher's advertisement presented as a scientific finding.

## The line

This skill reaches sources the way any reader without a subscription does. It uses the open
copy, the mirror, the preprint, the author's deposit, the data, or the abstract — and where a host
has asked automated clients to stay away, it stays away.

Credentials, institutional proxies, shared accounts and ways around bot mitigation are outside
what it does, and automating someone's authenticated session is outside it too.

Where lawful access exists, it belongs to the user. The [review table](CURATING.md#the-review-loop)
shows them which sources are closed and what each would contribute, and they can add a document
they obtained through their own means. That is the escalation, and it is theirs to take.

## What each source leaves with

**A status.** Three of them describe what arrived:

- **retrieved** — a document you can extract from
- **abstract** — only the abstract and metadata came back
- **failed** — no rung answered

A fourth, **citation only**, is a decision rather than a result: the review loop sets it when the
user keeps a source that could not be retrieved.

**A note**, composed from facts rather than written freely, so that forty of them stay scannable
down a column. It says:

- which rung answered
- whether the content is **structured full text or a flat PDF** — structure is what makes passages
  and tables extractable, so this is the most useful thing in the note
- whether it carries tables
- the version, where it is not the version of record

A failure's note names its wall: closed, account required, host declined, link rot.

## What a citation-only source becomes

A `ScientificPublication` carrying its canonical location, its metadata, and a plain statement of
why it could not be retrieved. It is citable — other artifacts can address it, and the record
shows it was considered — and nothing grounds on it.

It yields no Argument either. An abstract is the authors' summary of their own work, which
Symposium's extraction SOP is explicit about declining as a basis for extraction. So a
citation-only source yields a publication and waits, rather than an Argument assembled from
metadata. Where the hypothesis turns on one of them, that is a finding about the corpus, and the
user hears it.

---

Next: [curating](CURATING.md), which resolves identity and puts the corpus to the user.
