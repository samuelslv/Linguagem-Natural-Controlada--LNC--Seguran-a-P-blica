class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.current_pos = 0
        self.registros = []
        self.erros = []
    
    def parse(self):
        self.tokens, lex_errors = self.lexer.tokenize()
        self.erros.extend(lex_errors)
        
        while not self.is_at_end():
            try:
                registro = self.parse_registro()
                if registro:
                    self.registros.append(registro)
            except ParseError as e:
                self.erros.append(str(e))
                self.synchronize()
        
        return self.registros, self.erros
    
    def parse_registro(self):
        registro = {
            'natureza': None,
            'data_hora': None,
            'local': None,
            'descricao': None,
            'envolvidos': None,
            'objetos': None
        }
        
        # tipo: natureza
        self.consume('KEYWORD', 'tipo:')
        registro['natureza'] = self.consume('NATUREZA')[1]  # Acessa o valor da tupla
        
        # data: data_hora
        self.consume('KEYWORD', 'data:')
        registro['data_hora'] = self.consume('DATA_HORA')[1]
        
        # local: local
        self.consume('KEYWORD', 'local:')
        registro['local'] = self.parse_text()
        
        # relato: descrição
        self.consume('KEYWORD', 'relato:')
        registro['descricao'] = self.parse_text()
        
        # envolvidos: envolvidos
        self.consume('KEYWORD', 'envolvidos:')
        registro['envolvidos'] = self.parse_text()
        
        # objetos: objetos
        self.consume('KEYWORD', 'objetos:')
        registro['objetos'] = self.parse_text()
        
        return registro
    
    def parse_text(self):
        words = []
        while not self.is_at_end() and self.peek()[0] in ['PALAVRA', 'NUMERO', 'PONTUACAO']:
            words.append(self.advance()[1])  # Acessa o valor da tupla
        return ' '.join(words)
    
    def consume(self, token_type, value=None):
        if self.check(token_type, value):
            return self.advance()
        token = self.peek()
        raise ParseError(
            token[2] if len(token) > 2 else -1,  # Número da linha
            f"Esperado {token_type} '{value if value else ''}', encontrado '{token[1] if len(token) > 1 else 'EOF'}'"
        )
    
    def check(self, token_type, value=None):
        if self.is_at_end():
            return False
        token = self.peek()
        if token[0] != token_type:  # Acessa o tipo da tupla
            return False
        if value is not None and token[1] != value:  # Acessa o valor da tupla
            return False
        return True
    
    def advance(self):
        if not self.is_at_end():
            self.current_pos += 1
        return self.previous()
    
    def peek(self):
        return self.tokens[self.current_pos] if self.current_pos < len(self.tokens) else ('EOF', '', -1)
    
    def previous(self):
        return self.tokens[self.current_pos - 1]
    
    def is_at_end(self):
        return self.current_pos >= len(self.tokens)
    
    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous()[1] == 'objetos:':  # Acessa o valor da tupla
                return
            if self.peek()[1] == 'tipo:':  # Acessa o valor da tupla
                return
            self.advance()

class ParseError(Exception):
    def __init__(self, line_num, message):
        self.line_num = line_num
        self.message = message
        super().__init__(f"Erro de sintaxe (linha {line_num}): {message}")