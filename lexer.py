import re

class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.tokens = []
        self.errors = []
        self.keywords = ['tipo:', 'data:', 'local:', 'relato:', 'envolvidos:', 'objetos:']
        self.naturezas = ['furto', 'roubo', 'perda', 'ameaça', 'acidente', 'estelionato']
    
    def tokenize(self):
        token_patterns = [
            ('DATA_HORA', r'\d{2}/\d{2}/\d{2}( \d{2}:\d{2})?'),
            ('KEYWORD', r'tipo:|data:|local:|relato:|envolvidos:|objetos:'),
            ('NATUREZA', r'furto|roubo|perda|ameaça|acidente|estelionato'),
            ('PALAVRA', r'[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\-]+'),
            ('NUMERO', r'\d+'),
            ('PONTUACAO', r'[\,\.\:]'),
            ('ESPACO', r'\s+'),
            ('OUTRO', r'.')
        ]

        tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns)
        
        line_num = 1
        for mo in re.finditer(tok_regex, self.input_text):
            kind = mo.lastgroup
            value = mo.group()
            
            if kind == 'ESPACO':
                if '\n' in value:
                    line_num += value.count('\n')
                continue
            elif kind == 'OUTRO':
                self.errors.append(f"Erro léxico (linha {line_num}): Caractere inválido '{value}'")
                continue
            
            # Verifica se é palavra-chave
            if kind == 'KEYWORD' and value not in self.keywords:
                self.errors.append(f"Erro léxico (linha {line_num}): Palavra-chave inválida '{value}'")
                continue
                
            # Verifica se é natureza válida
            if kind == 'NATUREZA' and value not in self.naturezas:
                self.errors.append(f"Erro léxico (linha {line_num}): Natureza inválida '{value}'")
                continue
            
            self.tokens.append((kind, value, line_num))
            if '\n' in value:
                line_num += value.count('\n')
        
        return self.tokens, self.errors