"""
This script generates the table in the README.
"""

from pathlib import Path
import re

fdir = Path(".")
fpaths = list(fdir.glob("*/README.md"))

table = []
total = 0
for i, fpath in enumerate(sorted(fpaths)): 
    task = str(fpath).split("/")[0]
    github_url = f"https://github.com/HazyResearch/legalbench/tree/main/tasks/{task}".replace(" ", "%20")
    
    summary, license_name, size = "", "", ""
    with open(fpath) as in_file:
        for line in in_file:
            line = line.strip()
            if line.startswith("**Task summary**: "):
                summary = line.replace("**Task summary**: ", "").strip()
            if line.startswith("**Size (samples)**: "):
                size = line.replace("**Size (samples)**: ", "").strip()
            if line.startswith("**License**: "):
                license_name = line.replace("**License**: ", "").strip()
    url = f"[{task}]({github_url})"
    if len(size) > 0:
        total += eval(size)
    table.append([url, summary, size, license_name])
    print(str(i+2) + "|" + "|".join([task, size, summary, license_name]))
README = f"""# Task overview 

The table below provides an overview of the different tasks.

There are a total of {len(table)} tasks, encompassing {int(total)} samples.

Task | Description | Size | License 
---- | ----------- | -----| -------
"""

for row in table: 
    README += "|".join(row) + "\n"

with open("README.MD", "w") as out_file:
    out_file.write(README)
