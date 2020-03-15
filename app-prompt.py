# YARE wrapper without command line arguments

from os import listdir, path
from pathlib import PurePath
import sys
import app


def main():
    cwd = path.realpath(path.dirname(__file__))

    print("Searching for RGSSAD files in " + cwd)

    FileList = []
    Ind = 0

    for File in listdir(cwd):
        if File.endswith(('.rgssad', '.rgss2a', '.rgss3a')):
            Ind += 1
            print("#{} : {}".format(Ind, File))
            FileList.append(PurePath(cwd, File))

    if not FileList:
        raise IOError("No RGSSAD files found")

    ChosenOne = input("Please choose the file from the list above or ESC to exit\r\n")
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

    verbose = input("Should I go verbose? (Y/n)\r\n")

    outPath = "Extracted"
    question = input("One more thing: do you want specify extraction destination? (Y/n)\r\n")
    if question == "Y":
        outPath = input("Type the folder name: ")
    else:
        input("Okay, I will put the data into 'Extracted' subfolder. Press Enter to continue or Ctrl+C to exit.")

    outPath = PurePath(cwd, outPath)  # Ultimate solution

    print("So it's settled then. Processing {}, with output to {}".format(ChosenOne, outPath))
    del FileList

    RGSSAD.read(verbose)
    RGSSAD.DecryptFiles(outPath)
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
        sys.exit()
