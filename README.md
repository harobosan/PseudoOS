# PseudoOS

## Dependências: python3 e make

    $ apt update
    $ apt install python3 make
    $ apt install pip
    $ make install

## Testes:

    $ make static

## Executar com configurações padrão:

    $ make

## Executar com configurações diferentes:

    $ make run <args>

## Os argumentos passados através de make run são do formato:

    $ <argname>-<argvalue1>-<argvalue2>-<argvalue3>

## Tipos de argumentos:
### log-< int >

    Nível de verbose dos outputs do Pseudo-OS.

    0. Mínimas: apresenta apenas print de instruções e resultado de operações
       de arquivo.
    1. Reduzidas: adiciona print das caracteristicas de um processo quando o
       dispatcher o move para uma fila de execução.
    2. Básicas: adiciona informações das operações de arquivo quando se tenta execu-
       ta-las e avisos de [ERRO] para quando um processo tenta alocar recursos impo-
       ssíveis.
    3. WARN: adiciona avisos de [WARN] gerados quando um processo tenta alocar
       recursos mas não consegue no momento. 
    4. INFO: adiciona avisos de [INFO] gerados quando um processo consegue alocar
       algum recurso.
    5. Estado de ciclo: adiciona informações do ciclo de execução, apresentando o
       estado das filas de chegada, preparo, execução e espera de dispositivos ao
       fim de cada ciclo.
    6. Armazenamento e Memória: adiciona informações do estado da memória e de disco
       ao fim de cada ciclo. 

    Default: log-6

    ex.:

    $ make run log-3

### cycles-< int >

    Definição da quantidade de ciclos de execução que o sistema vai realizar, parando
    no dado ciclo mesmo sem ter completado todos os processos ou continuando até
    terminar todos os processos caso seja cycles-0. Útil para visualizar rapidamente
    os resultados de um determinado ciclo. (Recomenda-se utilizar junto de log-6 para
    mais informações do ciclo).

    Default: cycles-0

    ex.:

    $ make run log-6 cycles-3

### proc-< str >

    Path para o arquivo de processos. Não consegue ler arquivos com '-'
    no nome, renomeie antes de executar.

    Default: proc-tests/processes.txt

    ex.:

    $ make run tests/another_processes.txt

### file-< str >

    Path para o arquivo de sistema de arquivos. Não consegue ler arquivo com '-'
    no nome, renomeie antes de executar.

    Default: file-tests/files.txt

    ex.:

    $ make run file-tests/another_files.txt

### cmode-< time / cycle >

    Modo de operação do clock.

     time. quantum medido em millisegundos
    cycle. para quantum de ciclos do CPU

    Default: cmode-time

    ex.:

    $ make run cmode-cycle

### fmode-< synchronous / syncbatch / asynchronous >

    Modo de operação do sistema de arquivos, define em que momentos as operações de
    arquivos serão executadas.

     synchronous. Executa as operações junto das instruções do processo associado,
                  uma operação por instrução, podendo acabar o processo sem comple-
                  tar todas as operações.
       syncbatch. Executa as operações todas de uma vez após o processo terminar
                  todas as suas instruções, não é afetado pela preempção destes
                  processos.
    asynchronous. Executa as operações todas de uma vez apenas após todos os proce-
                  ssos terminarem de executar, não é afetado pela preempção destes
                  processos nem pela ordem execução dos processos.

    Default: fmode-synchronous

    ex.:

    $ make run fmode-syncbatch

### slices-< int >

    Definição dos time-slices das filas de escalonamento round robin. Pode receber
    multiplos argumentos separados por - e a quantidade de filas no escalonar será
    o número de argumentos +1 (fila de alta prioridade FIFO)

    Default: slices-1-1-2

    ex.:

    $ make run slices-2-4-8

### memory-< int >

    Definição da quantidade de memória que o sistema possui.

    Default: memory-1024

    ex.:

    $ make run memory-128

### reserved-< int >

    Definição da partição da memória principal reservada para processos de alta
    prioridade.

    Default: reserved-64

    ex.:

    $ make run memory-128 reserved-32

### devices-< str >
    Definição da quantidade e nome de cada dispositivo do sitemas, pode receber
    multiplos argumentos e nomes e gera um dispositivo mapeado em ordem para cada
    argumento.

    Default: devices-IMP1-IMP2-SCAN-MODN-SAT1-SAT2

    ex.:

    $ make run devices-SATA_1-SATA_2-SCANNER
