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
    
    def leitura(self, florista: Florista, flor: int):
        print("\nleitura", florista, str(flor))
        return None
    
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
