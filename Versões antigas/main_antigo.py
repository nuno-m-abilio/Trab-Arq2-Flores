import arquitetura as arq, argparse, io


# Configurando a chamada dos argumentos na linha de comando
parser = argparse.ArgumentParser()
parser.add_argument('arquivoDeOperacoes', type=str)
parser.add_argument('palavrasPorLinha', type=int)
parser.add_argument('linhasPorConjunto', type=int)
parser.add_argument('numConjuntos', type=int)
parser.add_argument('tamMP', type=int)
args = parser.parse_args()


def main(arquivoDeOperacoes:io.TextIOWrapper, palavrasPorLinha:int, linhasPorConjunto:int, numConjuntos:int, tamMP:int):
    ''' Função que tem interação direta com o usuário, tomando como entrada um arquivo aberto de
    instruções e os dados da memória da arquitetura a ser criada. Caso algum desses dados de
    memória seja inadequado, a própria função requer que o usuário corrija-o. Assim, um objeto da
    classe arquitetura é criado, as instruções são colocadas na MP e então executadas em sequência.
    
    Obs.1: O arquivo de operações lido não deve ter linhas vazias em seu interior, pois assim as
    instruções seguintes não serão lidas devido ao laço while da função funcoes.carregarInstrEmMP.
    De modo semelhante, não é o ideal ter instruções inválidas em seu interior, pois, ao
    encontrá-las, o ciclo de instrução irá se encerrar tentando executá-las.
    '''

    print('"Inicializando simulador de arquitetura simplificada com memória cache"\n')

    while palavrasPorLinha < 1 or palavrasPorLinha > 128:
        palavrasPorLinha = int(input('Valor de palavras por linha da cache inválido. O valor deve'
        'ser um inteiro entre 1 e 128. Por favor, insirar um valor correto:\n'))

    totalPalavrasCaches = 2 * palavrasPorLinha * linhasPorConjunto * numConjuntos

    while tamMP <= (totalPalavrasCaches):
        tamMP = int(input('Valor de palavras da memória principal inválido. O valor deve'
        'ser maior que o total de palavras da cache (%d). Por favor, insirar um valor correto:\n' % totalPalavrasCaches))
    
    print('Informações de memória:')
    print('    -> %d palavras por linha;' % palavrasPorLinha)
    print('    -> %d linhas por conjunto;' % linhasPorConjunto)
    print('    -> %d conjuntos;' % numConjuntos)
    print('    -> %d palavras na memória principal;\n' % tamMP)

    arquitetura = arq.Arquitetura(palavrasPorLinha, linhasPorConjunto, numConjuntos, tamMP)

    arquitetura.carregarInstrEmMP(arquivoDeOperacoes)

    arquitetura.rodarSequenciaInst()


if __name__ == '__main__':
    arquivoDeOperacoes = open(args.arquivoDeOperacoes, 'rt') 
    main(arquivoDeOperacoes, args.palavrasPorLinha, args.linhasPorConjunto, args.numConjuntos, args.tamMP)
    arquivoDeOperacoes.close()