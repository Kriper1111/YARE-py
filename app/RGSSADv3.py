# RGSSADv3

from app import RGSSAD
import time

class RGSSADv3(RGSSAD.Base):
    def read(self, verbose):
        print("Reading v3 file with size of " + hex(self.Size))
        self.Archive.seek(8, 0)

        self.key = int.from_bytes(self.Archive.read(4), "little")
        self.key = self.key * 9 + 3

        #for i in range(0, 1):
        while True:
            if verbose == "Y":
                print(">> Reading new file metadata.. <<")

            offset = self.DecryptNumber(self.Archive.read(4))
            size = self.DecryptNumber(self.Archive.read(4))
            key = self.DecryptNumber(self.Archive.read(4))

            if offset == 0:
                break

            length = self.DecryptNumber(self.Archive.read(4))
            filename = self.DecryptName(self.Archive.read(length))

            File = RGSSAD.EncryptedData(filename, offset, size, key)
            self.ArchivedData.append(File)
            #self.Archive.seek(size, 1)
            if verbose == "Y":
                print("file name " + filename)
                print("file size " + hex(size))
                print("offset " + hex(offset))
                print("key " + hex(self.key))
                print("we're at " + hex(self.Archive.tell()))
            #time.sleep(2)
        # print("holy shit, we made it.")

    def DecryptNumber(self, number):
        number = int.from_bytes(number, "little")
        decrypted = number ^ self.key
        return decrypted

    def DecryptName(self, encryptedName):
        decryptedName = []
        tKey = self.key.to_bytes(4, "little")
        Pos = 0
        for byte in encryptedName:
            Pos %= 4
            #if verbose
            #print("Decrypting byte {} with key bit {}".format(hex(byte), hex(tKey[Pos])))
            decryptedName.append(byte ^ tKey[Pos])
            Pos += 1
        decryptedName = bytearray(decryptedName).decode("UTF-8")
        return decryptedName
