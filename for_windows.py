# YARE wrapper for Windows

import os
import argparse
import app


def main():
    cwd = os.path.realpath(os.path.dirname(__file__))

    parser = argparse.ArgumentParser(description="RGSSAD file extraxtor")
    parser.add_argument('filename', metavar='filename', type=str, nargs='+', help='Source file')
    parser.add_argument('output', metavar='output', type=str, nargs='?', help='Output directory', default='.\\Extracted\\')
    args = parser.parse_args()

    filename = args.filename[0].replace(".\\", "")
    output = args.output.replace(".\\", "")

    inputFile = os.path.join(cwd, filename)
    outputDir = os.path.join(cwd, output)

    print(inputFile)

    RGSSAD = create(inputFile)

    print("So it's settled then. Processing {}, with output to {}".format(inputFile, outputDir))
    RGSSAD.read()
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
