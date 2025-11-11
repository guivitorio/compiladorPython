# Compilador (Checkpoint 1 & 2)

Projeto de disciplina "Construção de Compiladores I" que implementa um analisador léxico (Checkpoint 1) e um analisador sintático descendente recursivo (Checkpoint 2) para uma gramática didática.

## Visão geral

Este repositório contém um pequeno compilador/analisador para uma linguagem acadêmica (arquivo de exemplo: `programa_checkpoint2.mc`). O objetivo é demonstrar os requisitos do Checkpoint 1 (Analisador Léxico) e do Checkpoint 2 (Analisador Sintático).

- O analisador léxico (`src/scanner.py`) converte o código-fonte em tokens.
- O analisador sintático (`src/parser.py`) consome os tokens e valida se o programa segue a gramática.

O programa principal de demonstração é `main.py`.

## Funcionalidades implementadas

- Reconhecimento de identificadores e palavras reservadas
- Números inteiros e reais
- Comentários (comentário de linha com `#` e comentário multi-linhas `/* ... */` tratado no scanner)
- Operadores aritméticos e relacionais básicos
- Parênteses e strings (cadeias)
- Parser recursivo-descendente com reporte de erros sintáticos

## Estrutura do projeto

```
Compilador-python/
├─ gramatica.txt                # Documento da gramática (referência)
├─ main.py                      # Runner principal que demonstra léxico + parser
├─ programa_checkpoint2.mc      # Exemplo de programa de entrada (teste)
└─ src/
   ├─ __init__.py
   ├─ scanner.py                # Analisador léxico
   ├─ parser.py                 # Analisador sintático
   ├─ token_type.py             # Enumeração dos tipos de token
   └─ token.py                  # Classe Token
```

## Requisitos

- Python 3.7+ (testado com CPython 3.8/3.9)
- Não há dependências externas além da biblioteca padrão.

## Como executar

Abra o PowerShell na raiz do projeto (`C:\Users\Guilherme\Desktop\Compilador-python`) e execute:

```powershell
python .\main.py
```

Saída esperada:
- O scanner imprime a sequência de tokens encontrados em `programa_checkpoint2.mc`.
- Em seguida, o parser executa a análise sintática e informa se houve sucesso ou reporta erros sintáticos.

Se preferir ver apenas a análise sintática, edite `main.py` para pular a impressão dos tokens ou comente a seção correspondente.

## Comandos Git úteis (PowerShell)

Inicializar repositório local (se ainda não existir):

```powershell
# Inicializa o repositório
git init
# Cria um .gitignore básico (recomendado)
@"__pycache__/`n*.pyc`n.env`n"@ | Out-File -Encoding UTF8 .gitignore
# Adiciona e comita
git add .
git commit -m "Initial commit: analisador léxico e sintático"
```

Conectar a um repositório GitHub existente e enviar:

```powershell
# Adicione o remoto (substitua pela URL do seu repo)
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git
# Se o repositório remoto já tiver commits, sincronize primeiro:
git fetch origin
git pull --rebase origin main
# Envie para o GitHub
git push -u origin main
```

> Dica: se o GitHub pedir senha ao usar HTTPS, gere um Personal Access Token (PAT) e use-o como senha.

## Testes e verificação rápida

- Executando `main.py` com o arquivo de exemplo `programa_checkpoint2.mc` deve imprimir tokens e terminar com "Análise sintática concluída sem erros." (se o programa de exemplo for válido).

## Arquitetura / Contrato mínimo

- Entrada: string do código-fonte (arquivo `.mc`).
- Saída: sequência de tokens (impressa) e um relatório de sucesso/erros sintáticos.
- Erros léxicos retornam `None` no fluxo do scanner e causam abortamento do parser com mensagem adequada.

## Próximos passos sugeridos

- Adicionar testes unitários (pytest) para o scanner e o parser.
- Formalizar a gramática em `gramatica.txt` e gerar casos de teste automáticos.
- Adicionar lint/format (black, flake8) e CI (GitHub Actions).

## Autores

- Arthur Vinicius de Albuquerque Pimentel
- Guilherme Vitório Rodrigues de Carvalho
