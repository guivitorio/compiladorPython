# src/token.py

from .token_type import TiposDeToken
"""
Token.py

Define a estrutura de um Token.
Armazena o tipo, o texto (lexema) e a localização (linha/coluna)
para facilitar o reporte de erros (Requisito 9 - Ckp 1).
"""
class Token:
  def __init__(self, tipo: TiposDeToken, texto: str, linha: int = None, coluna: int = None):
    self.tipo = tipo
    self.texto = texto
    self.linha = linha # Requisito 9 (Ckp 1)
    self.coluna = coluna # Requisito 9 (Ckp 1)

  def __str__(self):
    pos_info = ""
    if self.linha is not None and self.coluna is not None:
      pos_info = f", Linha: {self.linha}, Coluna: {self.coluna}"
    # O tipo do enum é acessado com .name
    return f"Token [Tipo: {self.tipo.name}, Texto: '{self.texto}'{pos_info}]"