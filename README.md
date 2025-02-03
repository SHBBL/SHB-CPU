# SHB CPU

## ⚠️Doesn't support screen⚠️

## CPU:
A simple custom 8 bit CPU was designed using Logisim, featuring its own instruction set. To program it, a custom assembler was written in Python, translating assembly code into machine code for execution. This setup allows for experimenting with CPU design and low-level programming.

## Instruction Set:
 ```
0  -  000 - 000 - 00  - 00  - 000 - 00000000
mem - r/w - jmp - alu - reg - in2 - mov_8bit_data

```
## Installation:
```
git clone https://github.com/SHBBL/SHB-CPU.git
cd SHB-CPU
vim program.shb
python Assembler.py -f program.shb -o out
```
## Usage:
``
Usage: 
  Assembler.py [-h] -f -o Assembler.py: error: the following arguments are required: -f/--file, -o/--output
``

## Screenshots:
![alt text](https://github.com/SHBBL/SHB-CPU/blob/main/blob/8bit_cpu.png)
![alt text](https://github.com/SHBBL/SHB-CPU/blob/main/blob/assembler.png)

## dependencies:
* Logism
