#!/usr/bin/env python3
"""Stop a session under test as soon as it goes wrong, instead of when its turn ends.

    watch.py --events <turn.jsonl> [--pid <claude pid>] --model <model id>
             --community <name>[,<name>...] [--approved <flag file>]
             [--forbid <path>[,<path>...]] [--max-usd 10] [--max-minutes 90]
             [--abort-file <path>] [--replay]

Reads the event stream a headless session writes (`claude -p --output-format stream-json
--verbose`) as it grows. When a tripwire fires it writes the reason to the abort file, stops the
session with SIGINT (SIGTERM five seconds later if it is still running), and exits 2. It exits 0
when the session ends with nothing tripped. `--replay` reads a finished stream and reports what
would have tripped, without stopping anything.

The tripwires are faults a person would stop the run for at once:

  model      the session runs on a model other than --model
  leak       a command reads or writes a --forbid path: the fixture, the answers, the repository
  publish    something is published or stored before the --approved flag file exists
  community  a command names a user context outside --community
  loop       the same tool error four times in a row
  cost       the estimated spend of this turn passes --max-usd. The estimate is made from the
             token counts in the stream and reads low: about half of what the CLI reports
             when the turn ends. Set the ceiling at about half the real limit.
  time       the turn runs past --max-minutes

It judges no science: that is read at each stop. Needs only the standard library.
"""

import argparse
import json
import os
import re
import signal
import sys
import time

# USD per million tokens: input, output, cache read, cache write (one-hour writes, 2x input).
PRICES = {
    "claude-sonnet-5-5": (2.00, 10.00, 0.10, 4.00),
    "claude-opus-5-5": (4.00, 20.00, 0.20, 8.00),
    "claude-fable-5-2": (8.00, 40.00, 0.20, 16.00),
    "claude-haiku-5-5": (0.10, 0.50, 0.01, 0.20),
}
PUBLISH = re.compile(r"(scripts/main\.py|/symposium)\s+(publish(?!\s+--roles)|data\s+put)\b")
CONTEXT = re.compile(r"--user-context[ =]+['\"]?([A-Za-z0-9_\-]+)(?:/[A-Za-z0-9_\-]+)?")


class Trip(Exception):
    pass


class Watch:
    def __init__(self, a):
        self.a = a
        self.forbid = [os.path.expanduser(p) for p in (a.forbid or "").split(",") if p]
        self.communities = {c for c in a.community.split(",") if c}
        self.usage = {}  # message id -> usage of its last event
        self.models = set()
        self.last_error, self.error_run = None, 0
        self.started = time.time()

    def cost(self):
        total = 0.0
        for model, u in self.usage.values():
            p = PRICES.get(model) or PRICES.get(self.a.model) or PRICES["claude-opus-5-5"]
            total += (u.get("input_tokens", 0) * p[0] + u.get("output_tokens", 0) * p[1]
                      + u.get("cache_read_input_tokens", 0) * p[2]
                      + u.get("cache_creation_input_tokens", 0) * p[3]) / 1e6
        return total

    def event(self, o):
        kind = o.get("type")
        if kind == "system" and o.get("subtype") == "init" and o.get("model") != self.a.model:
            raise Trip(f"model: the session runs on {o.get('model')}, not {self.a.model}")
        if kind == "assistant":
            m = o.get("message") or {}
            if m.get("id") and m.get("usage"):
                self.usage[m["id"]] = (m.get("model"), m["usage"])
            for c in m.get("content") or []:
                if c.get("type") == "tool_use":
                    self.tool(json.dumps(c.get("input"), ensure_ascii=False))
        if kind == "user":
            for c in (o.get("message") or {}).get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_result":
                    text = c.get("content")
                    text = json.dumps(text)[:300] if not isinstance(text, str) else text[:300]
                    if c.get("is_error"):
                        self.error_run = self.error_run + 1 if text == self.last_error else 1
                        self.last_error = text
                        if self.error_run >= 4:
                            raise Trip(f"loop: the same tool error four times in a row: {text[:160]}")
                    else:
                        self.last_error, self.error_run = None, 0
        if self.cost() > self.a.max_usd:
            raise Trip(f"cost: this turn's estimated spend passed ${self.a.max_usd:.0f} (${self.cost():.2f})")
        if not self.a.replay and time.time() - self.started > self.a.max_minutes * 60:
            raise Trip(f"time: the turn ran past {self.a.max_minutes} minutes")

    def tool(self, text):
        for p in self.forbid:
            if p and p in text:
                raise Trip(f"leak: a command touches {p}")
        if PUBLISH.search(text) and not (self.a.approved and os.path.exists(self.a.approved)):
            raise Trip(f"publish: something is published or stored before approval: {PUBLISH.search(text).group(0)}")
        for name in CONTEXT.findall(text):
            if name not in self.communities and not name.startswith("qametab"):
                raise Trip(f"community: a command names the user context of {name}, outside {sorted(self.communities)}")


def lines(path, follow, alive):
    while not os.path.exists(path):
        if not follow or not alive():
            return
        time.sleep(1)
    with open(path, encoding="utf-8") as f:
        buf = ""
        while True:
            chunk = f.readline()
            if chunk:
                buf += chunk
                if buf.endswith("\n"):
                    yield buf
                    buf = ""
                continue
            if not follow or not alive():
                return
            time.sleep(2)


def stop(pid):
    for sig, wait in ((signal.SIGINT, 5), (signal.SIGTERM, 0)):
        try:
            os.kill(pid, sig)
        except ProcessLookupError:
            return
        for _ in range(wait):
            time.sleep(1)
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", required=True)
    ap.add_argument("--pid", type=int)
    ap.add_argument("--model", required=True)
    ap.add_argument("--community", required=True)
    ap.add_argument("--approved")
    ap.add_argument("--forbid")
    ap.add_argument("--max-usd", type=float, default=10.0)
    ap.add_argument("--max-minutes", type=float, default=90.0)
    ap.add_argument("--abort-file")
    ap.add_argument("--replay", action="store_true")
    a = ap.parse_args()
    w = Watch(a)

    def alive():
        if not a.pid:
            return False
        try:
            os.kill(a.pid, 0)
            return True
        except ProcessLookupError:
            return False

    try:
        for line in lines(a.events, follow=not a.replay, alive=alive):
            try:
                o = json.loads(line)
            except ValueError:
                continue
            w.event(o)
    except Trip as t:
        msg = f"STOPPED: {t}" if not a.replay else f"WOULD STOP: {t}"
        print(msg)
        if a.abort_file:
            with open(a.abort_file, "w", encoding="utf-8") as f:
                f.write(msg + "\n")
        if a.pid and not a.replay:
            stop(a.pid)
        sys.exit(2)
    print(f"clean: no tripwire (estimated spend ${w.cost():.2f})")


if __name__ == "__main__":
    main()
