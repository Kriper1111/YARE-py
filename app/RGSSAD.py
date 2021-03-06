# base class for RGSSAD

import os


def shorten(number):
    return number & 0xFFFFFFFF

class EncryptedData:
    def __init__(self, name, byteOffset, length, key):
        self.name = name
        self.offset = byteOffset
        self.size = length
        self.key = key


class Base:
    def __init__(self, fileName, size):
        self.Archive = open(fileName, "rb")
        self.Size = size
        self.key = 0xDEADCAFE
        self.ArchivedData = []

    def DecryptNumber(self, number):
        number = int.from_bytes(number, "little")
        number = shorten(number)
        decrypted = number ^ self.key
        self.key = (self.key*7)+3
        self.key = shorten(self.key)
        decrypted = shorten(decrypted)
        return decrypted
    
    def DecryptName(self, encryptedName):
        decryptedName = []
        for i in range(0, len(encryptedName)):
            decryptedName.append(encryptedName[i] ^ (self.key & 0xFF))
            self.key = (self.key*7) + 3
            self.key = shorten(self.key)
        decryptedName = bytearray(decryptedName).decode('utf-8')
        return decryptedName

    def DecryptFiles(self, path):
        for Index, File in enumerate(self.ArchivedData, start=1):
            decrypted = []
            self.Archive.seek(File.offset, 0)
            encrypted = self.Archive.read(File.size)
            print("Decoding file {}; #{} of {}".format(File.name, Index, len(self.ArchivedData)))
            i = 0
            Tkey = File.key
            keyBits = Tkey.to_bytes(4, "little")
            for byte in encrypted:
                decrypted.append(byte ^ keyBits[i])
                if i == 3:
                    Tkey = shorten(Tkey * 7 + 3)
                    keyBits = Tkey.to_bytes(4, "little")
                i = (i + 1) % 4
            OSpath = path
            if os.name == "posix":
                File.name = File.name.replace("\\", "/")
            filename = os.path.join(path, File.name)
            folder = os.path.split(File.name)[0]
            OSpath = os.path.join(path, folder)

            print("Decrypted all the bytes, storing them into {}".format(OSpath))
            os.makedirs(OSpath, exist_ok=True)
            output = open(filename, "wb")
            output.write(bytearray(decrypted))
            output.close()
        self.Archive.close()
