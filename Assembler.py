import argparse
import time

inp = True
out = True
err = False

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',type=str,metavar='',required=True,help='Input file (*.asm)')
parser.add_argument('-o','--output',type=str,metavar='',required=True,help='Output file (*.shb)')
args = parser.parse_args()

def help():
	print(r"""
		r/w   jmp    alu   reg   in2    mov     data
		/-\  /---\  /---\  /--\  /--\  /---\ /--------\
		 0    000    000    00    00    000   00000000
		""")

def checker(inp:bool,out:bool):
	infile = args.file.split('.')
	outfile = args.output.split('.')
	if infile[1] != 'asm':
		print(f'{infile[0]} must end with .asm')
		inp = False
	elif outfile[1] != 'shb':
		print(f'{outfile[0]} must end with .shb')
		out = False

def main(input:str,out:str):
	instruction = ''
	jmp = {'jmp':'111','je':'100','jg':'010','jl':'001','jge':'110','jle':'101'}
	alu = {"add":'001',"sub":'010',"mul":'011',"div":'100',"xor":'101',"and":'110',"or":'111'}
	reg = {'R1':'01','R2':'10','M1':'11'}
	lines = []
	check = []
	jmptable = {}
	variables = {}
	ind = 1
	lnct = 0
	try:
		with open(input,'r') as f:
			ilines = f.readlines()
			check = ilines
			for line in ilines:
				if line[0] == ';' or line in ['',None,'\n','\t']:
					continue
				elif ';' in line:
					line = line.split(';')
					line.remove(line[1])
				else:
					line = [line]
				if ' ' in line[0]:
					line[0] = line[0].strip()
				line = line[0].split(" ")
				if line[0] in alu or line[0] == 'mov':
					line[1] = line[1].split(",")
					line.append(line[1][0])
					line.append(line[1][1])
					line.remove(line[1])
				if ':' in line[0]:
					line = line[0].split(':')
					line.remove(line[1])
					if ind != 0:
						jmptable[line[0]] = ind - 1
					else:
						jmptable[line[0]] = ind
				elif line[1] == '=':
					line.remove('=')
					variables[line[0]] = line[1]
					continue
				lines.append(line)
				ind += 1
			for label in jmptable:
				lines.remove([label])
			for i in range(len(check)):
				check[i] = check[i].strip()
			for i in range(len(lines)):
				if lines[i][1] == '=':
					variables[lines[i][0]] = lines[i][2]
#*****************************************************************************************************
		print(jmptable)
		for j in range(len(lines)):
			if lines[j][0] in jmp:
				if lines[j][1] in jmptable:
					instruction = "0" + jmp[lines[j][0]] + "0000000000" +  format(jmptable[lines[j][1]],'08b')
				elif lines[j][1] in variables:
					instruction = "0" + jmp[lines[j][0]] + "0000000000" +  format(int(variables[lines[j][1]]),'08b')
				else:
					instruction = "0" + jmp[lines[j][0]] + "0000000000" +  format(int(lines[j][1]),'08b')

			elif lines[j][0] == 'mov':
				if lines[j][1] in reg and lines[j][1] not in variables:
					if lines[j][2] in reg:
						instruction = '0' + '000' + '000' + reg[lines[j][1]] + '00' + '0' + reg[lines[j][2]] + '00000000'
					elif lines[j][2] in variables:
						instruction = '0' + '000' + '000' + reg[lines[j][1]] + '00' + '100' + format(int(variables[lines[j][2]]),'08b')
					else:
						instruction = '0' + '000' + '000' + reg[lines[j][1]] + '00' + '100' + format(int(lines[j][2]),'08b')
				else:
					lnind = check.index(' '.join([lines[j][m] for m in [0]]) + ' ' + ','.join([lines[j][m] for m in [1,2]])) + 1
					raise Exception(f'Invalid register at line {lnind} -> {check[lnind - 1].strip()} <-')
					break

			elif lines[j][0] in alu:
				if lines[j][1] in reg and lines[j][1] != 'M1':
					if lines[j][2] in reg and lines[j][2] != 'M1':
						instruction = '0' + '000' + alu[lines[j][0]] + reg[lines[j][1]] + reg[lines[j][2]] + '000' + '00000000'
					elif lines[j][2] in variables and lines[j][1] != 'M1':
						instruction = '0' + '000' + alu[lines[j][0]] + reg[lines[j][1]] + '00' + '000' + format(int(variables[lines[j][2]]),'08b')
					elif lines[j][1] != 'M1':
						instruction = '0' + '000' + alu[lines[j][0]] + reg[lines[j][1]] + '00' + '000' + format(int(lines[j][2]),'08b')
					elif lines[j][1] == 'M1':
						raise Exception('M1 cannot be used in arithmetic operations')
						break
					else:
						lnind = check.index(' '.join([lines[j][m] for m in [0]]) + ' ' + ','.join([lines[j][m] for m in [1,2]])) + 1
						raise Exception(f'Invalid register at line {lnind} -> {check[lnind - 1].strip()} <-')
						break


			elif lines[j][0] == 'stmem':
				if lines[j][1] in variables:
					instruction = '1' + '000' + '000' + '00'+ '00' + '000' + format(int(variables[lines[j][1]]),'08b')
				else:
					instruction = '1' + '000' + '000' + '00'+ '00' + '000' + format(int(lines[j][1]),'08b')


			elif lines[j][0] == 'ldmem':
				if lines[j][1] in reg:
					instruction = '0' + '000' + '000' + reg[lines[j][1]] + '00' + '101' + '00000000'
				else:
					lnind = check.index(' '.join(lines[j])) + 1
					raise Exception(f"cannot load to constant number at line {lnind} -> {check[lnind - 1].strip()} <-")
					break

			elif lines[j][0] in variables:
				pass

			else:
				lnind = check.index(' '.join(lines[j])) + 1
				raise Exception(f"Invalid instruction at line {lnind} -> {check[lnind - 1].strip()} <-")
				break

			lines[j] = instruction

		err = False

	except Exception as error:
		print(error)
		err = True
	try:
		if not err:
			with open(out,'w') as g:
				for i in range(len(lines)):
					g.writelines(lines[i] + '\n')

	except:
		print(f'cannot write {out}')

if __name__ == '__main__':
	checker(inp,out)
	if inp and out:
		help()
		main(args.file,args.output)