"""Wait for the Pages build, then verify the live page, assets and QR decode."""
import io
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
U = "https://joeromance84.github.io/lrl-enterprises/"


def get(url):
    return urllib.request.urlopen(url, timeout=25).read()


for _ in range(24):
    try:
        if b"Lorentz Biotechnologies" in get(U):
            break
    except Exception:
        pass
    time.sleep(15)

ok = True
for p in ("", "assets/qr-code.png", "assets/qr-code.svg"):
    try:
        b = get(U + p)
        print("  [200] %-20s %d bytes" % (p or "(page)", len(b)))
    except Exception as e:
        ok = False
        print("  [FAIL] %s %s" % (p, e))

page = get(U).decode("utf-8", "replace")
for label, cond in (
    ("both brands present", "Lorentz Biotechnologies" in page and "Logan's Cosmetics" in page),
    ("preclinical stated", "preclinical stage" in page),
    ("no EIN", "42-4884112" not in page),
    ("biotech email", "LorentzBiotech@gmail.com" in page),
    ("cosmetics email", "LogansCosmetics@gmail.com" in page),
):
    ok &= cond
    print("  [%s] %s" % ("PASS" if cond else "FAIL", label))

try:
    import cv2
    import numpy as np
    from PIL import Image
    img = np.array(Image.open(io.BytesIO(get(U + "assets/qr-code.png"))).convert("RGB"))[:, :, ::-1]
    d, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    good = d == U
    ok &= good
    print("  [%s] QR decodes to live URL  (%s)" % ("PASS" if good else "FAIL", d or "no decode"))
except ImportError:
    print("  [SKIP] opencv missing - scan with a phone")

print("\nLIVE AND VERIFIED" if ok else "\nPROBLEMS ABOVE")
sys.exit(0 if ok else 1)
