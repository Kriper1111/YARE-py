import os, sys

from app import RGSSAD

class RGSSADv1(RGSSAD.Base):
    def read(self):
        print("Reading v1 or v2 file with size of "+hex(self.Size))
        self.Archive.seek(8, 0)
    
        while True:
            print(">> Reading new file metadata.. <<")
            length = self.DecryptNumber(self.Archive.read(4))
            filename = self.DecryptName(self.Archive.read(length))
            size = self.DecryptNumber(self.Archive.read(4))
            offset = self.Archive.tell()
            File = RGSSAD.EncryptedData(filename, offset, size, self.key)
            self.ArchivedData.append(File)
            self.Archive.seek(size, 1)
            """
            print("file name "+filename)
            print("file size "+str(size))
            print("offset "+hex(offset))
            print("new key "+hex(self.key))
            print("we're at"+hex(self.Archive.tell()))
            """
            if self.Archive.tell() == self.Size:
                break
        # print("holy shit, we made it.")
