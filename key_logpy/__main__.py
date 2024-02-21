import argparse
from keylogger import KeyLogger


# Run the program
def main() -> None:
    args = get_args()
    output = args.output
    with KeyLogger(output):
        while input('Press "q" to quit: ') != "q":
            pass

        
# Create a parser object that will hold all the information necessary to parse the command line
def get_args() -> argparse.ArgumentParser:
    '''
    Creates a argparse.ArgumentParser object that will hold the output file path if provided, 
    if not, the default file path will be used (keystrokes.log)
    '''
    
    parser = argparse.ArgumentParser(description="Keystroke logging")
    parser.add_argument("--output", "-o", type=str, metavar="output",
                        help="Log file [default: 'keystrokes.log'] - The path to the file where the keystrokes will be logged", default="keystrokes.log")
    
    parser.parse_args()
    return parser.parse_args()


if __name__ == "__main__":
    main()