import random
from enum import Enum

class Florista(Enum):
    ''' Tipo enumerado que representa os 4 floristas que trabalham na floricultura. Na arquitetura,
    cada um representa uma memória cache presente na lista floristas da arquitetura, que pode ser
    acessada pelo valor associado.'''
    HELOISE = 0
    JOSIANE = 1
    VALERIA = 2
    YANDRE = 3

class Moesi(Enum):
    ''' Tipo enumerado que representa os 5 estados do protocolo MOESI de coerência de cache, sendo
    usados nas linhas para essa indicação.'''
    M = 0
    O = 1
    E = 2
    S = 3
    I = 4

class Linha:
    ''' Estrutura que representa uma Linha na cache. Cada linha tem um vetor de inteiros do mesmo
    tamanho dos blocos da MP, além de um indicador do estado do protocolo Moesi e o número do bloco
    da MP que está armazenado aqui.'''

    dados: list[int]
    estado: Moesi
    bloco_mp: int

    def __init__(self):
        ''' Inicializa-se a cache com valores inválidos, então em especial o estado é I.'''
        self.dados = [0, 0, 0, 0]  # Cada linha tem 4 palavras
        self.estado =  Moesi.I # Inicialmente, todas começam como Invalid (I)
        self.bloco_mp = -1  # Qual bloco da memória principal está armazenado

class Cache:
    ''' Estrutura que representa os dados de controle de um florista na floricultura. Na arquitetura,
    ela possui uma lista de linhas de cache e um contador para aplicar o protocolo Fifo.'''

    linhas: list[Linha]
    fifo_contador: int

    def __init__(self):
        ''' Inicializa-se com 4 linhas inválidas e um contador nulo.'''
        self.linhas = [Linha() for _ in range(4)]  # Cada cache tem 4 linhas
        self.fifo_contador = 0  # Para FIFO

    def buscar_flor(self, flor: int) -> int|None:
        '''Essa função confere se um bloco da MP está presente na cache. Caso esteja (hit), ela
        retorna o índice da linha na cache. Caso contrário (miss), retorna None.
        
        >>> c = Cache()
        >>> c.linhas[1].estado = Moesi.E
        >>> c.linhas[1].dados = [0, 1, 2, 3]
        >>> c.linhas[1].bloco_mp = 0
        >>> c.linhas[2].dados = [4, 5, 6, 7]
        >>> c.linhas[2].bloco_mp = 1
        >>> c.buscar_flor(0)
        1
        >>> c.buscar_flor(4)

        '''
        bloco_flor = bloco(flor)
        for i in range(4):
            if self.linhas[i].estado != Moesi.I and self.linhas[i].bloco_mp == bloco_flor:
                return i
        return None
    
class Floricultura:
    ''' Classe que representa uma floricultura que possui uma estufa que armazena uma determinada
    quantidade de flores. A estufa é uma metáfora para a MP, que possui 32 blocos de 4 inteiros, em
    que cada posição está associada a uma flor e o valor armazenado é o número de flores em estoque.
    Além disso, há também uma lista com 4 caches, que aqui são representados por floristas em um
    sistema de gestão do estoque das suas flores. As políticas usadas são Moesi, Fifo e Write-Back.
    '''

    estufa: list[list[int]]
    floristas: list[Cache]
    
    def __init__(self):
        ''' Inicializa-se a estufa com valores randômicos de flores em estoque e Caches com linhas
        inválidas.'''

        self.estufa = [[random.randint(0, 250) for _ in range(4)] for _ in range(32)]
        self.floristas = [Cache() for _ in range(4)]
    
    def imprimir_caches(self):
        '''    
        Imprime o estado de todas as caches, mostrando as linhas, blocos e estados.
        '''
        print("\n=== Estado das Caches ===")
        for i, cache in enumerate(self.floristas):
            print(f"\nFlorista {Florista(i).name}:")
            for j, linha in enumerate(cache.linhas):
                estado = linha.estado.name
                bloco = linha.bloco_mp if linha.bloco_mp != -1 else "N/A"
                dados = linha.dados
                print(f"  Linha {j}: Bloco MP {bloco}, Estado {estado}, Dados {dados}")
        print("=========================\n")
    
    def leitura(self, florista: Florista, flor: int):

        ''' Realiza a leitura de uma flor por um florista específico.
        Busca em outras caches caso o dado não esteja presente na cache local.
        '''

        print("\nLeitura:", florista.name, "Flor:", flor)

        florista_cache = self.floristas[florista.value]  # Obtemos a cache do florista
        bloco_flor = bloco(flor)  # Calcula o bloco da memória principal
        posicao = pos_no_bloco(flor)  # Calcula a posição dentro do bloco

        # Verifica se o bloco está na cache local
        linha_cache = florista_cache.buscar_flor(flor)
        if linha_cache is not None:
            # Hit: A flor está na cache
            print(f"\nFlor encontrada!" 
                  f"\nQuantidade:{florista_cache.linhas[linha_cache].dados[posicao]}" 
                  f"\nEstado:{florista_cache.linhas[linha_cache].estado}")

            self.imprimir_caches() #TESTE

            return florista_cache.linhas[linha_cache].dados[posicao]

        # Miss: Verificar as outras caches
        print("Flor não encontrada! Verificando com outros floristas...")
        for i, outro_florista in enumerate(self.floristas):
            if i == florista.value:  # Não verificar a cache do florista atual
                continue
            linha_outro_florista = outro_florista.buscar_flor(flor)
            if linha_outro_florista is not None:
                # Dado encontrado em outra cache
                linha = outro_florista.linhas[linha_outro_florista]
                print(f"\nFlor encontrada com florista {Florista(i).name}!"
                      f"\nQuantidade {linha.dados[posicao]}" 
                      f"\nEstado: {linha.estado.name}")

                if linha.estado == Moesi.M:
                    # Transferir dados e atualizar estados
                    linha.estado = Moesi.O
                    nova_linha = florista_cache.linhas[florista_cache.fifo_contador % 4]
                    florista_cache.fifo_contador += 1
                    nova_linha.dados = linha.dados.copy()
                    nova_linha.bloco_mp = linha.bloco_mp
                    nova_linha.estado = Moesi.S  # Compartilhado
                    print("Dado transferido. Estado atualizado para Shared.")

                    self.imprimir_caches() #TESTE

                    return nova_linha.dados[posicao]
                
                elif linha.estado == Moesi.E:
                    # Apenas copiar dados, estados permanecem consistentes
                    linha.estado = Moesi.O
                    nova_linha = florista_cache.linhas[florista_cache.fifo_contador % 4]
                    florista_cache.fifo_contador += 1
                    nova_linha.dados = linha.dados.copy()
                    nova_linha.bloco_mp = linha.bloco_mp
                    nova_linha.estado = Moesi.S  # Compartilhado
                    print("Dado transferido. Estado atualizado para Shared.")

                    self.imprimir_caches() #TESTE

                    return nova_linha.dados[posicao]                
                
                elif linha.estado in (Moesi.O, Moesi.S):
                    # Apenas copiar dados, estados permanecem consistentes
                    nova_linha = florista_cache.linhas[florista_cache.fifo_contador % 4]
                    florista_cache.fifo_contador += 1
                    nova_linha.dados = linha.dados.copy()
                    nova_linha.bloco_mp = linha.bloco_mp
                    nova_linha.estado = Moesi.S  # Compartilhado
                    print("Dado transferido. Estado atualizado para Shared.")

                    self.imprimir_caches() #TESTE

                    return nova_linha.dados[posicao]

        # Nenhuma outra cache possui o dado, buscar na memória principal
        print("Bloco não encontrado em nenhuma cache. Carregando da memória principal...")
        linha_substituir = florista_cache.fifo_contador % 4
        florista_cache.fifo_contador += 1
        linha_cache = florista_cache.linhas[linha_substituir]
        linha_cache.dados = self.estufa[bloco_flor].copy()
        linha_cache.bloco_mp = bloco_flor
        linha_cache.estado = Moesi.E  # Estado inicial ao carregar da MP
        print(f"Bloco carregado!" 
              f"\nQuantidade: {linha_cache.dados[posicao]}"
                f"\nEstado: {linha_cache.estado}")

        self.imprimir_caches() #TESTE

        return linha_cache.dados[posicao]
    
    def escrita(self, florista: Florista, flor: int, novo_valor: int):
        print("\nescrita", florista, flor, novo_valor)
        return None
        
    def imprime(self):
        print("\nimprime")

def bloco(flor: int) -> int:
    ''' Função que calcula o bloco na memória principal que determinada flor (posição geral entre 0
    e 128) está presente'''
    return flor // 4

def pos_no_bloco(flor: int) -> int:
    ''' Função que calcula a posição que uma flor (posição geral entre 0 e 128) se encontra dentro
    do bloco da memória principal.'''
    return flor % 4



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
    floricultura: Floricultura = Floricultura()

    # Menu interativo
    while True:
        # Início
        print("\n\n--- Menu Floricultura com Simulação de Cache ---")
        # Escolha do florista
        florista_str = input("\nEscolha um florista (h: Heloise, j: Josiane, v: Valeria, y: Yandre, s: Sair): ").strip().lower()
        while florista_str not in ["h", "j", "v", "y", "s"]:
            florista_str = input("\nOpção Inválida! Digite um caractere válido para um florista (h: Heloise, j: Josiane, v: Valeria, y: Yandre, s: Sair): ").strip().lower()
        florista = Florista.HELOISE
        match florista_str:
            case "s":
                break
            case "h":
                florista = Florista.HELOISE
            case "j":
                florista = Florista.JOSIANE
            case "v":
                florista = Florista.VALERIA
            case "y":
                florista = Florista.YANDRE
        
        # Escolha da Operação
        operacao = input("\nEscolha a operação (l: Leitura, e: Escrita, s: Sair): ").strip().lower()
        while operacao not in ["l", "e", "s"]:
            operacao = input("\nOpção Inválida!Escolha uma operação da lista (l: Leitura, e: Escrita, s: Sair): ").strip().lower()
        if operacao == "s":
            break
        
        print("\nFlores disponíveis:\n")
        print(flores)
        flor_str = input("\nDigite o nome da flor: ").strip().lower()
        while (flor:= flores_dict.get(flor_str)) is None:
            flor_str = input("Flor não encontrada no catálogo! Digite outro nome: ").strip().lower()
        if operacao == "l":
            floricultura.leitura(florista, flor)
        elif operacao == "e":
            while True:
                try:
                    novo_valor = int(input("\nDigite o novo valor do estoque: "))
                    if novo_valor < 0:
                        print("O estoque não pode ser negativo! Insira um novo valor de estoque: ")
                    else:
                        break
                except ValueError:
                    print("Entrada inválida! Insira um novo valor de estoque: ")
            floricultura.escrita(florista, flor, novo_valor)
        floricultura.imprime()
    print("Encerrando o sistema da floricultura...")


main()