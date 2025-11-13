# Compilador - Analisador Léxico e Sintático (Checkpoint 1 & 2)

**Disciplina:** Projeto de Linguagens de Programação

Implementação de um compilador didático que demonstra dois dos principais componentes de qualquer compilador real:
1. **Checkpoint 1 (CP1):** Analisador Léxico (Scanner/Lexer)
2. **Checkpoint 2 (CP2):** Analisador Sintático (Parser) — com foco principal neste projeto

## Visão geral e objetivos

Este projeto implementa as duas primeiras fases de um compilador para uma linguagem acadêmica simples. Os arquivos de entrada têm extensão `.mc` (abreviação de "Máquina de Compilação").

**Fluxo do compilador:**
```
Código-fonte (.mc)
    ↓ [CP1: Analisador Léxico]
Sequência de Tokens
    ↓ [CP2: Analisador Sintático]
Validação Sintática (Sucesso ou Erro)
```

- **Checkpoint 1:** `src/scanner.py` — reconhece e classifica os elementos básicos do código.
- **Checkpoint 2:** `src/parser.py` — valida a estrutura e relações entre os elementos.

O arquivo `main.py` demonstra o funcionamento completo de ambas as fases.

## Funcionalidades implementadas

### Checkpoint 1 — Analisador Léxico

O scanner (`src/scanner.py`) realiza as seguintes tarefas:

- **Identificadores** — reconhece nomes de variáveis (ex.: `numero1`, `aux`).
- **Palavras-chave** — reconhece e classifica palavras reservadas:
  - Declaração: `DECLARACOES`, `VARIAVEL`, `INTEIRO`, `REAL`
  - Programa: `ALGORITMO`, `INICIO`, `FIM`
  - Controle: `SE`, `ENTAO`, `SENAO`, `ENQUANTO`
  - I/O: `LER`, `IMPRIMIR`
  - Lógica: `E`, `OU`
- **Números** — reconhece inteiros (`NUMINT`) e reais (`NUMREAL`).
- **Operadores aritméticos** — `+`, `-`, `*`, `/`.
- **Operadores relacionais** — `>`, `<`, `>=`, `<=`, `==`, `!=`.
- **Operador de atribuição** — `=`.
- **Símbolos especiais** — parênteses `(`, `)`, dois-pontos `:`.
- **Strings/Cadeias** — texto entre aspas duplas (ex.: `"ola"`).
- **Comentários** — ignora linhas começadas com `#` e blocos `/* ... */`.
- **Rastreamento de posição** — registra linha e coluna de cada token para melhor reporte de erros.

**Saída do Scanner:** lista de tokens com tipo, texto, linha e coluna.

### Checkpoint 2 — Analisador Sintático (Parser Recursivo-Descendente)

O parser (`src/parser.py`) é o foco principal deste projeto. Implementa um **parser recursivo-descendente preditivo** que valida a estrutura do programa de acordo com a gramática.

#### Gramática suportada (simplificada)

```
programa       : ':' DECLARACOES listaDeclaracoes ':' ALGORITMO listaComandos
listaDeclaracoes : (declaracao)+
declaracao     : VARIAVEL ':' tipoVar | IDENTIFICADOR ':' tipoVar
tipoVar        : INTEIRO | REAL

listaComandos  : (comando)+
comando        : comandoAtribuicao
               | comandoEntrada
               | comandoSaida
               | comandoCondicao
               | comandoRepeticao
               | subAlgoritmo

comandoAtribuicao : VARIAVEL '=' expressaoAritmetica | IDENTIFICADOR '=' expressaoAritmetica
comandoEntrada    : LER VARIAVEL | LER IDENTIFICADOR
comandoSaida      : IMPRIMIR '(' (VARIAVEL | IDENTIFICADOR | CADEIA) ')'
comandoCondicao   : SE expressaoRelacional ENTAO comando (SENAO comando)?
comandoRepeticao  : ENQUANTO expressaoRelacional comando
subAlgoritmo      : INICIO listaComandos FIM

expressaoAritmetica : termoAritmetico (('+' | '-') termoAritmetico)*
termoAritmetico     : fatorAritmetico (('*' | '/') fatorAritmetico)*
fatorAritmetico     : NUMINT | NUMREAL | IDENTIFICADOR | '(' expressaoAritmetica ')'

expressaoRelacional : termoRelacional (('E' | 'OU') termoRelacional)*
termoRelacional     : expressaoAritmetica OP_REL expressaoAritmetica | '(' expressaoRelacional ')'
```

#### Funcionalidades do Parser

- **Análise recursiva-descendente:** cada regra gramatical é implementada como um método que consome tokens.
- **Reporte de erros detalhado** (Requisito 3 do CP2):
  - Tipo de erro (token esperado vs. encontrado).
  - Localização (linha e coluna).
  - Continua buscando erros até o fim do arquivo.
- **Compatibilidade adaptada** (Requisito 4 do CP2):
  - Aceita tanto a palavra-chave literal `VARIAVEL` (gramática original) quanto `IDENTIFICADOR` (CP1).
- **Operadores booleanos:** suporta expressões lógicas com `E` (AND) e `OU` (OR).
- **Estruturas de controle:** condicional (`SE...ENTAO...SENAO`) e repetição (`ENQUANTO`).
- **Sub-blocos:** permite `INICIO...FIM` para agrupar comandos.

#### Fluxo de execução do Parser

1. **Advance:** obtém o primeiro token do scanner.
2. **Programa:** tenta fazer match com a regra `programa`.
3. **Análise recursiva:** cada regra gramatical chama outras regras conforme necessário.
4. **Expect/Optional:** verifica se o token atual é do tipo esperado:
   - `_expect()` — obrigatório; erro se não encontrado.
   - `_optional()` — opcional; consome se encontrado.
5. **Reporte:** se um erro sintático for encontrado, é capturado e adicionado à lista de erros.
6. **Resultado:** retorna dicionário `{"sucesso": bool, "erros": [lista_de_mensagens]}`.

#### Tratamento de erros no Parser

- Se o scanner encontrar um erro léxico (ex.: número mal formado), ele retorna `None`.
- O parser detecta isso no `_advance()` e levanta um `SyntaxError` com mensagem apropriada.
- Mensagens de erro incluem contexto: "ERRO SINTÁTICO: Esperado token do tipo X, encontrado Y na linha 5, coluna 10."

## Estrutura do projeto

```
Compilador-python/
├─ gramatica.txt                # Gramática formal de referência (documento original)
├─ README.md                    # Este arquivo
├─ main.py                      # Programa principal — demonstra CP1 e CP2
├─ programa_checkpoint2.mc      # Arquivo de exemplo (programa de teste)
└─ src/
   ├─ __init__.py               # Pacote Python
   ├─ scanner.py                # Analisador Léxico (CP1) — ~300 linhas
   ├─ parser.py                 # Analisador Sintático (CP2) — ~400 linhas
   ├─ token_type.py             # Enumeração dos tipos de token
   └─ token.py                  # Classe Token (estrutura de dados)
```

## Requisitos e instalação

- **Python:** 3.7 ou superior (testado com 3.8 e 3.9).
- **Dependências externas:** nenhuma! Usa apenas a biblioteca padrão do Python.

### Instalação rápida

Não há nada a instalar. Basta clonar o repositório e executar:

```powershell
cd C:\Users\Guilherme\Desktop\Compilador-python
python .\main.py
```

## Como usar e executar

### Execução padrão

```powershell
python .\main.py
```

**O que acontece:**

1. O programa lê o arquivo `programa_checkpoint2.mc`.
2. **Fase 1 (CP1):** O scanner analisa o código e imprime todos os tokens encontrados:
   ```
   Token [Tipo: DUAS_PONTOS, Texto: ':', Linha: 1, Coluna: 1]
   Token [Tipo: PALAVRA_RESERVADA_DECLARACOES, Texto: 'DECLARACOES', Linha: 1, Coluna: 2]
   Token [Tipo: IDENTIFICADOR, Texto: 'numero1', Linha: 2, Coluna: 1]
   ...
   ```

3. **Fase 2 (CP2):** O parser percorre os tokens e valida se obedecem a gramática:
   - Se **sucesso:** imprime "Análise sintática concluída sem erros."
   - Se **erro:** imprime lista de erros sintáticos encontrados (linha, coluna, tipo do erro).

### Analisar um arquivo personalizado

Edite `main.py` e altere a linha:

```python
programa_checkpoint = "programa_checkpoint2.mc"
```

para o caminho do seu arquivo:

```python
programa_checkpoint = "seu_programa.mc"
```

Depois execute novamente:

```powershell
python .\main.py
```

### Apenas o scanner (CP1)

Se quiser testar só o analisador léxico, crie um script Python simples:

```python
from src.scanner import AnalisadorLexico
from src.token_type import TiposDeToken

with open("programa_checkpoint2.mc", "r", encoding="utf-8") as f:
    codigo = f.read()

scanner = AnalisadorLexico(codigo)

while True:
    token = scanner.proximo_token()
    if token:
        print(token)
    if token is None or token.tipo == TiposDeToken.FIM_DE_ARQUIVO:
        break
```

### Apenas o parser (CP2)

```python
from src.scanner import AnalisadorLexico
from src.parser import Parser

with open("programa_checkpoint2.mc", "r", encoding="utf-8") as f:
    codigo = f.read()

scanner = AnalisadorLexico(codigo)
parser = Parser(scanner)

resultado = parser.parse()

if resultado["sucesso"]:
    print("✓ Programa válido!")
else:
    print("✗ Erros encontrados:")
    for erro in resultado["erros"]:
        print(f"  - {erro}")
```

## Exemplo de programa válido

Arquivo `programa_checkpoint2.mc`:

```
: DECLARACOES
numero1 : INTEIRO
numero2 : INTEIRO
numero3 : INTEIRO
: ALGORITMO
LER numero1
LER numero2
SE numero1 > numero2 ENTAO
  INICIO
    numero3 = numero1
  FIM
IMPRIMIR ( numero3 )
```

**Análise:**
- Declaração de 3 variáveis inteiras.
- Leitura de 2 números.
- Condicional: se número1 > número2, atribui número1 a número3.
- Imprime número3.

Ao rodar `main.py`, o scanner imprime os tokens e o parser valida que a estrutura está correta.

## Tratamento de erros

### Erros Léxicos (CP1)

O scanner detecta e reporta:
- Números mal formados (ex.: `1.2.3`, `.`, `1.`).
- Identificadores inválidos (ex.: `123abc`).
- Símbolos não reconhecidos.
- Strings não fechadas.

Mensagem de erro:
```
ERRO LÉXICO: Cadeia não finalizada na Linha: 5, Coluna: 10
```

### Erros Sintáticos (CP2)

O parser detecta e reporta:
- Tokens fora de ordem.
- Tipos de token não esperados.
- Estruturas incompletas.
- Operadores ou palavras-chave em posição errada.

Mensagem de erro:
```
ERRO SINTÁTICO: Esperado token do tipo PALAVRA_RESERVADA_ENTAO, encontrado 'numero1' (IDENTIFICADOR) na linha 12, coluna 22.
```

Se houver múltiplos erros, todos são coletados e impressos no final.

## Testes e verificação

### Com o arquivo de exemplo

```powershell
# Na raiz do projeto
python .\main.py
```

**Resultado esperado:** Se `programa_checkpoint2.mc` é um programa válido, a saída termina com:
```
--- Análise Sintática Concluída ---
Análise sintática concluída sem erros.
```

### Com um programa inválido

Crie um arquivo `teste_erro.mc`:

```
: DECLARACOES
numero : INTEIRO
: ALGORITMO
SE numero > 5 ENTAO
  numero = 10
```

(Falta a palavra-chave `INICIO` ou não fecha a estrutura corretamente.)

Edite `main.py` para apontar para `teste_erro.mc` e execute:

```powershell
python .\main.py
```

**Resultado esperado:** 
```
Foram encontrados erros sintáticos:
- ERRO SINTÁTICO: ...
```

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

## Arquitetura e Design

### Componentes principais

**`src/token.py`** — Classe `Token`
- Armazena: tipo, texto (lexema), linha, coluna.
- Método `__str__()` para impressão formatada.

**`src/token_type.py`** — Enumeração `TiposDeToken`
- Define todas as categorias de token: IDENTIFICADOR, NUMINT, OP_REL, etc.

**`src/scanner.py`** — Classe `AnalisadorLexico`
- Métodos privados para navegação: `_avancar_caractere()`, `_olhar_proximo_caractere()`.
- Método `_ignorar_espacos_e_comentarios()` que pula espaços em branco e comentários.
- Método público `proximo_token()` — retorna o próximo token válido ou `None` se erro léxico.

**`src/parser.py`** — Classe `Parser` + Exceção `SyntaxError`
- Métodos privados `_advance()`, `_expect()`, `_optional()` para navegação e validação.
- Métodos correspondentes à gramática: `_programa()`, `_comando()`, `_expressao_aritmetica()`, etc.
- Método público `parse()` — inicia a análise e retorna dicionário com sucesso/erros.

### Fluxo de dados

```
arquivo.mc
    ↓
main.py (lê arquivo)
    ↓
scanner.AnalisadorLexico(codigo)
    ↓ [loop proximo_token()]
token[] (lista em memória)
    ↓
parser.Parser(scanner)
    ↓ [parser.parse()]
resultado {"sucesso": bool, "erros": []}
    ↓
main.py (imprime resultado)
    ↓
stdout/stderr
```

## Próximos passos e melhorias sugeridas

1. **Testes automatizados** — criar testes com `pytest` para scanner e parser.
2. **Tabela de símbolos** — rastrear declarações de variáveis (CP3 futuro).
3. **Geração de código** — transformar árvore sintática em instruções intermediárias (CP3/CP4).
4. **Lint e CI** — adicionar `black`, `flake8` e GitHub Actions para automação.
5. **Documentação estendida** — adicionar mais exemplos e casos de teste na wiki.

## Licença

Defina uma licença apropriada (ex.: MIT, Apache 2.0) e crie um arquivo `LICENSE` na raiz.

## Autores

- Arthur Vinicius de Albuquerque Pimentel
- Guilherme Vitório Rodrigues de Carvalho
