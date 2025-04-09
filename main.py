from lexer import Lexer
from parser import Parser, ParseError

def format_output(registros):
    output = "ocorrências:\n"
    for registro in registros:
        output += "  registro:\n"
        output += f"    tipo: {registro['natureza']}\n"
        output += f"    data: {registro['data_hora']}\n"
        output += f"    local: {registro['local']}\n"
        output += f"    relato: {registro['descricao']}\n"
        output += f"    envolvidos: {registro['envolvidos']}\n"
        output += f"    objetos: {registro['objetos']}\n"
    return output

def main():
    try:
        with open('ocorrencias.txt', 'r', encoding='utf-8') as file:
            texto = file.read()
        
        lexer = Lexer(texto)
        parser = Parser(lexer)
        registros, erros = parser.parse()
        
        print("\n=== OCORRÊNCIAS PROCESSADAS ===\n")
        print(format_output(registros))
        
        if erros:
            print("\n=== ERROS ENCONTRADOS ===")
            for erro in erros:
                print(f"- {erro}")
        
        print(f"\nResumo: {len(registros)} registros válidos, {len(erros)} erros encontrados")
        
        with open('ocorrencias_processadas.txt', 'w', encoding='utf-8') as f:
            f.write(format_output(registros))
            print("\nArquivo 'ocorrencias_processadas.txt' gerado com sucesso!")
            
    except FileNotFoundError:
        print("Erro: Arquivo 'ocorrencias.txt' não encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")

if __name__ == "__main__":
    main()