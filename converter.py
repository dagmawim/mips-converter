#!/usr/bin/env python

# Author : Dagmawi Mulugeta
# Date : 03/11/2017
# purpose: Python script to convert mips instructions to binary and hex


from numpy import *


def jType(instruction):
    result = []
    opcode = insCodes[instruction[0]][0]  # OPCODE
    result.append(bin(opcode)[2:].zfill(6))  # OPCODE

    loc = int(instruction[1]) / 4
    imm = bin(loc)[2:].zfill(26)   # imm
    result.append(imm)             # imm

    bin_val = ''.join(result)
    hex_val = hex(int('0b' + bin_val, 2))[2:].zfill(8)
    return (hex_val, bin_val)


def rType(instruction):
    result = []
    shift = 0

    opcode = insCodes[instruction[0]][0]  # OPCODE
    result.append(bin(opcode)[2:].zfill(6))  # OPCODE

    if instruction[0] == 'sll' or instruction[0] == 'srl':
        shift = int(instruction[3])
        result.append(bin(opcode)[2:].zfill(5))  # rs

        rt = getRegister(instruction[2])
        result.append(bin(rt)[2:].zfill(5))  # rt
    else:
        rs = getRegister(instruction[2])  # rs
        result.append(bin(rs)[2:].zfill(5))  # rs

        rt = getRegister(instruction[3])
        result.append(bin(rt)[2:].zfill(5))  # rt

    rd = getRegister(instruction[1])
    result.append(bin(rd)[2:].zfill(5))  # rd

    result.append(bin(shift)[2:].zfill(5))  # shift

    func = insCodes[instruction[0]][1]     # Func Code
    result.append(bin(func)[2:].zfill(6))  # Func Code

    bin_val = ''.join(result)
    hex_val = hex(int('0b' + bin_val, 2))[2:].zfill(8)
    return (hex_val, bin_val)


def iType(instruction):
    result = []
    opcode = insCodes[instruction[0]][0]  # OPCODE
    result.append(bin(opcode)[2:].zfill(6))  # OPCODE

    if instruction[0] == 'sw' or instruction[0] == 'lw':
        baseAndImm = instruction[2].split('(')

        rs = getRegister(baseAndImm[1][:-1])
        result.append(bin(rs)[2:].zfill(5))  # rs

        rt = getRegister(instruction[1])
        result.append(bin(rt)[2:].zfill(5))  # rt

        imm = bin(int(baseAndImm[0]))[2:]       # imm
        result.append(imm.zfill(16))             # imm

    else:
        rs = getRegister(instruction[2])
        result.append(bin(rs)[2:].zfill(5))  # rs

        rt = getRegister(instruction[1])         # rt
        result.append(bin(rt)[2:].zfill(5))      # rt

        if instruction[0] == 'beq':
            new_pc = (int(instruction[3]) - 4) / 4
            ba = bin(new_pc)[2:]                     # br_addr
            result.append(ba.zfill(16))              # br_addr

        elif instruction[0] == 'andi' or instruction[0] == 'addi':
            sig = 0
            ind = bin(int(instruction[3])).find('0b')
            if ind != 0:
                sig = 1
            imm = bin(int(instruction[3]))[ind + 2:]       # imm
            result.append(str(sig) + imm.zfill(15))             # imm

    bin_val = ''.join(result)
    hex_val = hex(int('0b' + bin_val, 2))[2:].zfill(8)
    return (hex_val, bin_val)


registers = {
    'zero': 0,   'at': 1,   'v0': 2,   'v1': 3,
    'a0': 4,   'a1': 5,   'a2': 6,   'a3': 7,
    't0': 8,   't1': 9,   't2': 10,  't3': 11,
    't4': 12,  't5': 13,  't6': 14,  't7': 15,
    's0': 16,  's1': 17,  's2': 18,  's3': 19,
    's4': 20,  's5': 21,  's6': 22,  's7': 23,
    't8': 24,  't9': 25,  'k0': 26,  'k1': 27,
    'gp': 28,  'sp': 29,  'fp': 30,  'ra': 31
}


# FINISH THE INSTRUCTION CODES, WILL HAVE ISSUES
insCodes = {
    'add': (0, 0x20), 'sll': (0, 0x00), 'and': (0, 0x24), 'nor': (0, 0x27),
    'or': (0, 0x25),  'slt': (0, 0x2a),  'srl': (0, 0x02), 'sub': (0, 0x22),

    'addi': (0x8, 0), 'lw': (0X23, 0), 'beq': (0x4, 0), 'sw': (0x2b, 0),
    'subi': (0, 0), 'andi': (0xc, 0),

    'j': (0x2, 0)
}


instructionHandler = {
    'add': rType, 'sll': rType, 'and': rType, 'nor': rType,
    'or': rType, 'slt': rType, 'sll': rType, 'srl': rType,
    'sub': rType,

    'addi': iType, 'lw': iType, 'beq': iType, 'sw': iType,
    'subi': iType, 'andi': iType,

    'j': jType
}


def getRegister(value):
    return registers[value[1:]]


def getSeparatedInstruction(line):
    line_split = line.split(" ")
    split_second = line_split.pop(1).split(",")
    line_split.extend(split_second)
    return line_split


def convertToHex(line):
    separated = getSeparatedInstruction(line)
    if separated[0] == 'subi':
        old = separated[:]
        separated[0] = 'addi'
        separated[3] = str(-1 * int(separated[3]))
        print 'taking ', old, 'as ---->', separated
    converted = instructionHandler[separated[0]](separated)
    return converted


def main():
    inp_file = open('input.txt', 'r')
    out_file = open('output.txt', 'w')
    line = inp_file.readline()
    print 'Converting file ...'
    while line:
        bin_hex = convertToHex(line[:-2])
        # print line[:-2], ' -> ', bin_hex
        out_file.write(line[:-2] + '------>' + str(bin_hex) + '\n')
        line = inp_file.readline()
    print 'Done ...'
    print 'Output in output.txt'
    inp_file.close()
    out_file.close()


if __name__ == "__main__":
    main()
