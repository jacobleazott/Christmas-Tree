
file = open(f'auto_coordinates.txt', 'r')
write_File = open(f'auto_corrected_coordinates.txt', 'w')
coord = file.readline().split()

write_File.write(f"{int(coord[0]) - 350} {int(coord[1]) + 1} {int(coord[2]) + 13}/n")

file.close()
write_File.close()
