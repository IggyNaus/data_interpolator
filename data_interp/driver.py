import argparse
import numpy as np

# from dataset import text_input_filepath


def main():
    ## User input
    parser = argparse.ArgumentParser(description="Analyse file name, resolution input, ")
    parser.add_argument("--file-type", type=str, required=True)#, options=["web", "local"])

    # parser.add_argument("--INfilepath",  type=str, required=True, help="relative location of input file")
    # parser.add_argument("--OUTfilepath",    type=str,   required=True, help="desired relative location of output file")
    # parser.add_argument("--n-days",  type=int,   default=90,   help="number of days to analyze")
    # parser.add_argument("--outfile", type=str,   default="output.png", help="output figure path")
    
    args = parser.parse_args()
    match args.file_type:
        case "web":
            web_parser = argparse.ArgumentParser(description="Please input URL:")
            web_parser.add_argument("--url", type=str, required=True)
            web_args=web_parser.parse_args()
            print(f"Web")
        case "local":
            local_parser = argparse.ArgumentParser(description="Please input relative file path:")
            local_parser.add_argument("--file-path", type=str, required=True)
            local_args=local_parser.parse_args()
            print(f"Local")

    

if __name__ == "__main__":
    main()
