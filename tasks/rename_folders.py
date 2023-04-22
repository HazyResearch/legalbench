import os

folders = os.listdir(".")
for f in folders:
    if not os.path.isdir(f) or not os.path.exists(os.path.join(f, "README.md")):
        continue
    with open(os.path.join(f, "README.md")) as in_file:
        readme = in_file.readlines()

    new_f = f.lower().replace(" ", "_")
    readme[0] = f"# {new_f}"
    readme = " ".join(readme)
    
    with open(os.path.join(f, "README.md"), "w") as out_file:
        out_file.write(readme)
    os.rename(f, new_f)
    print(f"{f} --> {new_f}")