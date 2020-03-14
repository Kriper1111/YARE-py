# RGSSADv3

from app import RGSSAD

class RGSSADv3(RGSSAD.Base):
    def read(self):
        print("Reading v3 file with size of " + hex(self.Size))
        self.Archive.seek(8, 0)

        self.key = int.from_bytes(self.Archive.read(4), "little")
        self.key = self.key * 9 + 3

        while True:
            print(">> It's a new cycle<<")
            offset = self.DecryptNumber(self.Archive.read(4))
            size = self.DecryptNumber(self.Archive.read(4))
            filename = self.DecryptName(self.Archive.read(4))
            key = self.DecryptNumber(self.Archive.read(4))

            File = RGSSAD.EncryptedData(filename, offset, size, key)
            self.ArchivedData.append(File)
            self.Archive.seek(size, 1)
            print("file name " + filename)
            print("file size " + str(size))
            print("offset " + hex(offset))
            print("key " + hex(key))
            print("we're at" + hex(self.Archive.tell()))
            if self.Archive.tell() == self.Size:
                break
        print("holy shit, we made it.")

    def DecryptNumber(self, number):
        number = int.from_bytes(number, "little")
        decrypted = number ^ self.key
        return decrypted

    def DecryptName(self, encryptedName):
        decryptedName = []
        tKey = bytes(self.key)
        Pos = 0
        for byte in encryptedName:
            Pos %= 4
            decryptedName.append(byte ^ tKey[Pos])
            Pos += 1
        decryptedName = bytearray(decryptedName).decode("UTF-8")
        return decryptedName
