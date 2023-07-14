# PseudoOS

Dependências: python3 e make
    $ apt update
    $ apt install python3 make
    $ apt install pip
    $ make install

Testes:
    $ make install
    $ make static

Executar com configurações padrão:
    $ make

Executar com configurações diferentes:
    $ make run <args>

Os argumentos passados através de make run são do formato:
    $ <argname>-<argvalue1>-<argvalue2>-<argvalue3>

Tipos de argumentos:
log-< int >
    Nível de verbose dos outputs do Pseudo-OS

    $ make run log-6

proc-< str >
    Path para o arquivo de processos

    $ make run tests/processes.txt

file-< str >
    Path para o arquivo de sistema de arquivos

    $ make run file-tests/files.txt

cmode-< time | cycle >
    Modo de operação do clock, pode ser 'time' para quantum medido em milisegundos
    ou 'cycle' para quantum de ciclos do CPU

fmode-< synchronous | asynchronous | batch >
    Modo de operação do sistema de arquivos, define em que momentos as operações de
    arquivos serão executadas

slices-< int >
    Definição dos time-slices das filas de escalonamento round robin. Pode receber
    multiplos argumentos separados por - e a quantidade de filas no escalonar será
    o número de argumentos +1 (fila de alta prioridade FIFO)

    $ make run slices-1-1-2

memory-< int >
    Definição da quantidade de memória que o sistema possui.

    $ make run memory-1024

reserved-< int >
    Definição da partição da memória principal reservada para processos de alta
    prioridade.

    $ make run memory-1024 reserved-64

devices-< str >
    Definição da quantidade e nome de cada dispositivo do sitemas, pode receber
    multiplos argumentos e nomes e gera um dispositivo mapeado em ordem para cada
    argumento.

    $ make run devices-SATA_1-SATA_2-SCANNER
