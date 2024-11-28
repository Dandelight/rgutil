"""
A simple script that crawls information about an academic article
by DOI.

Copyleft 2023 Ruiming Guo
"""

import sys
import json
try:
    import crossref_commons.retrieval
except ImportError as e:
    print("Please run pip install crossref-commons")
    raise e

if len(sys.argv) == 3:
    in_path, out_path = sys.argv[1:]
else:
    print("Usage: python crossref.py <input file> <output file>")
    sys.exit(1)


result = []
with open(in_path, "r") as f:
    for index, doi in enumerate(f):
        doi = doi.strip()
        print(f"{index} Fetching {doi}")
        res = crossref_commons.retrieval.get_publication_as_json(doi)
        result.append(res)

with open(out_path, "w") as f:
    json.dump(result, f)
    print(f"Saved to {out_path}")
