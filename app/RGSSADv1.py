import os, sys

from app import RGSSAD

class RGSSADv1(RGSSAD.Base):
    def read(self):
        print("Reading v1 or v2 file with size of "+hex(self.Size))
        self.Archive.seek(8, 0)
    
        while True:
            print(">> It's a new cycle<<")
            length = self.DecryptNumber(self.Archive.read(4))
            filename = self.DecryptName(self.Archive.read(length))
            size = self.DecryptNumber(self.Archive.read(4))
            offset = self.Archive.tell()
            File = RGSSAD.EncryptedData(filename, offset, size, self.key)
            self.ArchivedData.append(File)
            self.Archive.seek(size, 1)
            print("file name "+filename)
            print("file size "+str(size))
            print("offset "+hex(offset))
            print("new key "+hex(self.key))
            print("we're at"+hex(self.Archive.tell()))
            if self.Archive.tell() == self.Size-1:
                break
        print("holy shit, we made it.")

# DecryptFiles(


"""
def DecryptInteger(integer):
    global key
    print("!! Decrypting {} using key {} !!".format(integer, hex(key)))
    integer = int.from_bytes(integer, "little")
    integer = shorten(integer)
    print("input int "+hex(integer))
    decrypted = integer ^ key
    key = (key*7)+3
    key = shorten(key)
    decrypted = shorten(decrypted)
    print("int decrypted "+str(decrypted))
    print("!! Decryption done !!")
    return decrypted
    
def DecryptName(encryptedName):
    decryptedName = []
    global key
    for i in range(0, len(encryptedName)):
        decryptedName.append(encryptedName[i] ^ (key & 0xFF))
        key = (key*7) + 3
        #print(hex(key))
        key = shorten(key)
    decryptedName = bytearray(decryptedName).decode('utf-8')
    return decryptedName

def DecryptFiles(Archive, List):
    for Index, File in enumerate(List, start=1):
        decrypted = []
        Archive.seek(File.offset, 0)
        encrypted = Archive.read(File.size)
        print("Decoding file {}; #{} of {}".format(File.name, Index, len(List)))
        j=0
        Tkey = File.key
        for byte in encrypted:
            j = j % 5
            #print(j)
            if j==4:
                j = 0
                Tkey=(Tkey*7)+3
                Tkey=shorten(Tkey)
            bKey = Tkey.to_bytes(4, "little")
            #print(type(bKey[1]))
            decrypted.append(byte ^ bKey[j])
            j+=1
        filename = "./Extracted/"+File.name.replace("\\", "/")
        print("Decrypted all the bytes, storing them into {}".format(filename))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        output = open(filename, "wb")
        output.write(bytearray(decrypted))
        output.close()
    print("Extraction and decryption done, enjoy!")
    Archive.close()

if __name__=='__main__':
    read()
"""