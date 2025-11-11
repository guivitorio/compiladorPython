# src/parser.py

from .token_type import TiposDeToken

# Classe de Exceção para Erros Sintáticos, para replicar a lógica do JS
class SyntaxError(Exception):
    def __init__(self, message, token=None):
        super().__init__(message)
        self.token = token # Armazena o token para contexto
        self.is_syntax_error = True # Simula o atributo _syntaxError
"""
Implementação do Analisador Sintático Descendente Preditivo Recursivo.
(Checkpoint 2)

Este parser consome os tokens gerados pelo AnalisadorLexico (Ckp 1)
e verifica se a estrutura do programa segue a gramática definida.
"""
class Parser:
  def __init__(self, scanner):
    self.scanner = scanner # O Analisador Léxico (Ckp 1)
    self.current = None # O token atual
    self.errors = [] # Lista de erros sintáticos (Req 3 - Ckp 2) 

  # Ponto de entrada do Analisador Sintático.
  def parse(self):
    self._advance() # Pega o primeiro token
    try:
      self._programa() # Inicia pela regra principal da gramática
      self._expect(TiposDeToken.FIM_DE_ARQUIVO) # Espera o fim do arquivo
      return {"sucesso": True, "erros": []}
    except SyntaxError as e:
      # Se for um erro sintático conhecido (inclui erro léxico que abortou)
      self.errors.append(str(e))
      return {"sucesso": False, "erros": self.errors}
    except Exception:
      # Se for outro erro (ex: erro interno)
      raise

  # --- Métodos Utilitários do Parser ---

  # Consome o token atual e pega o próximo do Analisador Léxico.
  # Se o léxico retornar 'None' (erro léxico), levanta um erro sintático
  # para abortar a análise.
  def _advance(self):
    t = self.scanner.proximo_token()
    while t is None:
      # Se t for 'None', o Scanner (Ckp 1) encontrou um erro léxico.
      # Aborta a análise sintática (Req 3 - Ckp 2) 
      raise SyntaxError(
        "Erro léxico encontrado. Abortando análise sintática."
      )
    self.current = t

  # Verifica se o token atual é do tipo esperado.
  # Se for, consome-o (_advance).
  # Se não for, levanta um erro sintático (Req 3 - Ckp 2).
  def _expect(self, tipo, texto: str = None):
    if not self.current:
      return self._raise(
        f"Esperado token do tipo {tipo.name}, mas não há token atual."
      )
    if self.current.tipo != tipo:
      return self._raise(
        f"Esperado token do tipo {tipo.name}, encontrado {self._fmt_token(self.current)}."
      )
    # Verificação opcional de texto (ex: esperar '(' e não só LEFT_PAR)
    if texto is not None and self.current.texto != texto:
      return self._raise(
        f"Esperado token '{texto}', encontrado {self._fmt_token(self.current)}."
      )
    self._advance() # Consome o token esperado

  # Verifica se o token atual é de um tipo (e texto) opcional.
  # Se for, consome e retorna 'True'.
  # Se não for, não faz nada e retorna 'False'.
  def _optional(self, tipo, texto: str = None):
    if self.current and self.current.tipo == tipo:
      if texto is None or self.current.texto == texto:
        self._advance()
        return True
    return False

  # Formata um token para exibição em mensagens de erro
  def _fmt_token(self, tok):
    pos = "em posição desconhecida"
    if tok and tok.linha is not None and tok.coluna is not None:
      pos = f"na linha {tok.linha}, coluna {tok.coluna}"
    
    # tok.tipo é um Enum, acessa-se o nome com .name
    tipo_nome = tok.tipo.name if tok.tipo else "DESCONHECIDO"
    return f"'{tok.texto}' ({tipo_nome}) {pos}"

  # Dispara um erro sintático formatado (Req 3 - Ckp 2)
  def _raise(self, msg):
    raise SyntaxError(f"ERRO SINTÁTICO: {msg}", self.current)

  # Verifica se o token atual é de um tipo específico
  def _is_current(self, tipo):
    return self.current and self.current.tipo == tipo

  # --- Implementação da Gramática (Ckp 2) ---
  # Os métodos abaixo correspondem às regras da gramática 

  # Regra: programa : ':' 'DECLARACOES' listaDeclaracoes ':' 'ALGORITMO' listaComandos;
  def _programa(self):
    self._expect(TiposDeToken.DOIS_PONTOS, ":")
    self._expect(TiposDeToken.PALAVRA_RESERVADA_DECLARACOES)
    self._lista_declaracoes()
    self._expect(TiposDeToken.DOIS_PONTOS, ":")
    self._expect(TiposDeToken.PALAVRA_RESERVADA_ALGORITMO)
    self._lista_comandos()

  # Regra: listaDeclaracoes : declaracao listaDeclaracoes | declaracao;
  # Implementação: (declaracao)+ (uma ou mais declarações)
  def _lista_declaracoes(self):
    self._declaracao() # Deve ter pelo menos uma
    while self._is_inicio_declaracao():
      # Pode ter mais
      self._declaracao()
  
  # Verifica se o token atual pode iniciar uma declaração
  def _is_inicio_declaracao(self):
    # Adaptado (Ckp 2, Req 4) : Inicia com IDENTIFICADOR (Ckp 1) ou 'VARIAVEL' (original)
    return (
      self._is_current(TiposDeToken.IDENTIFICADOR) or
      self._is_current(TiposDeToken.PALAVRA_RESERVADA_VARIAVEL)
    )

  # Regra Original (gramatica.txt): declaracao : VARIAVEL ':' tipoVar;
  # Regra Adaptada (Ckp 2, Req 4): O léxico Ckp 1 criou IDENTIFICADOR. 
  # Esta implementação aceita tanto 'VARIAVEL' (literal) quanto um IDENTIFICADOR.
  def _declaracao(self):
    if self._is_current(TiposDeToken.PALAVRA_RESERVADA_VARIAVEL):
      self._advance() # Aceita a palavra-chave 'VARIAVEL'
    else:
      # Ou aceita um IDENTIFICADOR (ex: 'idade', 'nota')
      self._expect(TiposDeToken.IDENTIFICADOR)
    self._expect(TiposDeToken.DOIS_PONTOS, ":")
    self._tipo_var()

  # Regra: tipoVar : 'INTEIRO' | 'REAL';
  def _tipo_var(self):
    if self._optional(TiposDeToken.PALAVRA_RESERVADA_INTEIRO):
      return
    if self._optional(TiposDeToken.PALAVRA_RESERVADA_REAL):
      return
    
    # Erro (Req 3 - Ckp 2) 
    self._raise(
      f"Tipo inválido. Esperado 'INTEIRO' ou 'REAL', encontrado {self._fmt_token(self.current)}."
    )

  # Regra (sem recursão): expressaoAritmetica : termoAritmetico (('+' | '-') termoAritmetico)*
  def _expressao_aritmetica(self):
    self._termo_aritmetico()
    while (
      self._is_current(TiposDeToken.OPERADOR_MATEMATICO) and
      (self.current.texto == "+" or self.current.texto == "-")
    ):
      self._advance() # Consome '+' ou '-'
      self._termo_aritmetico()

  # Regra (sem recursão): termoAritmetico : fatorAritmetico (('*' | '/') fatorAritmetico)*
  def _termo_aritmetico(self):
    self._fator_aritmetico()
    while (
      self._is_current(TiposDeToken.OPERADOR_MATEMATICO) and
      (self.current.texto == "*" or self.current.texto == "/")
    ):
      self._advance() # Consome '*' ou '/'
      self._fator_aritmetico()

  # Regra Original: fatorAritmetico : NUMINT | NUMREAL | VARIAVEL | '(' expressaoAritmetica ')'
  # Implementação Adaptada (Ckp 2, Req 4): 
  # Aceita NUMINT/NUMREAL (Ckp 1), VARIAVEL (literal), IDENTIFICADOR (Ckp 1),
  # ou '(' (Ckp 1) expressaoAritmetica ')' (Ckp 1).
  def _fator_aritmetico(self):
    if self._optional(TiposDeToken.NUMINT):
      return
    if self._optional(TiposDeToken.NUMREAL):
      return
    if self._optional(TiposDeToken.IDENTIFICADOR):
      return # Ckp 1
    if self._optional(TiposDeToken.PALAVRA_RESERVADA_VARIAVEL):
      return # Gramática Original
    
    # Fator entre parênteses (Ckp 1, Req 5)
    if self._optional(TiposDeToken.LEFT_PAR, "("):
      self._expressao_aritmetica()
      self._expect(TiposDeToken.RIGHT_PAR, ")")
      return
    
    # Erro (Req 3 - Ckp 2)
    self._raise(
      f"Fator inválido. Esperado NUMINT, NUMREAL, VARIAVEL, IDENTIFICADOR ou '(', encontrado {self._fmt_token(self.current)}."
    )

  # Regra (sem recursão): expressaoRelacional : termoRelacional (operadorBooleano termoRelacional)*
  def _expressao_relacional(self):
    self._termo_relacional()
    while (
      self._is_current(TiposDeToken.PALAVRA_RESERVADA_E) or
      self._is_current(TiposDeToken.PALAVRA_RESERVADA_OU)
    ):
      self._operador_booleano()
      self._termo_relacional()

  # Regra: termoRelacional : expressaoAritmetica OP_REL expressaoAritmetica | '(' expressaoRelacional ')'
  def _termo_relacional(self):
    if self._optional(TiposDeToken.LEFT_PAR, "("):
      self._expressao_relacional()
      self._expect(TiposDeToken.RIGHT_PAR, ")")
      return
    
    # Caso: expressaoAritmetica OP_REL expressaoAritmetica
    self._expressao_aritmetica()
    self._expect(TiposDeToken.OP_REL) # Ckp 1, Req 4
    self._expressao_aritmetica()

  # Regra: operadorBooleano : 'E' | 'OU';
  def _operador_booleano(self):
    if self._optional(TiposDeToken.PALAVRA_RESERVADA_E):
      return
    if self._optional(TiposDeToken.PALAVRA_RESERVADA_OU):
      return
    self._raise(f"Operador booleano inválido: {self._fmt_token(self.current)}.")

  # Regra: listaComandos : comando listaComandos | comando;
  # Implementação: (comando)+ (um ou mais comandos)
  def _lista_comandos(self):
    self._comando() # Pelo menos um comando
    while self._is_inicio_comando():
      # Seguido de zero ou mais comandos
      self._comando()

  # Verifica se o token atual pode iniciar um comando
  def _is_inicio_comando(self):
    return (
      self._is_current(TiposDeToken.PALAVRA_RESERVADA_VARIAVEL) or # Atribuição
      self._is_current(TiposDeToken.IDENTIFICADOR) or # Atribuição (Ckp 1)
      self._is_current(TiposDeToken.PALAVRA_RESERVADA_LER) or # Entrada
      self._is_current(TiposDeToken.PALAVRA_RESERVADA_IMPRIMIR) or # Saída
      self._is_current(TiposDeToken.PALAVRA_RESERVADA_SE) or # Condição
      self._is_current(TiposDeToken.PALAVRA_RESERVADA_ENQUANTO) or # Repetição
      self._is_current(TiposDeToken.PALAVRA_RESERVADA_INICIO) # Sub-bloco
    )

  # Regra: comando : comandoAtribuicao | comandoEntrada | comandoSaida | comandoCondicao | comandoRepeticao | subAlgoritmo;
  def _comando(self):
    # Ckp 2, Req 4 : Atribuição pode começar com IDENTIFICADOR (Ckp 1) ou 'VARIAVEL'
    if (
      self._is_current(TiposDeToken.PALAVRA_RESERVADA_VARIAVEL) or
      self._is_current(TiposDeToken.IDENTIFICADOR)
    ):
      self._comando_atribuicao()
      return
    if self._is_current(TiposDeToken.PALAVRA_RESERVADA_LER):
      self._comando_entrada()
      return
    if self._is_current(TiposDeToken.PALAVRA_RESERVADA_IMPRIMIR):
      self._comando_saida()
      return
    if self._is_current(TiposDeToken.PALAVRA_RESERVADA_SE):
      self._comando_condicao()
      return
    if self._is_current(TiposDeToken.PALAVRA_RESERVADA_ENQUANTO):
      self._comando_repeticao()
      return
    if self._is_current(TiposDeToken.PALAVRA_RESERVADA_INICIO):
      self._sub_algoritmo()
      return
    # Erro (Req 3 - Ckp 2)
    self._raise(f"Início de comando inválido: {self._fmt_token(self.current)}.")

  # Regra Original: comandoAtribuicao : 'VARIAVEL' = expressaoAritmetica;
  # Regra Adaptada (Ckp 2, Req 4): aceita IDENTIFICADOR no lugar de VARIAVEL. 
  # Utiliza o operador '=' do Ckp 1 (Req 3).
  def _comando_atribuicao(self):
    if self._optional(TiposDeToken.PALAVRA_RESERVADA_VARIAVEL):
      # aceita literal 'VARIAVEL' (gramática original)
      pass
    else:
      self._expect(TiposDeToken.IDENTIFICADOR) # aceita IDENTIFICADOR (Ckp 1)
    self._expect(TiposDeToken.OPERADOR_ATRIBUICAO, "=") # Ckp 1, Req 3
    self._expressao_aritmetica()

  # Regra Original: comandoEntrada : 'LER' VARIAVEL;
  # Regra Adaptada (Ckp 2, Req 4): aceita IDENTIFICADOR no lugar de VARIAVEL. 
  def _comando_entrada(self):
    self._expect(TiposDeToken.PALAVRA_RESERVADA_LER)
    if self._optional(TiposDeToken.PALAVRA_RESERVADA_VARIAVEL):
      # aceita literal 'VARIAVEL' (gramática original)
      return
    self._expect(TiposDeToken.IDENTIFICADOR) # aceita IDENTIFICADOR (Ckp 1)

  # Regra Original: comandoSaida : 'IMPRIMIR' LEFT_PAR (VARIAVEL | CADEIA) RIGHT_PAR;
  # Regra Adaptada (Ckp 2, Req 4/5):
  # Esta implementação aceita 'IMPRIMIR' '(' (IDENTIFICADOR | 'VARIAVEL' | CADEIA) ')'.
  def _comando_saida(self):
    self._expect(TiposDeToken.PALAVRA_RESERVADA_IMPRIMIR)
    self._expect(TiposDeToken.LEFT_PAR, "(") # Ckp 1, Req 5

    if self._optional(TiposDeToken.PALAVRA_RESERVADA_VARIAVEL):
      # aceita literal 'VARIAVEL'
      pass
    elif self._optional(TiposDeToken.IDENTIFICADOR):
      # aceita IDENTIFICADOR (Ckp 1)
      pass
    elif self._optional(TiposDeToken.CADEIA):
      # aceita CADEIA (ex: "ola")
      pass
    else:
      # Erro (Req 3 - Ckp 2)
      self._raise(
        f"Esperado VARIAVEL, IDENTIFICADOR ou CADEIA, encontrado {self._fmt_token(self.current)}."
      )
    self._expect(TiposDeToken.RIGHT_PAR, ")") # Ckp 1, Req 5

  # Regra: comandoCondicao : 'SE' expressaoRelacional 'ENTAO' comando ('SENAO' comando)?;
  def _comando_condicao(self):
    self._expect(TiposDeToken.PALAVRA_RESERVADA_SE)
    self._expressao_relacional()
    self._expect(TiposDeToken.PALAVRA_RESERVADA_ENTAO)
    self._comando() # Comando do 'SE'
    
    # Parte opcional do 'SENAO'
    if self._optional(TiposDeToken.PALAVRA_RESERVADA_SENAO):
      self._comando() # Comando do 'SENAO'

  # Regra: comandoRepeticao : 'ENQUANTO' expressaoRelacional comando;
  def _comando_repeticao(self):
    self._expect(TiposDeToken.PALAVRA_RESERVADA_ENQUANTO)
    self._expressao_relacional()
    self._comando()

  # Regra: subAlgoritmo : 'INICIO' listaComandos 'FIM';
  def _sub_algoritmo(self):
    self._expect(TiposDeToken.PALAVRA_RESERVADA_INICIO)
    self._lista_comandos()
    self._expect(TiposDeToken.PALAVRA_RESERVADA_FIM)