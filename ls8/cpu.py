"""CPU functionality."""

import sys
from os import path


"""Main."""

"""CPU functionality."""


# /usr/local/bin/python3 /Users/tadepew/Desktop/LambdaProjects/Computer-Architecture/ls8/ls8.py /Users/tadepew/Desktop/LambdaProjects/Computer-Architecture/ls8/examples/

#  /usr/local/bin/python3 ls8.py mult.ls8


# the instruction is like a set of wires
# 10000010 IR
# first two wires represent a piece of circuitry that represent operands

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
            0b01000101: self.push,
            0b01010100: self.jmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
            0b01010000: self.call,
            0b00010001: self.ret

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
        # 1st try
        # self.mar = self.ram_read(reg_b)
        # self.mdr = self.reg[self.mar]
        # self.mar = self.ram_read(reg_a)
        # self.mdr = self.mdr + self.reg[self.mar]
        # 2nd try
        # self.mdr = self.reg[reg_b]
        # self.mdr = self.mdr + self.reg[reg_a]
        # self.reg[reg_a] = self.mdr
        self.ram[reg_a] += self.ram[reg_b]

    def alu_mul(self, reg_a, reg_b):
        # self.mar = self.ram_read(reg_b)
        # self.mdr = self.reg[self.mar]
        # self.mdr = self.reg[reg_b] #new
        # # self.mar = self.ram_read(reg_a)
        # # self.mdr = self.mdr * self.reg[self.mar]
        # self.mdr = self.mdr * self.reg[reg_a] #new
        # self.reg[reg_a] = self.mdr # new
        self.ram[reg_a] *= self.ram[reg_b]

    def alu_and(self, reg_a, reg_b):
        # self.mar = self.ram_read(reg_b)
        # self.mdr = self.reg[self.mar]
        # self.mar = self.ram_read(reg_a)
        # self.mdr = self.mdr & self.reg[self.mar]
        # self.reg[self.mar] = self.mdr

        self.ram[reg_a] = self.ram[reg_a] & self.ram[reg_b]

    def alu_cmp(self, reg_a, reg_b):
        # self.mar = self.ram_read(reg_b)
        # self.mdr = self.reg[self.mar]
        # self.mar = self.ram_read(reg_a)
        # self.mdr = self.mdr & self.reg[self.mar]
        # # `FL` bits: `00000LGE`
        # if self.mdr > self.reg[self.mar]:
        #     self.fl = 0b00000100  # reg b > reg a (L)
        # elif self.mdr == self.reg[self.mar]:
        #     self.fl = 0b00000001  # they are equal (E)
        # else:
        #     self.fl = 0b00000010  # reg a > reb a (G)
        if self.ram[reg_a] < self.ram[reg_b]:
            self.fl = 0b00000100
        if self.ram[reg_a] == self.ram[reg_b]:
            self.fl = 0b00000001
        else:
            self.fl = 0b00000010

    def alu_dec(self, reg):
        # self.mar = self.ram_read(reg)
        # self.mdr = self.reg[self.mar]
        # self.mdr -= 1
        # self.reg[self.mar] = self.mdr
        self.ram[reg] -= 1

    def alu_inc(self, reg):
        # self.mar = self.ram_read(reg)
        # self.mdr = self.reg[self.mar]
        # self.mdr += 1
        # self.reg[self.mar] = self.mdr
        self.ram[reg] += 1

    def alu_div(self, reg_a, reg_b):
        # self.mar = self.ram_read(reg_b)
        # self.mdr = self.reg[self.mar]
        # if self.mdr == 0:
        #     print('Cannot divide by 0.')
        #     sys.exit(1)
        # self.mar = self.ram_read(reg_a)
        # self.mdr = self.reg[self.mar] / self.mdr  # floor division?
        # self.reg[self.mar] = self.mdr
        if self.ram[reg_b] == 0:
            print('Cannot divide by 0.')
            sys.exit(1)
        self.ram[reg_a] = (self.ram[reg_a] / self.ram[reg_b])

    def alu_not(self, reg, unused):
        # self.mar = self.ram_read(reg)
        # self.mdr = self.reg[self.mar]
        # self.mdr = ~self.mdr
        # self.reg[self.mar] = self.mdr
        self.ram[reg] = ~self.ram[reg]

    def alu_or(self, reg_a, reg_b):
        # self.mar = self.ram_read(reg_b)
        # self.mdr = self.reg[self.mar]
        # self.mar = self.ram_read(reg_a)
        # self.mdr = self.mdr | self.reg[self.mar]
        # self.reg[self.mar] = self.mdr
        self.ram[reg_a] = self.ram[reg_a] | self.ram[reg_b]

    def alu_xor(self, reg_a, reg_b):
        # self.mar = self.ram_read(reg_b)
        # self.mdr = self.reg[self.mar]
        # self.mar = self.ram_read(reg_a)
        # self.mdr = self.mdr ^ self.reg[self.mar]
        # self.reg[self.mar] = self.mdr
        self.ram[reg_a] = self.ram[reg_a] ^ self.ram[reg_b]

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
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

            # first two bits are the # of operands
            # ex:
            # 10001010
            #      10001010 (shifted 6)
            # 00000010
            # evaluate number of operands
            # binary 10
            # the above example is 2
            # add one for the instruction
            # 3 operands!
            # (no need to & because no bit higher than 2)

            move_pc_counter = self.ir >> 6
            num_operands = move_pc_counter

            if self.ir in self.instructions:

                if num_operands == 0:
                    self.instructions[self.ir]()

                elif num_operands == 1:
                    self.instructions[self.ir](operand_a)

                else:
                    self.instructions[self.ir](operand_a, operand_b)

            # if self.ir in self.instructions:
            #     self.instructions[self.ir]()

            else:
                print(f'Unknown instruction {self.ir} at address{self.pc}')
                sys.exit(1)
            # check if instruction adds to pc at all
            program_counter_check = self.ir & 0b00010000
            mod_program = program_counter_check >> 4
            # 00010000
            #    0001
            # mod_program = program_counter_check

            if mod_program == 1:
                pass
            else:
                self.pc += num_operands + 1

    def ram_read(self, address):  # memory address
        self.mdr = self.ram[address]
        return self.mdr

    def ram_write(self, data, address):
        # mdr #mar
        self.ram[address] = data

    def handle_ldi(self, register, value):
        # self.mar = self.ram_read(self.pc + 1)
        # self.mdr = self.ram_read(self.pc + 2)
        # self.reg[self.mar] = self.mdr
        self.ram[register] = value
        # self.pc += 3
        # 3 byte instruction
        # assigning value of a register to an integer

    def jmp(self, register):
        self.pc = self.ram[register]

    def handle_prn(self, register):
        # self.mar = self.ram_read(self.pc + 1)
        print(self.ram[register])
        # self.pc += 2
        # 2 byte instruction

    def handle_mul(self, reg_a, reg_b):
        self.alu('MUL', reg_a, reg_b)
        # self.pc += 3

    def handle_add(self, reg_a, reg_b):
        self.alu('ADD', reg_a, reg_b)
        # self.pc += 3

    def handle_and(self, reg_a, reg_b):
        self.alu('AND', reg_a, reg_b)
        # self.pc += 3

    def handle_cmp(self, reg_a, reg_b):
        self.alu('CMP', reg_a, reg_b)
        # self.pc += 3

    def handle_dec(self, reg_a):
        self.alu('DEC', reg_a, None)
        # self.pc += 2

    def handle_inc(self, reg_a):
        self.alu('INC', reg_a, None)
        # self.pc += 2

    def handle_div(self, reg_a, reg_b):
        self.alu('DIV', reg_a, reg_b)
        # self.pc += 3

    def handle_not(self, reg_a):
        self.alu('NOT', reg_a, None)
        # self.pc += 2

    def handle_or(self, reg_a, reg_b):
        self.alu('OR', reg_a, reg_b)
        # self.pc += 3

    def handle_xor(self, reg_a, reg_b):
        self.alu('XOR', reg_a, reg_b)
        # self.pc += 3

    def pop(self, register):
        # self.mar = self.ram_read(self.pc + 1)
        # self.reg[self.mar] = self.ram[self.sp]
        self.ram[register] = self.ram[self.sp]
        self.sp += 1

    def push(self, register):
        self.sp -= 1
        # self.mar = self.ram_read(self.pc + 1)
        # self.ram[self.sp] = self.reg[self.mar]
        self.ram[self.sp] = self.ram[register]

    def jeq(self, register):
        equal = self.fl & 0b00000001
        if equal == 1:
            self.pc = self.ram[register]
        else:
            self.pc += 2

    def jne(self, register):
        equal = self.fl & 0b00000001
        if equal == 0:
            self.pc = self.ram[register]
        else:
            self.pc += 2

    def call(self, register):
        return_addr = self.pc + 2
        self.sp -= 1

        self.ram[self.sp] = return_addr

        reg_num = self.ram[register]
        subroutine_addr = reg_num

        self.pc = subroutine_addr

    def ret(self):

        self.pc = self.ram[self.sp]
        self.sp += 1

    def handle_hlt(self):
        self.running = False
    # self.pc += 1


cpu = CPU()

cpu.load()
cpu.run()
