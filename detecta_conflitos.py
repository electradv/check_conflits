import subprocess
import sys

def get_merge_base(branch1, branch2):
    return subprocess.check_output(
        ["git", "merge-base", branch1, branch2], encoding="utf-8"
    ).strip()

def simula_merge_e_verifica_conflitos(branch1, branch2):
    base = get_merge_base(branch1, branch2)
    output = subprocess.check_output(
        ["git", "merge-tree", base, branch1, branch2],
        encoding="utf-8"
    )

    conflitos = []
    arquivo_atual = None

    for linha in output.splitlines():
        if linha.startswith("changed in both") or linha.startswith("changed in"):
            partes = linha.strip().split(" ")
            if len(partes) > 2:
                arquivo_atual = partes[-1]
        elif linha.startswith("<<<") and arquivo_atual:
            conflitos.append(arquivo_atual)
            arquivo_atual = None

    return conflitos

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python detecta_conflitos.py <branch-base> <branch-feature>")
        sys.exit(1)

    branch_base = sys.argv[1]
    branch_feature = sys.argv[2]

    conflitos = simula_merge_e_verifica_conflitos(branch_base, branch_feature)

    if conflitos:
        print("\n⚠️ Arquivos com conflito detectado:")
        for f in conflitos:
            print(f"   - {f}")
        sys.exit(1)
    else:
        print("✅ Nenhum conflito detectado.")
