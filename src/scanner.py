# src/scanner.py

import sys # Para simular console.error (print(..., file=sys.stderr))
from .token_type import TiposDeToken
from .token import Token

"""
Requisito 7 (Ckp 1): Tabela de Palavras Reservadas.
Este dicionário (Map) associa strings de palavras-chave aos seus respectivos tipos de token.
"""
PALAVRAS_RESERVADAS = {
  "DECLARACOES": TiposDeToken.PALAVRA_RESERVADA_DECLARACOES,
  "ALGORITMO": TiposDeToken.PALAVRA_RESERVADA_ALGORITMO,
  "INTEIRO": TiposDeToken.PALAVRA_RESERVADA_INTEIRO,
  "REAL": TiposDeToken.PALAVRA_RESERVADA_REAL,
  "IMPRIMIR": TiposDeToken.PALAVRA_RESERVADA_IMPRIMIR,
  "LER": TiposDeToken.PALAVRA_RESERVADA_LER,
  "SE": TiposDeToken.PALAVRA_RESERVADA_SE,
  "ENTAO": TiposDeToken.PALAVRA_RESERVADA_ENTAO,
  "SENAO": TiposDeToken.PALAVRA_RESERVADA_SENAO,
  "ENQUANTO": TiposDeToken.PALAVRA_RESERVADA_ENQUANTO,
  "INICIO": TiposDeToken.PALAVRA_RESERVADA_INICIO,
  "FIM": TiposDeToken.PALAVRA_RESERVADA_FIM,
  "E": TiposDeToken.PALAVRA_RESERVADA_E,
  "OU": TiposDeToken.PALAVRA_RESERVADA_OU,
  "VARIAVEL": TiposDeToken.PALAVRA_RESERVADA_VARIAVEL, # Palavra-chave da gramática original
}

class AnalisadorLexico:
  def __init__(self, codigo_fonte):
    self.codigo_fonte = codigo_fonte
    self.posicao_atual = 0 # Índice do caractere que estamos lendo
    self.linha_atual = 1 # Requisito 9 (Ckp 1): Controla a linha atual
    self.coluna_atual = 1 # Requisito 9 (Ckp 1): Controla a coluna atual

  # --- Métodos de Verificação e Navegação ---

  def _chegou_ao_fim(self):
    return self.posicao_atual >= len(self.codigo_fonte)

  # Avança um caractere e atualiza a posição (linha/coluna)
  def _avancar_caractere(self):
    if self._chegou_ao_fim():
      return "\0" # Caractere nulo para fim de arquivo
    caractere = self.codigo_fonte[self.posicao_atual]
    self.posicao_atual += 1
    if caractere == "\n":
      self.linha_atual += 1
      self.coluna_atual = 1
    else:
      self.coluna_atual += 1
    return caractere

  # Espia o caractere na posição 'lookahead' sem consumi-lo
  def _olhar_proximo_caractere(self, lookahead=0):
    idx = self.posicao_atual + lookahead
    if idx >= len(self.codigo_fonte):
      return "\0"
    return self.codigo_fonte[idx]

  # --- Métodos de Processamento ---

  def _ignorar_espacos_e_comentarios(self):
    while not self._chegou_ao_fim():
      proximo_caractere = self._olhar_proximo_caractere()

      # 1. Ignorar espaços em branco
      if proximo_caractere.isspace(): # Substitui /\s/.test(c)
        self._avancar_caractere()
        continue

      # 2. Requisito 8 (Ckp 1): Ignorar comentário de múltiplas linhas /* ... */
      if (
        proximo_caractere == "/" and
        self._olhar_proximo_caractere(1) == "*"
      ):
        self._avancar_caractere() # Consome '/'
        self._avancar_caractere() # Consome '*'
        while (
          not self._chegou_ao_fim() and
          not (
            self._olhar_proximo_caractere() == "*" and
            self._olhar_proximo_caractere(1) == "/"
          )
        ):
          self._avancar_caractere() # Consome o conteúdo do comentário
        if not self._chegou_ao_fim():
          self._avancar_caractere() # Consome '*'
          self._avancar_caractere() # Consome '/'
        continue # Volta ao início do loop

      # 3. Requisito 8 (Ckp 1): Ignorar comentário de linha única # ... \n
      if proximo_caractere == "#":
        self._avancar_caractere() # Consome '#'
        while (
          not self._chegou_ao_fim() and
          self._olhar_proximo_caractere() != "\n" and
          self._olhar_proximo_caractere() != "\r"
        ):
          self._avancar_caractere() # Consome o conteúdo do comentário
        continue
      
      # Se não for espaço nem comentário, para o loop
      break

  # Retorna o próximo token válido do código-fonte.
  # Este é o método principal do Analisador Léxico (Ckp 1).
  def proximo_token(self):
    # 1. Limpa espaços e comentários antes de procurar o próximo token.
    self._ignorar_espacos_e_comentarios()

    # 2. Se chegamos ao fim, retorna o token FIM_DE_ARQUIVO.
    if self._chegou_ao_fim():
      return Token(
        TiposDeToken.FIM_DE_ARQUIVO,
        "FIM_DE_ARQUIVO",
        self.linha_atual,
        self.coluna_atual
      )

    # 3. Guarda a posição inicial para reportar erros (Req 9)
    linha_do_token = self.linha_atual
    coluna_do_token = self.coluna_atual
    caractere_atual = self._avancar_caractere() # Consome o primeiro caractere do token

    # Requisito 1 (Ckp 1): Identificadores
    # Regra: (a-z | A-Z | _)(a-z | A-Z | _ | 0-9)*
    if caractere_atual.isalpha() or caractere_atual == "_":
      texto_completo = caractere_atual
      while (
        not self._chegou_ao_fim() and
        (self._olhar_proximo_caractere().isalnum() or # isalpha() or isdigit()
         self._olhar_proximo_caractere() == "_")
      ):
        texto_completo += self._avancar_caractere()

      # Requisito 7 (Ckp 1): Antes de retornar IDENTIFICADOR, verifica se é uma Palavra Reservada.
      tipo = PALAVRAS_RESERVADAS.get(texto_completo)
      if tipo is None:
        tipo = TiposDeToken.IDENTIFICADOR
      
      return Token(tipo, texto_completo, linha_do_token, coluna_do_token)

    # Requisito 6 (Ckp 1): Constantes Numéricas (Inteiros e Reais)
    # Regra: ((0-9)*.)?(0-9)+
    if caractere_atual.isdigit() or caractere_atual == ".":
      texto_completo = caractere_atual
      tem_ponto_decimal = caractere_atual == "."

      while not self._chegou_ao_fim():
        proximo = self._olhar_proximo_caractere()
        if proximo.isdigit():
          texto_completo += self._avancar_caractere()
        elif proximo == "." and not tem_ponto_decimal:
          tem_ponto_decimal = True
          texto_completo += self._avancar_caractere()
        else:
          break

      # Requisito 9 (Ckp 1): Tratamento de erro para números inválidos (ex: "1." ou ".")
      if texto_completo.endswith(".") or texto_completo == ".":
        print(
          f"ERRO LÉXICO: Número inválido '{texto_completo}' na Linha: {linha_do_token}, Coluna: {coluna_do_token}",
          file=sys.stderr
        )
        return None # Retorna None para sinalizar erro léxico

      # Requisito 9 (Ckp 1): Tratamento de erro para identificador mal formado (ex: "123nome")
      if self._olhar_proximo_caractere().isalpha():
        while (
          not self._chegou_ao_fim() and
          self._olhar_proximo_caractere().isalnum()
        ):
          texto_completo += self._avancar_caractere()
        print(
          f"ERRO LÉXICO: Identificador inválido '{texto_completo}' na Linha: {linha_do_token}, Coluna: {coluna_do_token}",
          file=sys.stderr
        )
        return None

      tipo_numero = (
        TiposDeToken.NUMREAL if tem_ponto_decimal else TiposDeToken.NUMINT
      )
      return Token(tipo_numero, texto_completo, linha_do_token, coluna_do_token)

    # Requisitos 2, 3, 4, 5 (Ckp 1): Operadores e Símbolos
    if caractere_atual == "+":
      return Token(TiposDeToken.OPERADOR_MATEMATICO, "+", linha_do_token, coluna_do_token)
    if caractere_atual == "-":
      return Token(TiposDeToken.OPERADOR_MATEMATICO, "-", linha_do_token, coluna_do_token)
    if caractere_atual == "*":
      return Token(TiposDeToken.OPERADOR_MATEMATICO, "*", linha_do_token, coluna_do_token)
    if caractere_atual == "/":
      return Token(TiposDeToken.OPERADOR_MATEMATICO, "/", linha_do_token, coluna_do_token)
    if caractere_atual == "(":
      return Token(TiposDeToken.LEFT_PAR, "(", linha_do_token, coluna_do_token)
    if caractere_atual == ")":
      return Token(TiposDeToken.RIGHT_PAR, ")", linha_do_token, coluna_do_token)
    if caractere_atual == ":":
      return Token(TiposDeToken.DOIS_PONTOS, ":", linha_do_token, coluna_do_token)
      
    if caractere_atual == ">":
      if self._olhar_proximo_caractere() == "=":
        self._avancar_caractere()
        return Token(TiposDeToken.OP_REL, ">=", linha_do_token, coluna_do_token)
      return Token(TiposDeToken.OP_REL, ">", linha_do_token, coluna_do_token)

    if caractere_atual == "<":
      if self._olhar_proximo_caractere() == "=":
        self._avancar_caractere()
        return Token(TiposDeToken.OP_REL, "<=", linha_do_token, coluna_do_token)
      return Token(TiposDeToken.OP_REL, "<", linha_do_token, coluna_do_token)

    if caractere_atual == "!":
      if self._olhar_proximo_caractere() == "=":
        self._avancar_caractere()
        return Token(TiposDeToken.OP_REL, "!=", linha_do_token, coluna_do_token)
      # Erro: '!' sozinho não é válido (segue a lógica original de JS)
      
    if caractere_atual == "=":
      if self._olhar_proximo_caractere() == "=":
        self._avancar_caractere()
        return Token(TiposDeToken.OP_REL, "==", linha_do_token, coluna_do_token)
      # Requisito 3 (Ckp 1)
      return Token(TiposDeToken.OPERADOR_ATRIBUICAO, "=", linha_do_token, coluna_do_token)

    # Token CADEIA (necessário para 'IMPRIMIR' da gramática do Ckp 2
    if caractere_atual == '"':
      texto = ""
      # Consome caracteres até o próximo "
      while not self._chegou_ao_fim() and self._olhar_proximo_caractere() != '"':
        texto += self._avancar_caractere()
      
      # Requisito 9 (Ckp 1): Erro de cadeia não finalizada
      if self._olhar_proximo_caractere() != '"':
        print(
          f"ERRO LÉXICO: Cadeia não finalizada na Linha: {linha_do_token}, Coluna: {coluna_do_token}",
          file=sys.stderr
        )
        return None
      self._avancar_caractere() # Consome o " final
      return Token(
        TiposDeToken.CADEIA,
        texto,
        linha_do_token,
        coluna_do_token
      )

    # Requisito 9 (Ckp 1): Erro para Símbolos Desconhecidos
    # Se o caractere não se encaixou em nenhuma regra, é um erro.
    print(
      f"ERRO LÉXICO: Símbolo não reconhecido '{caractere_atual}' na Linha: {linha_do_token}, Coluna: {coluna_do_token}",
      file=sys.stderr
    )
    return None