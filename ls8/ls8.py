#!/usr/bin/env python3

"""Main."""

"""CPU functionality."""


# /usr/local/bin/python3 /Users/tadepew/Desktop/LambdaProjects/Computer-Architecture/ls8/ls8.py /Users/tadepew/Desktop/LambdaProjects/Computer-Architecture/ls8/examples/

#  /usr/local/bin/python3 ls8.py mult.ls8




import sys
from os import path
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # available memory

        # 8 registers (variables) R0-R7 *general purpose register*
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.sp = self.reg[7]
        # array with values to store
        self.pc = 0  # program counter, index of the current instruction *special purpose register*
        self.ir = 0  # instruction register
        # like the 'intermediary' for what is from the program and what stores in reg/ram
        self.mar = 0  # memory address register
        self.mdr = 0  # memory data register

        self.fl = 0

        self.running = False

        # branch table for instructions
        self.instructions = {
            0b10000010: self.handle_ldi,
            0b01000111: self.handle_prn,
            0b10100010: self.handle_mul,
            0b10100000: self.handle_add,
            0b00000001: self.handle_hlt,
            0b10101000: self.handle_and,
            0b10100111: self.handle_cmp,
            0b01100110: self.handle_dec,
            0b10100011: self.handle_div,
            0b01100101: self.handle_inc,
            0b01101001: self.handle_not,
            0b10101010: self.handle_or,
            0b10101011: self.handle_xor,
            0b01000110: self.pop,
            0b01000101: self.push

        }

        # branch tablef or operations
        self.alu_operations = {
            'MUL': self.alu_mul,
            'ADD': self.alu_add,
            'AND': self.alu_and,
            'CMP': self.alu_cmp,
            'DEC': self.alu_dec,
            'DIV': self.alu_div,
            'INC': self.alu_inc,
            'NOT': self.alu_not,
            'OR': self.alu_or,
            'XOR': self.alu_xor,
        }

    def load(self):
        """Load a program into memory."""

        self.mar = 0

        # For now, we've just hardcoded a program:

        program = sys.argv[1]

        with open(program) as file:
            for line in file:
                # if the line is a line break or a comment, don't add to memory
                line = line.split("#")
                try:
                    self.mdr = int(line[0], 2)  # only read the command code
                except ValueError:
                    continue
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

    # ALU = math functions for the computer to do
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op in self.alu_operations:
            self.alu_operations[op](reg_a, reg_b)

        else:
            raise Exception("Unsupported ALU operation")

    def alu_add(self, reg_a, reg_b):
        self.mar = self.ram_read(reg_b)
        self.mdr = self.reg[self.mar]
        self.mar = self.ram_read(reg_a)
        self.mdr = self.mdr + self.reg[self.mar]
        self.reg[self.mar] = self.mar

    def alu_mul(self, reg_a, reg_b):
        self.mar = self.ram_read(reg_b)
        self.mdr = self.reg[self.mar]
        self.mar = self.ram_read(reg_a)
        self.mdr = self.mdr * self.reg[self.mar]
        self.reg[self.mar] = self.mdr

    def alu_and(self, reg_a, reg_b):
        self.mar = self.ram_read(reg_b)
        self.mdr = self.reg[self.mar]
        self.mar = self.ram_read(reg_a)
        self.mdr = self.mdr & self.reg[self.mar]
        self.reg[self.mar] = self.mdr

    def alu_cmp(self, reg_a, reg_b):
        self.mar = self.ram_read(reg_b)
        self.mdr = self.reg[self.mar]
        self.mar = self.ram_read(reg_a)
        self.mdr = self.mdr & self.reg[self.mar]
        if self.mdr > self.reg[self.mar]:
            self.fl = 0b00000100  # reg a > reg b
        elif self.mdr == self.reg[self.mar]:
            self.fl = 0b00000001  # they are equal
        else:
            self.fl = 0b00000010  # reg b > reb a

    def alu_dec(self, reg, unused):
        self.mar = self.ram_read(reg)
        self.mdr = self.reg[self.mar]
        self.mdr -= 1
        self.reg[self.mar] = self.mdr

    def alu_inc(self, reg, unused):
        self.mar = self.ram_read(reg)
        self.mdr = self.reg[self.mar]
        self.mdr += 1
        self.reg[self.mar] = self.mdr

    def alu_div(self, reg_a, reg_b):
        self.mar = self.ram_read(reg_b)
        self.mdr = self.reg[self.mar]
        if self.mdr == 0:
            print('Cannot divide by 0.')
            sys.exit(1)
        self.mar = self.ram_read(reg_a)
        self.mdr = self.reg[self.mar] / self.mdr  # floor division?
        self.reg[self.mar] = self.mdr

    def alu_not(self, reg, unused):
        self.mar = self.ram_read(reg)
        self.mdr = self.reg[self.mar]
        self.mdr = ~self.mdr
        self.reg[self.mar] = self.mdr

    def alu_or(self, reg_a, reg_b):
        self.mar = self.ram_read(reg_b)
        self.mdr = self.reg[self.mar]
        self.mar = self.ram_read(reg_a)
        self.mdr = self.mdr | self.reg[self.mar]
        self.reg[self.mar] = self.mdr

    def alu_xor(self, reg_a, reg_b):
        self.mar = self.ram_read(reg_b)
        self.mdr = self.reg[self.mar]
        self.mar = self.ram_read(reg_a)
        self.mdr = self.mdr ^ self.reg[self.mar]
        self.reg[self.mar] = self.mdr

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
        self.running = True
        while self.running:

            self.ir = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            aa = self.ir >> 6
            num_operands = (aa + 1)

            # if self.ir in self.instructions:

            #     if num_operands == 0:
            #         self.instructions[self.ir]()

            #     elif num_operands == 1:
            #         self.instructions[self.ir](operand_a)

            #     else:
            #         self.instructions[self.ir](operand_a, operand_b)

            if self.ir in self.instructions:
                self.instructions[self.ir]()

            else:
                print(f'Unknown instruction {self.ir} at address{self.pc}')
                sys.exit(1)

            self.pc += num_operands

    def ram_read(self, address):  # memory address
        return self.ram[address]

    def ram_write(self, data, address):
        # mdr #mar
        self.ram[address] = data

    def handle_ldi(self):
        self.mar = self.ram_read(self.pc + 1)
        self.mdr = self.ram_read(self.pc + 2)
        self.reg[self.mar] = self.mdr
        # self.pc += 3
        # 3 byte instruction
        # assigning value of a register to an integer

    def handle_prn(self):
        self.mar = self.ram_read(self.pc + 1)
        print(self.reg[self.mar])
        # self.pc += 2
        # 2 byte instruction

    def handle_mul(self):
        self.alu('MUL', self.pc + 1, self.pc + 2)
        # self.pc += 3

    def handle_add(self):
        self.alu('ADD', self.pc + 1, self.pc + 2)
        # self.pc += 3

    def handle_and(self):
        self.alu('AND', self.pc + 1, self.pc + 2)
        # self.pc += 3

    def handle_cmp(self):
        self.alu('CMP', self.pc + 1, self.pc + 2)
        # self.pc += 3

    def handle_dec(self):
        self.alu('DEC', self.pc + 1, None)
        # self.pc += 2

    def handle_inc(self):
        self.alu('INC', self.pc + 1, None)
        # self.pc += 2

    def handle_div(self):
        self.alu('DIV', self.pc + 1, self.pc + 2)
        # self.pc += 3

    def handle_not(self):
        self.alu('NOT', self.pc + 1, None)
        # self.pc += 2

    def handle_or(self):
        self.alu('OR', self.pc + 1, self.pc + 2)
        # self.pc += 3

    def handle_xor(self):
        self.alu('XOR', self.pc + 1, self.pc + 2)
        # self.pc += 3

    def pop(self):
        self.mar = self.ram_read(self.pc + 1)
        self.ram[self.mar] = self.ram[self.sp]
        self.sp += 1

    def push(self):
        self.sp -= 1
        self.mar = self.ram_read(self.pc + 1)
        self.ram[self.sp] = self.ram[self.mar]

    def handle_hlt(self):
        self.running = False
        # self.pc += 1


cpu = CPU()

cpu.load()
cpu.run()
