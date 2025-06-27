from collections import defaultdict
import re
import subprocess
import sys

def get_merge_base(branch1, branch2):
    return subprocess.check_output(
        ["git", "merge-base", branch1, branch2], encoding="utf-8"
    ).strip()

def simula_merge_e_verifica_conflitos(branch1, branch2):
    base = get_merge_base(branch1, branch2)

    output_bytes = subprocess.check_output(["git", "merge-tree", base, branch1, branch2])
    output = output_bytes.decode("utf-8", errors="replace")

    return extrair_conflitos(output)

def extrair_conflitos(diff_text: str):
    arquivos_conflito = defaultdict(int)
    current_file = None

    # Quebra o texto linha por linha
    lines = diff_text.splitlines()
    
    for i, line in enumerate(lines):
        # Detecta caminho do arquivo
        if line.strip().startswith("result") or line.strip().startswith("our"):
            match = re.search(r'\s+[\d]+ [a-f0-9]+\s+(.+)', line)
            if match:
                current_file = match.group(1)

        # Detecta início de um bloco de conflito
        elif line.startswith("@@") and current_file:
            arquivos_conflito[current_file] += 1

    return arquivos_conflito

# def extrair_conflitos(output: str) -> list[str]:
#     conflitos = set()
#     arquivo_atual = None

#     for linha in output.splitlines():
#         linha = linha.strip()

#         # Captura caminho do arquivo
#         if any(linha.startswith(prefixo) for prefixo in ("merged", "result", "our", "their")):
#             match = re.search(r'([\w/\.-]+\.*)$', linha)
#             if match:
#                 arquivo_atual = match.group(1)

#         # Verifica marcador real de conflito
#         if '<<<<<<<' in linha and arquivo_atual:
#             conflitos.add(arquivo_atual)
#             arquivo_atual = None  # Reinicia até novo match de arquivo

#     return list(conflitos)

# def extrair_conflitos(output: str):
#     conflitos = set()
#     arquivo_atual = None

#     linhas = output.splitlines()
#     for i, linha in enumerate(linhas):
#         linha = linha.strip()

#         # Detecta nome do arquivo antes do bloco
#         if linha.startswith("merged") or linha.startswith("result") or linha.startswith("our") or linha.startswith("their"):
#             match = re.search(r'([\w/\.-]+\.*)$', linha)
#             if match:
#                 arquivo_atual = match.group(1)

#         # Quando chega num bloco de diff, verifica se tem + e -
#         elif linha.startswith("@@") and arquivo_atual:
#             # olha as próximas 6 linhas do bloco
#             bloco = linhas[i+1:i+6]
#             has_minus = any(l.strip().startswith("-") for l in bloco)
#             has_plus = any(l.strip().startswith("+") for l in bloco)

#             if has_minus and has_plus:
#                 conflitos.add(arquivo_atual)

#     return list(set(conflitos))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python detecta_conflitos.py <branch-base> <branch-feature>")
        sys.exit(1)

    branch_base = sys.argv[1]
    branch_feature = sys.argv[2]

    # branch_base = "origin/development" #sys.argv[1]
    # branch_feature = "origin/conflito-dev" #sys.argv[2]

    # branch_base = "origin/qa" #sys.argv[1]
    # branch_feature = "origin/master" #sys.argv[2]

    conflitos = simula_merge_e_verifica_conflitos(branch_base, branch_feature)

    if conflitos:
        print(f"⚠️ -{len(conflitos)} arquivos com conflito detectado:")
        print(conflitos)
        # sys.exit(1)
    else:
        print("✅ Nenhum conflito detectado")