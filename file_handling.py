File_handle = open("3a. Task1Data (3).txt", "r")
read_line = File_handle.readline()

while len(read_line) > 0:
    print(read_line)
    read_line = File_handle.readline()
File_handle.close()