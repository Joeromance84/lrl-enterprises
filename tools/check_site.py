#!/usr/bin/env python3
"""check_site.py - claim and structure check for the LRL Enterprises page.

Exit 0 = clean, 1 = findings. Run before every push.
Checks wording mechanically. It cannot judge whether a claim is fair in
context - read the page too.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

# visible text only, footer disclaimer removed (it legitimately says "treat, cure")
body = re.sub(r"<footer>.*?</footer>", "", html, flags=re.S)
text = re.sub(r"<[^>]+>", " ", re.sub(r"<(style|head)>.*?</\1>", "", body, flags=re.S))
low = re.sub(r"\s+", " ", text).lower()

fails = []


def ck(label, ok, detail=""):
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label, ("  - " + detail) if detail else ""))
    if not ok:
        fails.append(label)


print("=== STRUCTURE ===")
ck("doctype", html.lstrip().startswith("<!DOCTYPE"))
ck("sections balanced", html.count("<section") == html.count("</section>"))
ck("divs balanced", html.count("<div") == html.count("</div>"))
ck("terminated", html.rstrip().endswith("</html>"))

print("\n=== DRUG / DISEASE CLAIMS (must be absent from page body) ===")
banned = [r"\bpain\b", r"inflammat", r"psoria", r"\bburns?\b", r"\bheal", r"\btreats?\b",
          r"\bcures?\b", r"analges", r"reverse[sd]? aging", r"reverses? the", r"joint",
          r"cognit", r"\bdermis\b", r"deep (?:into )?tissue", r"clinical study participant",
          r"most advanced", r"guarantee", r"validated", r"patent", r"fda[- ]approved",
          r"cleared", r"zero (?:side|adverse)", r"\bn ?= ?\d"]
hits = sorted({m.group(0) for p in banned for m in re.finditer(p, low)})
ck("no drug, disease or unverifiable claims", not hits, ", ".join(hits))

print("\n=== THINGS THAT MUST NOT BE PUBLISHED ===")
ck("EIN not on page", "42-4884112" not in html and "424884112" not in html)
ck("no clinical recruitment", not re.search(
    r"enroll(?:ment)? (?:now|today|in (?:a|our|the) (?:study|trial))"
    r"|participate in (?:a|our|the) (?:study|trial)|join (?:a|our|the) (?:study|trial)"
    r"|become a (?:study )?participant", low))

print("\n=== REQUIRED ===")
ck("cosmetic disclaimer", "not intended to diagnose, treat, cure or prevent any disease" in html)
ck("research not available", "not available to the public" in html)
ck("preclinical stated", "preclinical stage" in html)
ck("IND and IRB named before any study", "FDA IND and IRB approval" in html)
ck("SPF regulated-as-sunscreen note", "regulated by the FDA as a sunscreen" in html)
ck("biotech email", "LorentzBiotech@gmail.com" in html)
ck("cosmetics email", "LogansCosmetics@gmail.com" in html)

print("\nFAILURES: %d" % len(fails) if fails else "\nALL CHECKS PASS")
sys.exit(1 if fails else 0)
