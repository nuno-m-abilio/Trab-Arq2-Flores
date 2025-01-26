from enum import Enum
import floricultura as f

def main():
    ''' Inicia a estrutura de dados da estufa com os tamanho corretos, insere valores na MP estufa,
    associa posições na MP a flores e inicia o loop de interação com o usuário para que ele escolha
    o processador florista e a operação que quer fazer. O loop interativo continua, printando a
    arquitetura a cada iteração, até que o usuário insira "s".'''
    
    # Inicializa nomes das flores e associa a números de 0 a 127
    flores = ['rosa', 'tulipa', 'orquídea', 'girassol', 'lírio', 'dália', 'azaleia', 'cravo',
    'violeta', 'hortênsia', 'camélia', 'jasmim', 'begônia', 'amarílis', 'gérbera', 'peônia',
    'petúnia', 'magnólia', 'copo-de-leite', 'margarida', 'narciso', 'lótus', 'gladíolo', 'antúrio',
    'hibisco', 'flor-de-lis', 'ipê', 'cerejeira', 'verbena', 'alecrim', 'lavanda', 'manacá',
    'cravina', 'camomila', 'girassol-do-campo', 'bromélia', 'ciclame', 'calêndula', 'estrelícia',
    'flor-de-maio', 'freesia', 'azucena', 'anis', 'trevo', 'salvia', 'buganvília', 'edelvaisse',
    'cactos', 'flor-de-maracujá', 'gengibre', 'gloxínia', 'ipê-amarelo', 'jasmim-manga', 'tagetes',
    'magnólia-branca', 'papoula', 'maranta', 'murta', 'névoa', 'orquídea-negra', 'primavera',
    'rabo-de-galo', 'sálvia-branca', 'tomilho', 'urze', 'verbena-roxa', 'viuvinha', 'ylang-ylang',
    'cravo-vermelho', 'jasmim-estrela', 'lírio-do-vale', 'madressilva', 'mimosa', 'onze-horas',
    'orquídea-bambu', 'orquídea-chocolate', 'orquídea-fantasma', 'orquídea-vanila', 'paixão-flor',
    'papoula-californiana', 'pata-de-vaca', 'primavera-roxa', 'raíz-de-ouro', 'rosa-do-deserto',
    'rosa-mística', 'silene', 'stevia-flor', 'tajete', 'trapoeraba', 'trevo-roxo', 'baunilha',
    'trombeta-dourada', 'valeriana', 'verônica', 'viburno', 'viola-tricolor', 'xerântemo', 'zínia',
    'angelônia', 'astromélia', 'belladona', 'cana-da-índia', 'cinerária', 'cosmos', 'dianthus',
    'dulcamara', 'echinacea', 'esponjinha', 'flor-borboleta', 'flor-de-cera', 'flor-de-coral',
    'flor-de-íris', 'gazânia', 'gerânio', 'helicônia', 'jasmim-do-cabo', 'lantana', 'malva',
    'melissa', 'mirabilis', 'nêspera-florida', 'no-me-esqueças', 'orquídea-tigre', 'pervinca',
    'ranúnculo', 'sapatinho-de-judia', 'trébol', 'uvaia-florida']

    # Dicionário associando nomes a números
    flores_dict = {flores[i]: i for i in range(128)}

    # Inicializa a Floricultura
    floricultura = f.Floricultura()

    # Menu interativo
    while True:
        # Início
        print("\n\n--- Menu Floricultura com Simulação de Cache ---")
        
        # Escolha do florista
        florista_str = input("\nEscolha um florista (h: Heloise, j: Josiane, v: Valeria, y: Yandre, s: Sair): ").strip().lower()
        while florista_str not in ["h", "j", "v", "y", "s"]:
            florista_str = input("\nOpção Inválida! Digite um caractere válido para um florista (h: Heloise, j: Josiane, v: Valeria, y: Yandre, s: Sair): ").strip().lower()
        florista = f.Florista.HELOISE
        match florista_str:
            case "s":
                break
            case "h":
                florista = f.Florista.HELOISE
            case "j":
                florista = f.Florista.JOSIANE
            case "v":
                florista = f.Florista.VALERIA
            case "y":
                florista = f.Florista.YANDRE
        
        # Escolha da Operação
        operacao = input("\nEscolha a operação (l: Leitura, e: Escrita, s: Sair): ").strip().lower()
        while operacao not in ["l", "e", "s"]:
            operacao = input("\nOpção Inválida!Escolha uma operação da lista (l: Leitura, e: Escrita, s: Sair): ").strip().lower()
        
        # Saí da aplicação apagando toda a floricultura
        if operacao == "s":
            break
        
        # Escolher sobre qual flor iremos fazer a operação
        print("\nFlores disponíveis:\n")
        print(flores)
        flor_str = input("\nDigite o nome da flor: ").strip().lower()
        while (flor:= flores_dict.get(flor_str)) is None:
            flor_str = input("Flor não encontrada no catálogo! Digite outro nome: ").strip().lower()
        
        # Confere se é o caso e faz a leitura
        if operacao == "l":
            floricultura.leitura(florista, flor)
       
       # Confere se é o caso e faz a escrita
        elif operacao == "e":
            while True:
                try: # Try-except para catch o ValueError caso o novo valo do imput nçao seja int
                    novo_valor = int(input("\nDigite o novo valor do estoque: "))
                    if novo_valor < 0:
                        print("O estoque não pode ser negativo! Insira um novo valor de estoque: ")
                    else:
                        break
                except ValueError:
                    print("Entrada inválida! Insira um novo valor de estoque: ")
            floricultura.escrita(florista, flor, novo_valor)
        
        # Permite visualização completa da floricultura,com todos os dados da estufa e dos floristas
    print("Encerrando o sistema da floricultura...")

main()