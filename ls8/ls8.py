#!/usr/bin/env python3

"""Main."""

"""CPU functionality."""


# /usr/local/bin/python3 /Users/tadepew/Desktop/LambdaProjects/Computer-Architecture/ls8/ls8.py /Users/tadepew/Desktop/LambdaProjects/Computer-Architecture/ls8/examples/




import sys
from os import path
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256

        self.reg = [0] * 8
        self.pc = 0  # program counter
        self.ir = 0  # instruction register

        self.mar = 0  # mem address register
        self.mdr = 0  # mem data register

        self.fl = [0] * 8

    def load(self):
        """Load a program into memory."""

        self.mar = 0

        # For now, we've just hardcoded a program:

        program = sys.argv[1]

        with open(program) as file:
            for line in file:
                if line[0] == '#' or line[0] == '\n':
                    continue
                self.mdr = int(line[:8], 2)  # only read command code
                self.ram_write(self.mdr, self.mar)
                self.mar += 1
        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # while self.mar < len(program):
        #     self.mdr = program[self.mar]
        #     self.ram_write(self.mdr, self.mar)
        #     self.mar += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            # self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
            self.mar = self.ram_read(reg_b)
            self.mdr = self.reg[self.mar]
            self.mar = self.ram_read(reg_a)
            self.mdr = self.mdr * self.reg[self.mar]
            self.reg[self.mar] = self.mdr

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            self.ir = self.ram_read(self.pc)
            if self.ir == 0b10000010:  # LDI load immediate
                self.mar = self.ram_read(self.pc + 1)
                self.mdr = self.ram_read(self.pc + 2)
                self.reg[self.mar] = self.mdr
                self.pc += 3

            elif self.ir == 0b01000111:  # PRN print register
                self.mar = self.ram_read(self.pc + 1)
                print(self.reg[self.mar])
                self.pc += 2

            elif self.ir == 0b10100010:  # MUL
                self.alu('MUL', self.pc + 1, self.pc + 2)
                self.pc += 3

            elif self.ir == 0b00000001:  # HLT halt
                running = False
                self.pc += 1

            else:
                print(f'Unknown instruction {self.ir} at address{self.pc}')
                sys.exit(1)

    def ram_read(self, memadr):  # memory address
        return self.ram[memadr]

    def ram_write(self, memdata, memadr):
        self.ram[memadr] = memdata


cpu = CPU()

cpu.load()
cpu.run()
