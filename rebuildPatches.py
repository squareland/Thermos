# Copyright (C) kmecpp 2022

import subprocess

from pathlib import Path

# NOTE: "--ignore-space-at-eol" breaks some patches!

clean = Path("eclipse/Clean/src/main/java")
modified = Path("eclipse/Cauldron/src/main/java")

def git_diff(p1, p2):
    return subprocess.Popen([
            'git', 'diff',
             '--minimal', '--no-index', '--no-prefix', '--ignore-blank-lines',
             str(p1), str(p2)
        ], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

print("Computing diff...")
diff = git_diff(clean, modified)
files = [file for file in diff.split("diff --git ") if file] # First element of list will be empty

print("Generating patches...")
for file in files:
    lines = [line for line in file.splitlines() if line != '\ No newline at end of file']

    patch_start = [i for i in range(len(lines)) if lines[i].startswith('---')][0]
    lines = lines[patch_start:]    

    base_path = work_path = None

    if lines[0] != "--- /dev/null":
        base_path = Path(lines[0][4:].strip('"')).relative_to("eclipse/Clean/src/main/java")
        lines[0] = "--- " + Path("../src-base/minecraft", base_path).as_posix()
    if lines[1] != "+++ /dev/null":
        work_path = Path(lines[1][4:].strip('"')).relative_to("eclipse/Cauldron/src/main/java")
        lines[1] = "+++ " + Path("../src-work/minecraft", work_path).as_posix()

    output_path = Path("patches2", (work_path if work_path else base_path)).with_suffix(".java.patch")

    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("@@ "):
            lines[i] = line[:line.rindex("@@") + 2]

    if lines[-1]:
        lines.append("") # Add a blank line at EOF if missing

    patch = "\n".join(lines)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        with output_path.open() as f:
            if f.read() == patch:
                continue


    print(output_path)    
    with open(output_path, "w+") as f:
        f.write(patch)

print("DONE!")

