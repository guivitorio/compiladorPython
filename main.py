# main.py

import sys
from src.scanner import AnalisadorLexico
from src.parser import Parser, SyntaxError
from src.token_type import TiposDeToken
"""
CONSTRUÇÃO DE COMPILADORES I
Checkpoint 1 (Analisador Léxico) e Checkpoint 2 (Analisador Sintático)

Nomes dos Integrantes do Grupo:

- Arthur Vinicius de Albuquerque Pimentel
- Guilherme Vitório Rodrigues de Carvalho

"""

def main():
  try:
    # Ajuste o caminho do arquivo de entrada conforme a sua estrutura de pastas
    # O arquivo original é 'programa_checkpoint2.mc' (arquivo está na raiz do projeto)
    programa_checkpoint = "programa_checkpoint2.mc"
    
    # Usa a forma idiomática de Python para ler o arquivo
    with open(programa_checkpoint, "r", encoding="utf-8") as f:
        codigo_fonte = f.read()

    # --- Fase 1: Análise Léxica (Demonstração Ckp 1) ---
    analisador = AnalisadorLexico(codigo_fonte)

    print("--- Iniciando Análise Léxica do Arquivo (Ckp 1) ---")

    while True:
      token_atual = analisador.proximo_token()
      if token_atual:
        print(token_atual)
      
      # O loop continua até encontrar o FIM_DE_ARQUIVO ou um erro léxico (que retorna None)
      if token_atual is None or token_atual.tipo == TiposDeToken.FIM_DE_ARQUIVO:
          break

    print("--- Análise Léxica Concluída ---")

    # --- Fase 2: Análise Sintática (Ckp 2) ---

    # É necessário criar uma *nova instância* do Analisador Léxico
    # para o Parser, pois o primeiro analisador já consumiu o código-fonte.
    analisador_para_parser = AnalisadorLexico(codigo_fonte)
    parser = Parser(analisador_para_parser)

    print("\n--- Iniciando Análise Sintática (Ckp 2) ---")

    # O método .parse() inicia a análise sintática descendente recursiva
    resultado = parser.parse()

    if resultado["sucesso"]:
      print("Análise sintática concluída sem erros.")
    else:
      # Requisito 3 (Ckp 2): Reportar erros sintáticos
      print("Foram encontrados erros sintáticos:", file=sys.stderr)
      for err in resultado["erros"]:
        print("- " + err, file=sys.stderr)
      sys.exit(1)

  except FileNotFoundError:
    print(f"Ocorreu um erro: Arquivo '{programa_checkpoint}' não encontrado.", file=sys.stderr)
    sys.exit(1)
  except Exception as erro:
    # Erros internos não-tratados pelo parser (como erro de codificação)
    print("Ocorreu um erro ao tentar processar o arquivo:", erro, file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
  main()