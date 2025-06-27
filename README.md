# Detect Merge Conflicts Action

Esta GitHub Action detecta se há **conflitos de merge** entre duas branches antes de realizar o merge.

## 💡 Como funciona

Ela simula um merge usando `git merge-tree` e falha caso algum conflito real seja detectado.

## 🛠️ Uso

```yaml
- uses: sua-org-ou-usuario/detect-merge-conflicts@v1
  with:
    base: ${{ github.base_ref }}
    head: ${{ github.head_ref }}
```

## 📥 Inputs

| Nome  | Descrição                  | Obrigatório |
|-------|-----------------------------|-------------|
| base  | Branch base do PR          | ✅ sim      |
| head  | Branch de origem do PR     | ✅ sim      |

## ✅ Resultado

- Falha com erro se um ou mais arquivos estiverem em conflito real.
