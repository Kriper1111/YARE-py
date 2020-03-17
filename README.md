# YARE-py
**Y**et **A**nother **R**GSSAD **E**xtractor, now in Python.

I know, something like this already exists elsewhere, but their version is messy.

This repository is **Work in Progress**. That means I'm a lazy clump of moss and would update it from time to time.

If you dare enough to use it, you would need Python 3+.
<br>Are there any benefits of using this over other extractors out there?
Well it worked on the archive on which others failed.

**How to install**
1. Again, you need Python 3. Go grab it from their website
  * for Android use QPython
2. Download this repo and unzip wherever you like
3. Move onto **Usage** step

**How  to use**
<br>There are two versions of it: `app-prompt.py` and `app-told.py`.
  * `app-prompt.py` is more user-friendly: you run it and it asks you for things it needs. **Keep  in mind** that it can only detect game archives that are *inside of the script folder*. I suggest using it on Android since you can't specify command-line arguments there.
  * `app-told.py` takes options it needs from command-line arguments. Run `app-told.py -h` for some bit of help. If you don't know what are those, use `app-prompt.py`.
<br>

*RGSSAD File format*
<br>I'm not sure whether or not can I share this. RGSSAD files have two versions: v1 (.rgssad, .rgss2a) and v3 (.rgss3a). They are similar, but have their differences.
   * **RGSSAD v1** has the following structure:
       
       [header *8*] [filename_length *4*] [filename *filename_length*] [file_size *4*] [file_data *file_size*] ...
       
       where number in italics is length of the block.
       
       Every block is encrypted with a key, that "permutates" every decryption. Permutation is done by multiplying the key by 7 and adding 3. Default key is `0xDEADCAFE`. To decrypt data, we have to bitwise XOR the encrypted data with the key. The key has to be 4 bytes long, otherwise garbage data would appear.
   
   * **RGSSAD v3** however doesn't permutate its key every metadata decryption. (Metadata being is filename, file_size, etc.). This format also has different structure:
       
       [header *8*] [metadata_key *4*] [file_data_offset *4*] [file_size *4*] [file_key *4*] [filename_length *4*] [filename *filename_length*] ... @file_data1_offset:[file_data1 *file_size1*] ...
       
       Also this format of archives uses separate key for file data encryption, though, the same enryption method as v1. File metadata is encrypted using *metadata_key* that is multiplied by 9 and increased by 3.
       
<br>

*It's more like "can I do this" project then anything else.*

*This is not a Jojo refrence.*
