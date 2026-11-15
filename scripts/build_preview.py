"""Build index.html from scripts/preview_template.html using the REAL recorded outputs."""
import base64
import html
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "docs", "outputs")
read = lambda n: open(os.path.join(OUT, n), encoding="utf-8").read().strip("\n")
res = json.load(open(os.path.join(OUT, "results.json"), encoding="utf-8"))

page = open(os.path.join(ROOT, "scripts", "preview_template.html"), encoding="utf-8").read()
values = {
    "SCHOLARSHIP": html.escape(read("scholarship_session.txt")),
    "SCHOLARSHIP_INVALID": html.escape(read("scholarship_invalid_input.txt")),
    "PHARMACY": html.escape(read("pharmacy_session.txt")),
    "PHARMACY_INVALID": html.escape(read("pharmacy_invalid_input.txt")),
    "TESTS_PASSED": str(res["tests"]["total"] - res["tests"]["failed"]),
    "TESTS_TOTAL": str(res["tests"]["total"]),
    "REVENUE": f"{res['pharmacy']['total_revenue']:,.0f}",
}
for key, val in values.items():
    page = page.replace("{{" + key + "}}", val)
assert "{{" not in page, "unfilled placeholder"

# Embed every image as a data URI so index.html is fully self-contained:
# it shows all visuals even when opened on its own, without the assets/ folder.
def embed(match):
    path = os.path.join(ROOT, match.group(1))
    data = base64.b64encode(open(path, "rb").read()).decode("ascii")
    return 'src="data:image/png;base64,' + data + '"'

page = re.sub(r'src="(assets/[a-z_]+\.png)"', embed, page)
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)
print("wrote index.html", len(page), "bytes")
