import argparse
import numpy as np

from dataset import text_input_filepath


def main():
    ## User input
    parser = argparse.ArgumentParser(description="Analyse file name, resolution input, ")
    parser.add_argument("--INfilepath",  type=str, required=True, help="relative location of input file")
    parser.add_argument("--OUTfilepath",    type=str,   required=True, help="desired relative location of output file")
    # parser.add_argument("--n-days",  type=int,   default=90,   help="number of days to analyze")
    # parser.add_argument("--outfile", type=str,   default="output.png", help="output figure path")
    args = parser.parse_args()
    text_input_filepath(args.INfilepath,args.OUTfilepath)

if __name__ == "main":
    main()
