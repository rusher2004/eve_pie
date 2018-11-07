import os

directory = os.fsencode('csv/zkill_history/2012')

dir_array = []

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	dir_array.append(filename)
	print(os.path.abspath(file))

print(len(dir_array))