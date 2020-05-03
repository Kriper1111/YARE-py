# YARE wrapper with command-line arguments

from os import path, makedirs
from pathlib import PurePath
import argparse
import app
import sys


def main():
    cwd = path.realpath(path.dirname(__file__))

    parser = argparse.ArgumentParser(description="RGSSAD file extractor")
    parser.add_argument('input', metavar='filename', type=str, nargs='+', help='Source file')
    parser.add_argument('--output', '-o', metavar='output', type=str, nargs='?',
                        help='Output directory, default: "Extracted" subfolder', default='Extracted')
    parser.add_argument('--verbose', '-v', metavar='-v', action="store_const", const="Y", help="Verbose")
    args = parser.parse_args()

    filename = args.input[0]
    output = args.output

    inputFile = PurePath(cwd, filename)
    outputDir = PurePath(cwd, output)
    
    if not path.exists(inputFile):
        raise IOError("Can't find the specified file")
    
    try:
        makedirs(outputDir, exist_ok = True)
    except OSError:
        if input("Can't create output dir, use default? (Y/n): ").lower() == "y":
            outputDir = PurePath(cwd, "Extracted")
        else:
            sys.exit()
    
    verbose = args.verbose

    RGSSAD = create(inputFile)

    print("So it's settled then. Processing {}, with output to {}".format(inputFile, outputDir))
    RGSSAD.read(verbose)
    RGSSAD.DecryptFiles(outputDir)
    print("\r\nJob's done.")


def create(filePath):
    tmp = open(filePath, "rb")
    data = tmp.read(8)
    size = tmp.seek(0, 2)
    tmp.close()
    if data[0:6].decode('ASCII') == "RGSSAD":
        if data[7] == 1:
            return app.RGSSADv1.RGSSADv1(filePath, size)
        if data[7] == 3:
            return app.RGSSADv3.RGSSADv3(filePath, size)
    raise IOError("Headers look wrong, are you sure that's valid RGSSAD?")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e))
