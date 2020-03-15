# YARE wrapper for Windows

from os import path
from pathlib import PurePath
import argparse
import app


def main():
    cwd = path.realpath(path.dirname(__file__))

    parser = argparse.ArgumentParser(description="RGSSAD file extraxtor")
    parser.add_argument('filename', metavar='filename', type=str, nargs='+', help='Source file')
    parser.add_argument('output', metavar='output', type=str, nargs='?',
                        help='Output directory, default: "Extracted" subfolder', default='Extracted')
    parser.add_argument('--verbose', '-v', metavar='-v', action="store_const", const="Y", help="Verbose", default="n")
    args = parser.parse_args()

    filename = args.filename[0]
    output = args.output

    inputFile = PurePath(cwd, filename)
    outputDir = PurePath(cwd, output)
    verbose = args.verbose
    print(verbose)

    print(inputFile)

    RGSSAD = create(inputFile)

    print("So it's settled then. Processing {}, with output to {}".format(inputFile, outputDir))
    RGSSAD.read(verbose)
    RGSSAD.DecryptFiles(outputDir)
    print("Job's done.")


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
