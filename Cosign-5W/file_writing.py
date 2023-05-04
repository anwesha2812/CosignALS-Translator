def writeTofile(folder, data, filename, i, seconds): #ap
    # Convert binary data to proper format and write it on Hard Disk
        seconds=str(seconds)
        with open(folder+"/"+filename+str(i)+".bmp", 'wb') as file:
            file.write(data)

