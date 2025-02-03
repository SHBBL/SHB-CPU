import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file',type=str,metavar='',required=True,help='Input file (*.shb)')
parser.add_argument('-o','--output',type=str,metavar='',required=True,help='Output file (*.hshb)')
args = parser.parse_args()

with open(args.file,"r") as f:
    lines = f.readlines()
    for ins in lines:
        inst = ins.strip()
        decimal_num = int(inst, 2)
        hex_num = hex(decimal_num)[2:]
        with open(args.output,"a+") as f:
            f.write(hex_num + "\n")