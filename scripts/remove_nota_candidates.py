#!/usr/bin/env python3
"""Remove all NOTA candidates from candidates.json"""

import json

json_path = "app/data/lok_sabha/lok-sabha-2024/candidates.json"

with open(json_path, "r") as f:
    candidates = json.load(f)

original_count = len(candidates)
filtered = [c for c in candidates if c["name"] != "NOTA"]
removed_count = original_count - len(filtered)

with open(json_path, "w") as f:
    json.dump(filtered, f, indent=4)

print(f"Removed {removed_count} NOTA candidates. {len(filtered)} candidates remaining.")

