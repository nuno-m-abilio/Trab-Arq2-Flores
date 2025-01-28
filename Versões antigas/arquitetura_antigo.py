import io


class Instrucao:
    ''' Classe que representa uma Instrução a ser executada na Arquitetura. Cada instrução tem um
    Opcode que determina sua ação e até 3 valores inteiros de referência que utiliza para isso.'''

    Opcode:str
    a:int
    b:int
    c:int

    def __init__(self, instStr:str) -> None:
        ''' O construtor toma como entrada uma String e faz seu processamento/decodificação,
        separando o Opcode dos valores referenciais. Para isso, considera-se que a string está no
        formato correto de "Opcode A, B, C", com A, B e C podendo ser valores imediatos (a, b, c),
        número dos registradores (ra, rb, rc) ou vazios. O formato "Opcode ra, b(rc)" também é
        válido Para as operções que tem somente 1, 2 ou nenhum operador, os valores b e c ficam
        marcados com o valor inválido -1.
        
        >>> x = 'add r2,r31,r100'
        >>> y = Instrucao(x)
        >>> y.Opcode
        'add'
        >>> y.a
        2
        >>> y.b
        31
        >>> y.c
        100

        >>> x = 'lw r2,31(r100)'
        >>> y = Instrucao(x)
        >>> y.Opcode
        'lw'
        >>> y.a
        2
        >>> y.b
        31
        >>> y.c
        100
        
        >>> x = 'not r2, r32'
        >>> y = Instrucao(x)
        >>> y.Opcode
        'not'
        >>> y.a
        2
        >>> y.b
        32
        >>> y.c
        -1

        >>> x = 'jal 0'
        >>> y = Instrucao(x)
        >>> y.Opcode
        'jal'
        >>> y.a
        0
        >>> y.b
        -1
        >>> y.c
        -1
        
        >>> x = 'ret'
        >>> y = Instrucao(x)
        >>> y.Opcode
        'ret'
        >>> y.a
        -1
        >>> y.b
        -1
        >>> y.c
        -1
        '''

        OpcodeAux = ''
        aAux:str = ''
        bAux:str = ''
        cAux:str = ''
        i:int = 0 
        tam:int = len(instStr)
        while i < tam and instStr[i] != ' ':
            OpcodeAux += instStr[i]
            i += 1
        i += 1 
        if i < tam:
            while i < tam and instStr[i] != ',':
                if instStr[i] != 'r':
                    aAux += instStr[i]
                i += 1
            i += 1
            if i < tam:
                while i < tam and instStr[i] != ',' and instStr[i] != '(':
                    if instStr[i] != 'r' and instStr[i] != ' ':
                        bAux += instStr[i]
                    i += 1
                i += 1
                if i < tam:
                    while i < tam  and instStr[i] != ')':
                        if instStr[i] != 'r' and instStr[i] != ' ':
                            cAux += instStr[i]
                        i += 1
                else:
                    cAux = '-1'
            else:
                bAux, cAux = '-1', '-1'
        else:
            aAux, bAux, cAux = '-1', '-1', '-1'
        self.Opcode = OpcodeAux
        self.a = int(aAux)
        self.b = int(bAux)
        self.c = int(cAux)


class CicloDeInstrucao:
    ''' Classe que representa um ciclo de instrução simplificado com 2 etapas: leitura, que
    armazena uma String com a instrução lida; e decodificacao + separação de operandos + execução,
    que armazena também uma String (por questões de praticidade na hora de printá-lo), que logo após
    ter um valor atribuído, será decodificada e executada.'''

    leitura:str
    execucao:str

    def __init__(self) -> None:
        ''' Construtor padrão com valores inválidos padrão. O valor 'Início é importante, pois ao
        tentar ser executado como uma instrução, gerará um print que evidenciará o início do Ciclo
        de Instruções'''
        self.leitura = 'Inicio'
        self.execucao = ''


class LinhaCacheInstr:
    ''' Classe que representa um bloco da memória Cache de Instruções (str). Seus atributos são a
    tag dos valores que ela armazena nos endereços, um vetor com esses endereços e o número de
    vezes que ela foi acessada.'''

    tag:int|None
    enderecos:list[str]
    acessos:int

    def __init__(self, palavrasPorLinha:int) -> None:
        ''' Construtor padrão da classe, que inicializa-a sem uma tag, com "palavrasPorLinha"
        endereços e sem acessos.'''
        self.tag = None
        self.enderecos = [''] * palavrasPorLinha
        self.acessos = 0


class LinhaCacheDados:
    ''' Classe que representa um bloco da memória Cache de Dados (int). Seus atributos são a tag
    dos valores que ela armazena nos endereços, um vetor com esses endereços e o número de vezes
    que ela foi acessada.'''

    tag:int|None
    enderecos:list[int]
    acessos:int

    def __init__(self, palavrasPorLinha:int) -> None:
        ''' Construtor padrão da classe, que inicializa-a sem uma tag, com "palavrasPorLinha"
        endereços e sem acessos.'''
        self.tag = None
        self.enderecos = [0] * palavrasPorLinha
        self.acessos = 0


class Processador:
    ''' Classe que representa o processador da Arquitetura, tendo como campos uma lista de inteiros
    que representa os 32 Registradores de Uso Geral, inteiros para representar o Contador de
    Programa (PC), Ponteiro da Pilha (RSP) e Endereço de Retorno (RA), além de um bool que indica
    se houve oveflow na última operação.'''

    Registradores: list[int]
    PC:int
    RSP:int
    RA:int
    OF:bool

    def __init__(self) -> None:
        ''' Construtor padrão da classe Processador.'''
        self.Registradores = [0] * 32
        self.PC = 0
        self.RSP = 0
        self.RA = 0
        self.OF = False


class Arquitetura:
    ''' Classe que simulada uma arquitetura simplificada com memória cache, composta por um
    conjunto de instruções aritméticas, lógicas, de desvio e de movimentação de dados entre
    registradores e memória. Nela, há campos específicos para o processador, memória principal
    (MP), cache de instruções, cache de dados, ciclo de instrução e informações da memória.'''
    
    processador:Processador
    MP:list[list[int|str]]
    cacheInst:list[list[LinhaCacheInstr]]
    cacheDados:list[list[LinhaCacheDados]]
    cicloDeInstrucao:CicloDeInstrucao
    infoMemoria:list[int]

    def __init__(self, palavrasPorLinha:int, linhasPorConjunto:int, numConjuntos:int, tamMP:int) -> None:
        ''' Construtor padrão da arquitetura que inicializa o processador e o ciclo de instrução em
        suas formas padrão e as memórias principal e cache conforme os parâmetros passados na
        entrada. Ressalta-se aqui que a MP é dividida em blocos de tamanho igual às linhas da
        cache, existindo a possibilidade de haver um último bloco menor que os demais, mas sem que
        isso influencie na cache. Além disso, no atributo que armazena as especificações da
        memória, estão as informações de palavras por linha da cache [0], linhas por conjunto [1],
        total de conjuntos [2] e tamanho da MP [3] respectivamente '''

        # Correção de parametros inválidos realizados na main

        self.processador = Processador()
        self.MP = [[''] * palavrasPorLinha for _ in range(int(tamMP / palavrasPorLinha))]
        corretorBlocosMP:int = tamMP % palavrasPorLinha
        if corretorBlocosMP > 0:
            self.MP += [[''] * corretorBlocosMP]
        self.cacheInst = [[LinhaCacheInstr(palavrasPorLinha) for _ in range(linhasPorConjunto)] for _ in range(numConjuntos)]
        self.cacheDados = [[LinhaCacheDados(palavrasPorLinha) for _ in range(linhasPorConjunto)]for _ in range(numConjuntos)]
        self.cicloDeInstrucao = CicloDeInstrucao()
        self.infoMemoria = [palavrasPorLinha, linhasPorConjunto, numConjuntos, tamMP]
    

    def carregarInstrEmMP(self, arquivoDeOperacoes:io.TextIOWrapper) -> None:
        ''' Método que toma como entrada um arquivo de texto aberto com instruções e escreve essas
        instruções na MP da arquitetura. Cada linha do arquivo tem uma instrução que é colocada em
        um endereço da MP.'''
        instLida:str = arquivoDeOperacoes.readline().strip()
        i:int = 0
        while instLida:
            self.MP[blocoNaMP(self, i)][localNoBloco(self, i)] = instLida
            instLida = arquivoDeOperacoes.readline().strip()
            i += 1


    def rodarSequenciaInst(self) -> None:
        ''' Método que lê e executa sequencialmente as instruções da memória a partir do endereço
        armazenado em PC, printando as informações da arquitetura a cada ciclo. O critério de
        parada da função é quando um valor inválido de instrução tenta ser lido.'''
        continua = self.rodarInst()
        self.printInfo()
        while continua:
            continua = self.rodarInst()
            self.printInfo()


    def rodarInst(self) -> bool:
        ''' Método que lê e executa uma operação alterando o Ciclo de Instruções. Ele coloca a
        Instrução que está em leitura no espaço da execução, então decodifica-a e executa-a mudando
        o PC. Em seguida, lê-se uma nova operação segundo essa nova informação do PC, coloca-a na
        leitura e retorna True, caso a execução tenha sido válida, e False, caso contrário.'''
        self.cicloDeInstrucao.execucao = self.cicloDeInstrucao.leitura
        instrucaoValida = self.executaInstrucao(Instrucao(self.cicloDeInstrucao.execucao))
        self.cicloDeInstrucao.leitura = self.lerInst(self.processador.PC)
        return instrucaoValida


    def lerInst(self, endereco:int) -> str:
        ''' Método que retorna uma string com a instrução em "endereço". Caso o bloco da instrução
        não esteja na cache, ele é colocado nela seguindo a política de substituição LFU.'''
        tagInst:int = tag(self, endereco)
        conjInst:int = conjNaCache(self, endereco)
        i:int = 0
        tagAtual:int|None = self.cacheInst[conjInst][i].tag
        linhasPorConj:int = self.infoMemoria[1]
        while tagAtual is not None and tagAtual != tagInst and i < (linhasPorConj - 1):
            i += 1
            tagAtual = self.cacheInst[conjInst][i].tag
        if tagAtual != tagInst:
            if tagAtual is not None:
                # Vamos fazer substituição adotando a política LFU
                i = 0
                for j in range(linhasPorConj):
                    if self.cacheInst[conjInst][j].acessos < self.cacheInst[conjInst][i].acessos:
                        i = j
                self.cacheInst[conjInst][i].acessos = 0
            self.cacheInst[conjInst][i].enderecos = self.MP[blocoNaMP(self, endereco)] # type: ignore
            self.cacheInst[conjInst][i].tag = tagInst
        self.cacheInst[conjInst][i].acessos += 1 
        # O str() no return serve para, ainda que um a linha de inteiros entre indevidamente na cache de instruções,
        # a saida seja uma string inválida que para o ciclo de instruçõesn (não ser aqui onde dá erro)
        return str(self.cacheInst[conjInst][i].enderecos[localNoBloco(self, endereco)])


    def executaInstrucao(self, instrucao:Instrucao) -> bool:
        '''Função que tenta executar uma determinada instrução em uma arquitetura. Caso execute,
        retorna True, caso contrário, False.'''
        match instrucao.Opcode:
            case 'Inicio':
                print('\nIniciando Ciclo de Instruções')
            case 'add':
                resultado:int = self.processador.Registradores[instrucao.b] + self.processador.Registradores[instrucao.c]
                self.processador.Registradores[instrucao.a] = resultado
                self.processador.OF = (resultado > (2**63 - 1)) or (resultado < -(2**63))
                self.processador.PC += 1
            case 'addi':
                resultado = self.processador.Registradores[instrucao.b] + instrucao.c
                self.processador.Registradores[instrucao.a] = resultado
                self.processador.OF = (resultado > (2**63 - 1)) or (resultado < -(2**63))
                self.processador.PC += 1
            case 'sub':
                resultado = self.processador.Registradores [instrucao.b] - self.processador.Registradores[instrucao.c]
                self.processador.Registradores[instrucao.a] = resultado
                self.processador.OF = (resultado > (2**63 - 1)) or (resultado < -(2**63))
                self.processador.PC += 1
            case 'subi':
                resultado = self.processador.Registradores[instrucao.b] - instrucao.c
                self.processador.Registradores[instrucao.a] = resultado
                self.processador.OF = (resultado > (2**63 - 1)) or (resultado < -(2**63))
                self.processador.PC += 1
            case 'mul':
                resultado = self.processador.Registradores [instrucao.b] * self.processador.Registradores[instrucao.c]
                self.processador.Registradores[instrucao.a] = resultado
                self.processador.OF = (resultado > (2**63 - 1)) or (resultado < -(2**63))
                self.processador.PC += 1
            case 'div':
                resultado = self.processador.Registradores [instrucao.b] // self.processador.Registradores[instrucao.c]
                self.processador.Registradores[instrucao.a] = resultado
                self.processador.OF = (resultado > (2**63 - 1)) or (resultado < -(2**63))
                self.processador.PC += 1
            case 'not':
                self.processador.Registradores[instrucao.a] = ~ self.processador.Registradores[instrucao.b]
                self.processador.PC += 1
            case 'or':
                self.processador.Registradores[instrucao.a] = self.processador.Registradores[instrucao.b] & self.processador.Registradores[instrucao.c]
                self.processador.PC += 1
            case 'and':
                self.processador.Registradores[instrucao.a] = self.processador.Registradores[instrucao.b] | self.processador.Registradores[instrucao.c]
                self.processador.PC += 1
            case 'blti':
                if self.processador.Registradores[instrucao.a] < self.processador.Registradores[instrucao.b]:
                    self.processador.PC = instrucao.c
                else:
                    self.processador.PC += 1
            case 'bgti':
                if self.processador.Registradores[instrucao.a] > self.processador.Registradores[instrucao.b]:
                    self.processador.PC = instrucao.c
                else:
                    self.processador.PC += 1
            case 'beqi':
                if self.processador.Registradores[instrucao.a] == self.processador.Registradores[instrucao.b]:
                    self.processador.PC = instrucao.c
                else:
                    self.processador.PC += 1
            case 'blt':
                if self.processador.Registradores[instrucao.a] < self.processador.Registradores[instrucao.b]:
                    self.processador.PC = self.processador.Registradores[instrucao.c]
                else:
                    self.processador.PC += 1
            case 'bgt':
                if self.processador.Registradores[instrucao.a] > self.processador.Registradores[instrucao.b]:
                    self.processador.PC = self.processador.Registradores[instrucao.c]
                else:
                    self.processador.PC += 1
            case 'beq':
                if self.processador.Registradores[instrucao.a] == self.processador.Registradores[instrucao.b]:
                    self.processador.PC = self.processador.Registradores[instrucao.c]
                else:
                    self.processador.PC += 1
            case 'jr':
                self.processador.PC = self.processador.Registradores[instrucao.a]
            case 'jof':
                if self.processador.OF:
                    self.processador.PC = self.processador.Registradores[instrucao.a]
            case 'jal':
                self.processador.RA = self.processador.PC + 1
                self.processador.PC = instrucao.a
            case 'ret':
                self.processador.PC = self.processador.RA
            case 'lw':
                self.processador.Registradores[instrucao.a] = self.lerDados(instrucao.b + self.processador.Registradores[instrucao.c])
                self.processador.PC += 1
            case 'sw':
                endereco = instrucao.b + self.processador.Registradores[instrucao.c]
                self.MP[blocoNaMP(self, endereco)][localNoBloco(self, endereco)] = self.processador.Registradores[instrucao.a] # Valor na MP atualizado
                self.atualizaLinhaCacheDados(endereco) # Valor na Cache Atualizado
                self.processador.PC += 1
            case 'mov':
                self.processador.Registradores[instrucao.a] = self.processador.Registradores[instrucao.b]
                self.processador.PC += 1
            case 'movi':
                self.processador.Registradores[instrucao.a] = instrucao.b
                self.processador.PC += 1
            case _:
                print('Operação Inválida - Fim de sequência de Operações')
                return False
        return True


    def printInfo(self) -> None:
        ''' Printa as informações atuais de uma arquitetura.'''
        print('\n')
        print('Valores armazenados na arquitetura:')
        print('\n')
        print("Ciclo de Instrução:")
        print('[Lido: ', self.cicloDeInstrucao.leitura, ']\n[Executado: ', self.cicloDeInstrucao.execucao, ']')
        print('\n')
        print('Registradores de uso geral:')
        print(self.processador.Registradores)
        print('\n')
        print('Registradores de controle de estado')
        print('PC:', self.processador.PC, '  RSP:', self.processador.RSP, '  RA:', self.processador.RA, '  OF:', self.processador.OF)
        print('\n')
        print('Memória Cache de Instruções:')
        for i in range(self.infoMemoria[2]):
            print('Conjunto', i, ":")
            for j  in range(self.infoMemoria[1]):
                print('    Linha', j, ': ', 'Tag ->', self.cacheInst[i][j].tag, '| Acessos ->', self.cacheInst[i][j].acessos, \
                    '| Registros ->', self.cacheInst[i][j].enderecos)
        print('\n')
        print('Memória Cache de Dados:')
        for i in range(self.infoMemoria[2]):
            print('Conjunto', i, ":")
            for j  in range(self.infoMemoria[1]):
                print('    Linha', j, ': ', 'Tag ->', self.cacheDados[i][j].tag, '| Acessos ->', self.cacheDados[i][j].acessos, \
                    '| Registros ->', self.cacheDados[i][j].enderecos)
        print('\n')  
        print('Memória Principal:')
        print('\n')
        print(self.MP)


    def lerDados(self, endereco:int) -> int:
        ''' Método que retorna um inteiro com o dado do endereço passado por uma instrução. Caso o
        bloco do dado não esteja na cache, ele é colocado nela seguindo a política de substituição
        LFU. (Método usado na "instrução lw".)'''
        tagDados:int = tag(self, endereco)
        conjDados:int = conjNaCache(self, endereco)
        i:int = 0
        tagAtual:int|None = self.cacheDados[conjDados][i].tag
        linhasPorConj:int = self.infoMemoria[1]
        while tagAtual is not None and tagAtual != tagDados and i < (linhasPorConj - 1):
            i += 1
            tagAtual = self.cacheDados[conjDados][i].tag
        if tagAtual != tagDados:
            if tagAtual is not None:
                # Vamos fazer substituição adotando a política LFU
                i = 0
                for j in range(linhasPorConj):
                    if self.cacheDados[conjDados][j].acessos < self.cacheDados[conjDados][i].acessos:
                        i = j
                self.cacheDados[conjDados][i].acessos = 0
            self.cacheDados[conjDados][i].enderecos = self.MP[blocoNaMP(self, endereco)] # type: ignore
            self.cacheDados[conjDados][i].tag = tagDados
        self.cacheDados[conjDados][i].acessos += 1 
        return self.cacheDados[conjDados][i].enderecos[localNoBloco(self, endereco)]


    def atualizaLinhaCacheDados(self, endereco:int):
        ''' Método que atualiza o valor de uma linha da cache de dados com a palavra em "endereco"
        na MP. Caso a linha não esteja na cache, nada acontece. (Método usado na instrução "sw".)
        '''
        tagDados:int = tag(self, endereco)
        conjDados:int = conjNaCache(self, endereco)
        i:int = 0
        tagAtual:int|None = self.cacheDados[conjDados][i].tag
        linhasPorConj:int = self.infoMemoria[1]
        while tagAtual != tagDados and i < (linhasPorConj - 1):
            i += 1
            tagAtual = self.cacheDados[conjDados][i].tag
        if tagAtual == tagDados:
            self.cacheDados[conjDados][i].enderecos = self.MP[blocoNaMP(self, endereco)] # type: ignore


def blocoNaMP(arquitetura:Arquitetura, endereco:int) -> int:
    ''' "Bloco" do endereço na MP.'''
    return endereco // arquitetura.infoMemoria[0] # endereço // nº de palavras na linha


def localNoBloco(arquitetura:Arquitetura, endereco:int) -> int:
    ''' Coordenada da "Palavra" no bloco da MP / linha da cache.'''
    return endereco % arquitetura.infoMemoria[0] # endereço % nº de palavras na linha


def conjNaCache(arquitetura:Arquitetura, endereco:int) -> int:
    ''' "Conjunto" do endereço na cache.'''
    return blocoNaMP(arquitetura, endereco) % arquitetura.infoMemoria[2] # bloco % nº de conjuntos


def tag(arquitetura:Arquitetura, endereco:int) -> int:
    ''' "Tag" do endereço (igual para todos num mesmo bloco na MP).'''
    return blocoNaMP(arquitetura, endereco) // arquitetura.infoMemoria[2] # bloco // nº de conjuntos