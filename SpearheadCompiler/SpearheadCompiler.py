# Spearhead Compiler
# Source language = Flint
# Target language = binary for Neander
# Current compiling steps:
# Direct Mnemonic -> pure binary.

## MNEMONICS DICTIONARY
class Variable:           # Stores variable metadata, used for replacing the calls with the correct addresses.
  def __init__(self, name, value, byte):
    self.name = name
    self.value = value
    self.byte = byte

class Marker:           # Stores marker metadata
  def __init__(self, tag, location):
    self.tag = tag
    self.location = location



program =[]
uncommented=[]
var_list =[]
marker_list=[]
var_unpacked = []
MnemonicDict = {
"NOP": 0,
"STA": 16,
"LDA": 32,
"ADD": 48,
"OR": 64,
"AND": 80,
"NOT": 96,
"JMP": 128,
"JN": 144,
"JZ": 160,
"HLT": 240
}

with open('source.txt') as source:
    raw = source.readlines()

for line_n in range(len(raw)):
    line = raw[line_n]
    line = line.replace('\n', '') # remove newlines
    if line[:2] == '//':
        print('a')
    else:
        uncommented.append(line)
        print(line)




for line_n in range(len(uncommented)):
    line = uncommented[line_n]
    print(line)
    if '#' in line: # Case line contains Marker, store marker metadata and run rest of line testes
        line_unpacked = line.split(' ')
        for marker in line_unpacked[1:]:
            marker_list.append(Marker( marker[1:], line_n))
        line = line_unpacked[0]


    if str(line).isnumeric():     # Case line is a number, treat as an address/operand
        #print('isnumber')
        program.append(str(line))

    elif str(line) in MnemonicDict:  # Case line is keyword, replace it for the correct opcode value
        #print('true')
        line = MnemonicDict[line]
        program.append(line)

    elif str(line)[:3] == "VAR":  # Case line is var definition, store the metadata and write the initial value
        #print(line)
        var_unpacked = str(line).split(" ")
        var_list.append(Variable(var_unpacked[1], var_unpacked[2], line_n))
        #print(var_list[0].name)
        #print(var_list[0].value)
        #print(var_list[0].byte)
        program.append(var_unpacked[2])

    else:
        program.append(line)
    print(line)



for line_n in range(len(program)):   
    line = program[line_n]
    for variable in var_list:        # Replace the variable calls with the values from the var list
        if variable.name == str(line):
            line = variable.byte

    for marker in marker_list:   # Replace the marker calls with the marker locations
        if marker.tag == str(line)[1:]:
            line = marker.location
    program[line_n] = int(line)




#print(program)
#for line in program:
    #print(line)




while len(program) < 256:   # Preemptively completes the empty values of the program file with zeroes. Necessary for NEANDER to recognize the file as readable.
    program.append(0)

neander_file = [3, 78, 68, 82]    # 4 byte code that is found in all NEANDER mem files. Necessary for file recognition.
for line in program:
    neander_file.append(line)
    neander_file.append(0)          # Even though NEANDER instructions are 1 byte long, the file format uses 2 byte instructions and adresses. Second bytes always 0


binary = bytearray(neander_file)   # Converts int list to binary byte array

with open('program.MEM', 'wb') as output:
    output.write(binary)

