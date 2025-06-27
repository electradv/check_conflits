from collections import defaultdict
import re
import subprocess
import sys

def get_merge_base(branch_base: str, branch_feature: str):
    return subprocess.check_output(["git", "merge-base", branch_base, branch_feature], encoding="utf-8").strip()

def simulate_merge_and_check_conflicts(branch_base: str, branch_feature: str):
    base = get_merge_base(branch_base, branch_feature)

    output_bytes = subprocess.check_output(["git", "merge-tree", base, branch_base, branch_feature])
    output = output_bytes.decode("utf-8", errors="replace")

    return extract_conflits(output)

def extract_conflits(diff_text: str):
    conflit_list = defaultdict(int)
    current_file = None
    inside_file = False

    lines = diff_text.splitlines()
    
    for line in lines:
        if line.strip().startswith("result") or line.strip().startswith("our"):
            match = re.search(r'\s+\d+\s+[a-f0-9]+\s+(.+)', line)
            if match:
                current_file = match.group(1)
                inside_file = True
                continue
        
        if inside_file and "<<<<<<< .our" in line.strip():
            conflit_list[current_file] += 1

    return conflit_list


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Used: python detecta_conflitos.py <branch-base> <branch-feature>")
        sys.exit(1)

    branch_base = sys.argv[1]
    branch_feature = sys.argv[2]

    # Local Tests
    # branch_base = "origin/development"
    # branch_feature = "feature/multi-agentes"

    # branch_base = "origin/qa"
    # branch_feature = "origin/master"

    conflits = simulate_merge_and_check_conflicts(branch_base, branch_feature)

    if conflits:
        print(f"⚠️ -{len(conflits)} file(s) with conflict detected:")
        print(conflits)
        sys.exit(1)
    else:
        print("✅ No conflicts detected")