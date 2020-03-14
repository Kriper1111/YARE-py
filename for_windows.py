# Wrapper for windows

import os
import argparse
import app


def main():
    cwd = os.path.realpath(os.path.dirname(__file__))

    parser = argparse.ArgumentParser(description="RGSSAD file extraxtor")
    parser.add_argument('filename', metavar='filename', type=str, nargs='+', help='Source file')
    parser.add_argument('output', metavar='output', type=str, nargs='?', help='Output directory', default='.\\Extracted')
    args = parser.parse_args()

    inputFile = os.path.join(cwd, args.filename[0])
    outputDir = os.path.join(cwd, args.output)

    print(inputFile)

    RGSSAD = create(inputFile)

    """
    print("Searching for RGSSAD files in " + cwd)

    FileList = []
    Ind = 0

    for File in os.listdir(cwd):
        if File.endswith(('.rgssad', '.rgss2a', '.rgss3a')):
            Ind += 1
            print("#{} : {}".format(Ind, File))
            FileList.append(os.path.join(cwd, File))

    if not FileList:
        raise IOError("No RGSSAD files found")

    ChosenOne = input("Please choose the file from the list above or ESC to exit")
    if not ChosenOne:
        raise ValueError("I asked you nicely to choose the file")
    if ChosenOne == "ESC":
        print("Got it, shutting down")
        sys.exit()
    try:
        ChosenOne = int(ChosenOne) - 1
    except ValueError:
        raise ValueError("Whatever you typed is not a number")
    if ChosenOne > len(FileList):
        raise ValueError("This number is too large")
    if ChosenOne < 0:
        raise ValueError("This number is too small")
    ChosenOne = FileList[ChosenOne]
    RGSSAD = create(ChosenOne)
    print("Chosen One, you overcame may trials, now you may become analyzed")

    path = "Extracted"
    question = input(
        "One more thing: can I get the folder for extracting? Default is 'Extracted' in this folder. (Y/n)")
    if question == "Y":
        path = input("Type the folder name: ").replace("./", "")
    path = os.path.join(cwd, path)

    
    del FileList
    """
    print("So it's settled then. Processing {}, with output to {}".format(inputFile, outputDir))
    RGSSAD.read()
    RGSSAD.DecryptFiles(outputDir)
    print("Job's done.")


def create(filePath):
    tmp = open(filePath, "rb")
    data = tmp.read(8)
    print(data[7])
    size = tmp.seek(0, 2)
    tmp.close()
    if data[0:6].decode('ASCII') == "RGSSAD":
        if data[7] == 1:
            print(app.RGSSADv1.RGSSADv1.__dict__)
            return app.RGSSADv1.RGSSADv1(filePath, size)
        if data[7] == 3:
            return app.RGSSADv3.RGSSADv3(filePath, size)
    raise IOError("Headers look wrong, are you sure that's valid RGSSAD?")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e))
