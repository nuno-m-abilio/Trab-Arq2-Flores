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

    def buscar_bloco(self, bloco_flor: int) -> int|None:
        '''Essa função confere se um bloco da MP está presente na cache. Caso esteja (hit), ela
        retorna o índice da linha na cache. Caso contrário (miss), retorna None.
        
        >>> c = Cache()
        >>> c.linhas[1].estado = Moesi.E
        >>> c.linhas[1].dados = [0, 1, 2, 3]
        >>> c.linhas[1].bloco_mp = 0
        >>> c.linhas[2].dados = [4, 5, 6, 7]
        >>> c.linhas[2].bloco_mp = 1
        >>> c.buscar_bloco(0)
        1
        >>> c.buscar_bloco(4)

        '''
        hit_or_miss:int|None = None
        for i in range (4):
            linha = self.linhas[i]
            if linha.bloco_mp == bloco_flor and linha.estado != Moesi.I:
                hit_or_miss = i
                break
        return hit_or_miss
    
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

    def imprime_mp(self):
        '''
        Imprime como está os dados da MP
        '''

        print("\n=== Estado da MP ===")
        for i, bloco in enumerate(self.estufa):
            print(f"Linha {i}: Bloco MP {bloco}")

    
    def write_back(self, cache_linha: Linha):
        '''
        Passa os dados da linha da cache de volta para a memória principal
        '''
        localizacao_mp = cache_linha.bloco_mp
        self.estufa[localizacao_mp] = cache_linha.dados.copy()
        
    def verifica_estado(self, linha_substituida: Linha):

        '''
        Corrige os estados das caches quando uma linha em estado 'Owned (O)' é substituída.
        Promove uma linha em estado 'Shared (S)' para 'Owned (O)', se aplicável.
        '''

        linha_promovida = False  # Flag para evitar múltiplas promoções
        bloco_substituido = linha_substituida.bloco_mp

        # Percorre todas as caches
        for florista_cache in self.floristas:
            for linha in florista_cache.linhas:
                if linha.bloco_mp == bloco_substituido and linha.estado == Moesi.S:
                    if not linha_promovida:
                        # Promove a primeira linha encontrada em estado Shared
                        linha.estado = Moesi.O
                        linha_promovida = True
                        print(f"Linha promovida para Owned em cache.")
                    else:
                        # Linhas subsequentes permanecem em estado Shared
                        linha.estado = Moesi.S

        # Caso não tenha mais nenhuma outra cache em estado Shared, escreve o dado na MP
        if not linha_promovida:
            self.write_back(linha_substituida)
    
                    
    def leitura(self, florista: Florista, flor: int):

        ''' Realiza a leitura de uma flor por um florista específico.
        Busca em outras caches caso o dado não esteja presente na cache local.
        '''

        print("\nLeitura:", florista.name, "Flor:", flor)

        florista_cache = self.floristas[florista.value]  # Obtemos a cache do florista
        bloco_flor = bloco(flor)  # Calcula o bloco da memória principal
        posicao = pos_no_bloco(flor)  # Calcula a posição dentro do bloco

        # Verifica se o bloco está na cache local
        linha_cache = florista_cache.buscar_bloco(bloco(flor))
        if linha_cache is not None:
            # Hit: A flor está na cache
            print(f"\nFlor encontrada!" 
                  f"\nQuantidade:{florista_cache.linhas[linha_cache].dados[posicao]}" 
                  f"\nEstado:{florista_cache.linhas[linha_cache].estado}")

            self.imprimir_caches() #TESTE
            self.imprime_mp() #TESTE

            return florista_cache.linhas[linha_cache].dados[posicao]

        # Miss: Verificar as outras caches
        print("Flor não encontrada! Verificando com outros floristas...")
        for i, outro_florista in enumerate(self.floristas):
            if i == florista.value:  # Não verificar a cache do florista atual
                continue
            linha_outro_florista = outro_florista.buscar_bloco(bloco(flor))

            if linha_outro_florista is not None:
                # Dado encontrado em outra cache
                linha = outro_florista.linhas[linha_outro_florista]
                print(f"\nFlor encontrada com florista {Florista(i).name}!"
                      f"\nQuantidade {linha.dados[posicao]}" 
                      f"\nEstado: {linha.estado.name}")

                if linha.estado in (Moesi.M, Moesi.E):
                    # Transferir dados e atualizar estados
                    linha.estado = Moesi.O
                    
                nova_linha = florista_cache.linhas[florista_cache.fifo_contador]

                # Caso um estado owned seja substituido
                if nova_linha.estado == Moesi.O:
                    self.verifica_estado(nova_linha)

                # Caso um estado modified seja substituido 
                if nova_linha.estado == Moesi.M:
                    self.write_back(nova_linha)

                florista_cache.fifo_contador = (florista_cache.fifo_contador + 1) % 4
                nova_linha.dados = linha.dados.copy()
                nova_linha.bloco_mp = linha.bloco_mp
                nova_linha.estado = Moesi.S  # Compartilhado
                print("Dado transferido. Estado atualizado para Shared.")

                self.imprimir_caches() #TESTE
                self.imprime_mp() #TESTE

                return nova_linha.dados[posicao]           

        # Nenhuma outra cache possui o dado, buscar na memória principal
        print("Bloco não encontrado em nenhuma cache. Carregando da memória principal...")
        linha_cache_mp = florista_cache.linhas[florista_cache.fifo_contador]
        print(linha_cache_mp)

        #Caso um estado owned seja substituido
        if linha_cache_mp.estado == Moesi.O:
            self.verifica_estado(nova_linha)

        florista_cache.fifo_contador = (florista_cache.fifo_contador + 1) % 4
        linha_cache_mp.dados = self.estufa[bloco_flor].copy()
        linha_cache_mp.bloco_mp = bloco_flor
        linha_cache_mp.estado = Moesi.E  # Estado inicial ao carregar da MP
        print(f"Bloco carregado!" 
              f"\nQuantidade: {linha_cache_mp.dados[posicao]}"
                f"\nEstado: {linha_cache_mp.estado}")

        self.imprimir_caches() #TESTE
        self.imprime_mp() #TESTE

        return linha_cache_mp.dados[posicao]
    
    def escrita(self, florista: Florista, flor: int, novo_valor: int) -> int:
        ''' Realizar uma operação de escrita na cache, alterando o valor original de algum elemento
        do estoque de flores. Isso é feito seguindo o protocolo MOESI, garantindo a coerência entre
        múltiplas caches e a memória principal. O algoritmo de substituição utilizado é o FIFO e a
        política de escrita é o write-back (os dados modificados são escritos na memória principal
        somente quando são substituídos na cache.). Retorna o próprio novo_valor para verificar a
        conclusão da função.'''

        # Definição de dados iniciais
        bloco_flor:int = bloco(flor)
        pos_no_bloco_flor:int = pos_no_bloco(flor)
        florista_certo:Cache = self.floristas[florista.value]
        
        # Procura da cache 
        hit_or_miss:int|None = florista_certo.buscar_bloco(bloco_flor)

        # Caso do Hit, ou seja, encontramos uma linha não inválida na nossa cache com o bloco certo
        if hit_or_miss is not None:
            linha:Linha = florista_certo.linhas[hit_or_miss]
            if linha.estado in [Moesi.M, Moesi.O, Moesi.S]: # Atualiza na MP
                self.estufa[bloco_flor] = linha.dados
                if linha.estado != Moesi.M:
                    for i in range(4):
                        if i != florista.value:
                            invalida:int|None = self.floristas[i].buscar_bloco(bloco_flor)
                            if invalida is not None:
                                self.floristas[i].linhas[invalida].estado = Moesi.I
            linha.estado = Moesi.M
            dados_modificados:list[int] = linha.dados[:]
            dados_modificados[pos_no_bloco_flor] = novo_valor
            linha.dados = dados_modificados

        # Caso do Miss, ou seja, não encontramos uma linha válida na nossa cache com o bloco certo
        # e vamos ter que fazer uma substiuição segundo o algoritmo Fifo
        else: # hit_or_miss is None
            
            # Aplicação da política Write Back
            substituida:Linha = florista_certo.linhas[florista_certo.fifo_contador]
            promovida:int|None = None
            # Caso da linha substituida ter estado O e há uma linha em outra cache com S que é
            # promovida a O, sem necessidade de escrever de volta na memória 
            if substituida.estado == Moesi.O:
                for i in range(4):
                    if i != florista.value:
                        promovida = self.floristas[i].buscar_bloco(substituida.bloco_mp)
                        if promovida is not None: # Nesse caso há uma outra linha com estado S
                            self.floristas[i].linhas[promovida].estado = Moesi.O
                            break
            # Caso linha substituida ter estado O, mas não haver linha S em outra cache,
            # ou linha substituida ter estado M, aí precisa escrever de volta na memória
            if promovida is None or substituida.estado == Moesi.M:
                self.estufa[substituida.bloco_mp] = substituida.dados

            # Invalidação das linhas das outras caches
            for i in range(4):
                if i != florista.value:
                    invalida = self.floristas[i].buscar_bloco(bloco_flor)
                    if invalida is not None:
                        linha_invalida:Linha = self.floristas[i].linhas[invalida]
                        # Deixei repetitivo mesmo para ficar fácil de ver o que acontece com cada
                        # linha que tentamos inválidar
                        match linha_invalida.estado:
                            case Moesi.E: # Linha é invalidada e não procura outras linhas
                               linha_invalida.estado = Moesi.I
                               break 
                            case Moesi.M: # Atualiza na MP e linha é invalidada e não procura outras linhas
                                self.estufa[linha_invalida.bloco_mp] = linha_invalida.dados
                                linha_invalida.estado = Moesi.I
                                break 
                            case Moesi.S: # Linha é invalidada
                                linha_invalida.estado = Moesi.I
                            case Moesi.O: # Atualiza na MP e linha é invalidada
                                self.estufa[linha_invalida.bloco_mp] = linha_invalida.dados
                                linha_invalida.estado = Moesi.I

            
            dados_modificados = self.estufa[bloco_flor][:]
            dados_modificados[pos_no_bloco_flor] = novo_valor
            nova_linha:Linha = Linha()
            nova_linha.dados = dados_modificados
            nova_linha.estado = Moesi.M
            nova_linha.bloco_mp = bloco_flor
            florista_certo.linhas[florista_certo.fifo_contador] = nova_linha
            florista_certo.fifo_contador = (florista_certo.fifo_contador + 1) % 4

        return novo_valor

def bloco(flor: int) -> int:
    ''' Função que calcula o bloco na memória principal que determinada flor (posição geral entre 0
    e 128) está presente'''
    return flor // 4

def pos_no_bloco(flor: int) -> int:
    ''' Função que calcula a posição que uma flor (posição geral entre 0 e 128) se encontra dentro
    do bloco da memória principal.'''
    return flor % 4
