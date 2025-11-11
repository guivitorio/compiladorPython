# src/token_type.py

import enum

"""
TiposDeToken.py

Este ficheiro exporta um objeto que funciona como uma enumeração
para todas as categorias de tokens que o nosso analisador pode reconhecer.
"""
class TiposDeToken(enum.Enum):
  # --- Tokens da Gramática Original (Ckp 2) ---
  PALAVRA_RESERVADA_DECLARACOES = "PALAVRA_RESERVADA_DECLARACOES"
  PALAVRA_RESERVADA_ALGORITMO = "PALAVRA_RESERVADA_ALGORITMO"
  PALAVRA_RESERVADA_INTEIRO = "PALAVRA_RESERVADA_INTEIRO" # Ckp 1 pedia 'int', mas 'INTEIRO' foi mantido
  PALAVRA_RESERVADA_REAL = "PALAVRA_RESERVADA_REAL" # Ckp 1 pedia 'float', mas 'REAL' foi mantido
  PALAVRA_RESERVADA_IMPRIMIR = "PALAVRA_RESERVADA_IMPRIMIR" # Ckp 1 pedia 'print', mas 'IMPRIMIR' foi mantido
  PALAVRA_RESERVADA_LER = "PALAVRA_RESERVADA_LER"
  PALAVRA_RESERVADA_SE = "PALAVRA_RESERVADA_SE" # Ckp 1 pedia 'if'
  PALAVRA_RESERVADA_ENTAO = "PALAVRA_RESERVADA_ENTAO"
  PALAVRA_RESERVADA_SENAO = "PALAVRA_RESERVADA_SENAO" # Ckp 1 pedia 'else'
  PALAVRA_RESERVADA_ENQUANTO = "PALAVRA_RESERVADA_ENQUANTO"
  PALAVRA_RESERVADA_INICIO = "PALAVRA_RESERVADA_INICIO"
  PALAVRA_RESERVADA_FIM = "PALAVRA_RESERVADA_FIM"
  PALAVRA_RESERVADA_E = "PALAVRA_RESERVADA_E"
  PALAVRA_RESERVADA_OU = "PALAVRA_RESERVADA_OU"
  PALAVRA_RESERVADA_VARIAVEL = "PALAVRA_RESERVADA_VARIAVEL" # Token da gramática original

  # --- Tokens Adicionados no Ckp 1 (Analisador Léxico) ---

  # Requisito 1 (Ckp 1): Identificadores (nomes de variáveis)
  IDENTIFICADOR = "IDENTIFICADOR"

  # Requisito 6 (Ckp 1): Números (Inteiros e Reais)
  NUMINT = "NUMINT"
  NUMREAL = "NUMREAL"

  # Requisito 4 (Ckp 1): Operadores Relacionais (>, <, ==, etc.)
  OP_REL = "OP_REL"

  # Requisito 2 (Ckp 1): Operadores Matemáticos (+, -, *, /)
  OPERADOR_MATEMATICO = "OPERADOR_MATEMATICO"

  # Requisito 3 (Ckp 1): Operador de Atribuição (=)
  OPERADOR_ATRIBUICAO = "OPERADOR_ATRIBUICAO"

  # Requisito 5 (Ckp 1): Parênteses
  LEFT_PAR = "LEFT_PAR"
  RIGHT_PAR = "RIGHT_PAR"

  # Token CADEIA (implícito no Ckp 2 para o comando IMPRIMIR)
  CADEIA = "CADEIA"

  # --- Tokens de Controle ---
  DOIS_PONTOS = "DOIS_PONTOS" # Símbolo da gramática original
  FIM_DE_ARQUIVO = "FIM_DE_ARQUIVO" # Token de controle do parser