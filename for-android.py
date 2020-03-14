# YARE wrapper for Android

import os,sys

# we list every *.rgssad, *.rgss2a and *.rgss3a
# user picks the file using input()
# we analyze the file
# and send it through respective class
# and work from there

def main():
    cwd = os.path.dirname(__file__)
    
    print("Searching for RGSSAD files in "+cwd)
    
    FileList = []
    
    for File in os.listdir(cwd):
        if File.endswith(('.rgssad','.rgss2a','.rgss3a')):
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
        ChosenOne = int(ChosenOne)-1
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
    question = input("One more thing: can I get the folder for extracting? Default is 'Extracted' in this folder. (Y/n)")
    if question=="Y":
        path = input("Type the folder name: ").replace("./","")
    path = os.path.join(cwd, path)
    
    print("So it's settled then. Processing {}, with output to {}".format(ChosenOne, path)
    del FileList # don't need that, i hope
    
    RGSSAD.read()
    RGSSAD.decrypt(path)
    print("Job's done.")

def check(filePath):
    tmp = open(filePath, "rb")
    data = tmp.read(8)
    tmp.close()
    if data[0:5].decode('ASCII')=="RGSSAD":
        if data[7]==1:
            return app.RGSSADv1(filePath)
        if data[7]==3:
            return app.RGSSADv3(filePath)
    raise IOError("Headers look wrong, are you sure that's valid RGSSAD?")

if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(str(e))
