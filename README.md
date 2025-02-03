# SHB CPU

## ⚠️Doesn't support screen⚠️

## CPU:
A simple custom CPU was designed using Logisim, featuring its own instruction set. To program it, a custom assembler was written in Python, translating assembly code into machine code for execution. This setup allows for experimenting with CPU design and low-level programming.

## Instruction Set:
 ```
0  -  000 - 000 - 00  - 00  - 000 - 00000000
mem - r/w - jmp - alu - reg - in2 - mov_8bit_data

```
## Installation:
```
git clone https://github.com/SHBBL/SHB-CPU.git
cd SHB-CPU
```
## Usage:
``
main.exe <rom game from /chip8_emulator/roms>
``

## Screenshots:
![alt text](https://github.com/SHBBL/chip8_emulator/blob/main/blob/invaders.png)
![alt text](https://github.com/SHBBL/chip8_emulator/blob/main/blob/invaders2.png)

## dependencies:
* Logism
