import argparse


## User input
parser = argparse.ArgumentParser(description="Analyse file name, resolution input, ")
parser.add_argument("--file-name",  type=str, default="file.txt", help="relative location of input file")
# parser.add_argument("--n-days",  type=int,   default=90,   help="number of days to analyze")
# parser.add_argument("--outfile", type=str,   default="output.png", help="output figure path")
args = parser.parse_args()

### Verify correct inputs: 
print(f"Selected File: {args.file_name}")
# print(f"Days:      {args.n_days}")   # note: hyphens become underscores
# print(f"Output:    {args.outfile}")



