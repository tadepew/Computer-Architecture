import sys

PRINT_NAME = 1
HALT = 2
SAVE_REGISTER = 3  # SAVE_REGISTER R1, 37   register[1] = 37
PRINT_REGISTER = 4
ADD = 5

memory = [
    PRINT_NAME,
    SAVE_REGISTER,
    1,  # register #
    37,  # value assigned to the register
    PRINT_REGISTER,
    1,  # print value from this register
    SAVE_REGISTER,
    2,
    3,
    ADD,
    2,
    2,
    HALT
]

register = [0] * 8  # 8 registers, like a variable

program_counter = 0
running = True

while running:
    instruction_register = memory[program_counter]
    if instruction_register == PRINT_NAME:
        print('Vincent')
        program_counter += 1
    elif instruction_register == SAVE_REGISTER:
        register_number = memory[program_counter + 1]
        value = memory[program_counter + 2]
        register[register_number] = value
        program_counter += 3
    elif instruction_register == PRINT_REGISTER:
        register_index = memory[program_counter + 1]
        value = register[register_index]
        print(value)
        program_counter += 2
    elif instruction_register == ADD:
        register_index_one = memory[program_counter + 1]
        register_index_two = memory[program_counter + 2]
        value_one = register[register_index_one]
        value_two = register[register_index_two]
        print(value_one + value_two)
        program_counter += 3
    elif instruction_register == HALT:
        running = False
        program_counter += 1
    else:
        print(
            f'Unknown instruction {instruction_register} at address {program_counter}')
        sys.exit(1)
