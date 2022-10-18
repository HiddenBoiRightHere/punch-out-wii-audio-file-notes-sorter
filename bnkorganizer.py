import tkinter as tk
from tkinter import filedialog as fd
import os
import sys



def OrganizerFull(file_path, file_path2, file_path3, interleaveCertainty):


    # Open two files. "rb" defines "read" and "binary"
    wem_original = open(file_path, "rb")
    dsp_replacing = open(file_path2, "rb")

    #Find value at offset 0x87 for both 1 and 2 channels for wem.
    wem_original.seek(0x87)
    wem_originalChannelByte = wem_original.read(1)


    #Print value at offset 0x87 for both 1 and 2 channels for wem.
    w_o = wem_originalChannelByte.hex()

    #Find value at offset 0x4B for both 1 and 2 channels for dsp.
    dsp_replacing.seek(0x4B)
    dsp_replacingChannelBytes = dsp_replacing.read(2)

    #Print value at offset 0x4B for both 1 and 2 channels for dsp.
    d_r = dsp_replacingChannelBytes.hex()

    #Compares if files have the same set of channels.

    if w_o == "2e" and d_r == "0000":
        wem_original.seek(0xDC)
        wem_originalDataLength = wem_original.read(4)
        progressLabel = tk.Label(root, text = "These one-channel files' channels are compatible.")
        progressLabel.pack()
    elif w_o == "5c" and d_r == "0204":
        wem_original.seek(0xFC)
        wem_originalDataLength = wem_original.read(4)
        progressLabel = tk.Label(root, text="These two-channel files' channels are compatible.")
        progressLabel.pack()
    else:
        progressLabel = tk.Label(root, text="These files' channels are not compatible. Press the button below to exit.")
        progressLabel.pack()
        var = tk.IntVar()
        WaitConfirmation = tk.Button(root, text="Okay", command=lambda: var.set(1))
        WaitConfirmation.pack()
        root.wait_variable(var)
        WaitConfirmation.pack_forget()
        sys.exit()




    #Compares the audio lengths determined by the data tag.

    #Finds data length of wem files


    #Finds data length of .dsp files

    dsp_replacing.seek(0x04)
    dsp_replacingDataLength = dsp_replacing.read(4)
    #Converts byte size of file information into integers.

    wem_originalInt = int.from_bytes(wem_originalDataLength, byteorder='big')
    dsp_replacingInt = int.from_bytes(dsp_replacingDataLength, byteorder='big')


    #if statement for calculating size
    #if size of dsp > size of wem, give user a warning but ability to proceed.


    small = 0
    same = 0
    large = 0

    if dsp_replacingInt > wem_originalInt:
        small = 1
        warnText = tk.Label(root, text = "Your .wem file allows less data than your .dsp file. Please note that your data will be cut off. Continue?", wraplength=500)
        warnText.pack()
        var = tk.IntVar()
        WaitConfirmation = tk.Button(root, text="Okay", command=lambda: var.set(1))
        WaitConfirmation.pack()
        root.wait_variable(var)
        WaitConfirmation.pack_forget()
    elif dsp_replacingInt == wem_originalInt:
        warnText = tk.Label(root, text = "Your file is exactly the same size!")
        warnText.pack()
        same = 1
    else:
        large = 1
        warnText = tk.Label(root, text="Your .wem file allows more data than your dsp file provides. Please note that additional null values of silence will replace the necessary length needed. Continue?", wraplength=500)
        warnText.pack()
        var = tk.IntVar()
        WaitConfirmation = tk.Button(root, text="Okay", command=lambda: var.set(1))
        WaitConfirmation.pack()
        root.wait_variable(var)
        WaitConfirmation.pack_forget()

    #4. Determine whether overwritten file length is too short to create a file. (as I'm tired of this, it is a feature that will have to wait.)
    #if size of wem is smaller than 2000, use stacking only for now and warn user (needs to be tested)
    # 5. Once all the basic checks are done, begin taking out the necessary data. The coefficient(s) which depend on channels and actual audio data.
    #create new file that is exact copy of wem

    wemOutputFile = open(file_path3 + r"/wemOutFile.wem", "wb")
    wem_original.seek(0x0)

    if w_o == "2e":
        wemReadInOutHeaders = wem_original.read(0xE0)
        wemOutputFile.write(wemReadInOutHeaders)
    else:
        wemReadInOutHeaders = wem_original.read(0x100)
        wemOutputFile.write(wemReadInOutHeaders)


    #read and save coefficients from dsp

    dsp_replacing.seek(0x1C)
    dspReadInOutCoefficients = dsp_replacing.read(0x2E)
    # write coefficients into new wem
    wemOutputFile.seek(0x88)
    wemOutputFile.write(dspReadInOutCoefficients)

    if w_o == "5c":
        dsp_replacing.seek(0x7C)
        dspReadInOutCoefficients = dsp_replacing.read(0x2E)
        wemOutputFile.seek(0xB6)
        wemOutputFile.write(dspReadInOutCoefficients)
    else:
        pass







    #split into blocks of 2000. if less than 2000, stack and warn user. (or well, too bad, I won't warn you about it.)
    if w_o == "2e":
        dsp_replacing.seek(0x60)
    else:
        dsp_replacing.seek(0xC0)
    i = 1

    chunk_size = 0x2000
    chunk = dsp_replacing.read(chunk_size)
    oddByteCollection = open(file_path3 + r"\oddByteList", "wb")
    evenByteCollection = open(file_path3 + r"\evenByteList", "wb")


    while chunk:
        if (i % 2) == 1:
            oddByteCollection.write(chunk)
            chunk = dsp_replacing.read(chunk_size)
            i = i + 1
        else:
            evenByteCollection.write(chunk)
            chunk = dsp_replacing.read(chunk_size)
            i = i + 1



    #close files to allow reading later
    oddByteCollection.close()
    evenByteCollection.close()

    oddByteCollectionWrite = open(file_path3 + r"\oddByteList", "rb")
    evenByteCollectionWrite = open(file_path3 + r"\evenByteList", "rb")

    oddByteCollectionWrite.seek(0x0)
    evenByteCollectionWrite.seek(0x0)

    #determine if interleave is necessary, then choose to interleave.
    if w_o == "2e":
        fullCollection = open(file_path3 + r"\totalList", "wb")
        dsp_replacing.seek(0x60)
        dspDataSC = dsp_replacing.read()
        fullCollection.write(dspDataSC)
        fullCollection.close()
        fullCollectionWriter = open(file_path3 + r"\totalList", "rb")
        fullCollectionWriterFiller = fullCollectionWriter.read()
    #write only necessary data
    totalOdd = oddByteCollectionWrite.read()
    totalEven = evenByteCollectionWrite.read()

    oddByteCollectionWrite.seek(0x00)
    evenByteCollectionWrite.seek(0x00)



    if w_o == "2e":
        wemOutputFile.seek(0xE0)
    else:
        wemOutputFile.seek(0x100)




    # 7. Implant replacing data into the file.
    #determines what to write into output file based on size
    #large means that the wem file will accept more bytes, thus nulls need to fill in the blanks
    if large == 1:
        if interleaveCertainty == 0:
            wemOutputFile.write(totalOdd)
            wemOutputFile.write(totalEven)
            totalExtraNull = wem_originalInt - dsp_replacingInt
            nullCounter = 0
            while nullCounter < totalExtraNull:
                wemOutputFile.write(b"\x00")
                nullCounter = nullCounter + 1
        else:
            oddByteCollectionWrite.seek(0x00)
            evenByteCollectionWrite.seek(0x00)
            while oddByteCollectionWrite or evenByteCollectionWrite:
                oddInterl = oddByteCollectionWrite.read(0x08)
                evenInterl = evenByteCollectionWrite.read(0x08)
                wemOutputFile.write(oddInterl)
                wemOutputFile.write(evenInterl)
                if oddInterl == b'':
                    break
            totalExtraNull = wem_originalInt - dsp_replacingInt
            nullCounter = 0
            while nullCounter < totalExtraNull:
                wemOutputFile.write(b"\x00")
                nullCounter = nullCounter + 1


    elif small == 1:
        #small means that the wem cannot take all the bytes, thus the file must cut off the data.
        #find the limit
        if interleaveCertainty == 0:
            differenceLarge = dsp_replacingInt - wem_originalInt
            writeTotal = wem_originalInt // 2
            #split into odd and even chunks
            oddByteCollectionWrite.seek(0x0)
            evenByteCollectionWrite.seek(0x0)
            largeOdd = oddByteCollectionWrite.read(writeTotal)
            largeEven = evenByteCollectionWrite.read(writeTotal)
            #write into file stacked at max length
            wemOutputFile.write(largeOdd)
            wemOutputFile.write(largeEven)
        else:
            oddByteCollectionWrite.seek(0x00)
            evenByteCollectionWrite.seek(0x00)
            writeTotal = wem_originalInt // 2
            #gets total that can be written
            largeOdd = oddByteCollectionWrite.read(writeTotal)
            largeEven = evenByteCollectionWrite.read(writeTotal)
            #opens new files to store bytes
            insertlargeOdd = open(file_path3 + r"\intlOdd", "wb")
            insertlargeEven = open(file_path3 + r"\intlEven", "wb")
            #writes bytes into files
            insertlargeOdd.write(largeOdd)
            insertlargeEven.write(largeEven)
            #closes files from writing
            insertlargeOdd.close()
            insertlargeEven.close()
            #opens files for reading
            readlargeOdd = open(file_path3 + r"\intlOdd", "rb")
            readlargeEven = open(file_path3 + r"\intlEven", "rb")

            while oddByteCollectionWrite or evenByteCollectionWrite:
                oddInterl = readlargeOdd.read(0x08)
                evenInterl = readlargeEven.read(0x08)
                wemOutputFile.write(oddInterl)
                wemOutputFile.write(evenInterl)
                if oddInterl == b'':
                    break
    else:
        if interleaveCertainty == 0:
            #same, so write it all out.
            wemOutputFile.write(totalOdd)
            wemOutputFile.write(totalEven)
        else:
            oddByteCollectionWrite.seek(0x00)
            evenByteCollectionWrite.seek(0x00)
            while oddByteCollectionWrite or evenByteCollectionWrite:
                oddInterl = oddByteCollectionWrite.read(0x08)
                evenInterl = evenByteCollectionWrite.read(0x08)
                wemOutputFile.write(oddInterl)
                wemOutputFile.write(evenInterl)
                if oddInterl == b'':
                    break

    oddByteCollectionWrite.close()
    evenByteCollectionWrite.close()
    os.remove(file_path3 + r"/oddByteList")
    os.remove(file_path3 + r"/evenByteList")
    if interleaveCertainty == 1:
        if small == 1:
            readlargeOdd.close()
            readlargeEven.close()
            os.remove(file_path3 + r"\intlOdd")
            os.remove(file_path3 + r"\intlEven")
        else:
            pass
    else:
        pass

    if w_o == "2e":
        fullCollectionWriter.close()
        os.remove(file_path3 + r"/totalList")
    else:
        pass
