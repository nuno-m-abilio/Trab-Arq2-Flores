# Trab-Arq2-Flores
Simulação de Coerência de Cache MOESI - Floricultura

Contextualização:

Este projeto foi desenvolvido para a disciplina Arquitetura e Organização de Computadores 2, ministrada pela Professora Sandra na Universidade Estadual de Maringá (UEM). O trabalho foi realizado pelos alunos: Eduardo Angelo Rozada Minholi (RA: 134932) e Nuno Miguel Mendonça Abilio (RA: 132830)

Descrição do Projeto:

Este programa simula um sistema de coerência de cache utilizando o protocolo MOESI (Modified, Owned, Exclusive, Shared, Invalid) em um contexto metafórico de uma floricultura.

Na simulação:
- A memória principal (MP) é representada por uma estufa, composta por 32 blocos, cada um contendo 4 palavras.
- Os 4 processadores são representados por floristas (Heloise, Josiane, Valeria e Yandre), cada um com sua memória cache.
- Cada cache possui 4 linhas, e o mapeamento é totalmente associativo.
- A substituição segue a política FIFO (First-In, First-Out).
- A escrita segue a política Write-Back.
- O programa permite operações de leitura, escrita, consulta de blocos na MP e impressão do estado da floricultura.

Requisitos: Para executar o programa, é necessário ter instalado Python 3.10 ou superior

Como Executar:
1 - Clone este repositório ou baixe os arquivos main.py e floricultura.py.
2 - No terminal ou prompt de comando, navegue até o diretório onde os arquivos estão salvos.
3 - Execute o comando: python main.py

Funcionamento:
Ao rodar o programa, o usuário interage com um menu textual onde pode:
- Escolher um florista (correspondente a um dos processadores/caches).
- Selecionar uma operação:
    - l - Leitura da quantidade de uma flor no estoque.
    - e - Escrita da quantidade de uma flor no estoque.
    - c - Consulta do bloco de uma flor na MP.
    - i - Imprimir todo o estado da floricultura (caches e MP).
    - s - Sair do programa.
- Escolher a flor sobre a qual deseja realizar a operação.
- O sistema imprime as informações relevantes e garante a coerência dos dados conforme as regras do protocolo MOESI.

Estrutura do Código:
O programa é dividido em dois arquivos principais:
- main.py: Contém o loop interativo que permite ao usuário realizar operações na floricultura.
- floricultura.py: Contém as classes que modelam o sistema de memória, incluindo as caches, a memória principal e a implementação do protocolo MOESI.

Em caso de dúvidas, mande um e-mail para ra13280@uem.br ou ra134932@uem.br