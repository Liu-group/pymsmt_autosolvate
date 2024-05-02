import sys
from .MCPB_orca_packed import run_mcpb_orca
def main(args=None):
    if args is None:
        args = sys.argv[1:]
        print(args)
    if len(args) == 2:
        print('start to use MCPB_orca to generate FF parameters')
        MCPBin = args[0]
        step = args[1]
        run_mcpb_orca(inputfile=MCPBin,step=step)
    elif len(args) != 2:
        print('Error: only one args needed, please provide the name of MCPB.in inputs file, and step')
        sys.exit()

if __name__ == '__main__':
    main()
