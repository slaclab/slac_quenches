import matplotlib.pyplot as plt
import numpy as np
import re # importing regular expression module

# changes with each file
filename = 'ACCL_L3B_3180_20220630_154604_QUENCH.txt'
faultname = 'ACCL:L3B:3180:CAV:FLTAWF'
timestamp = '2022-06-30_15:04.712966'

# read the entire file into memory
with open(filename,'r') as file:
    lines = file.readlines()

# find the start and end lines based on keywords
start_line = None 
end_line = None
data_lines = []

# flag to indicate that we are in the right section
in_section = False

# for i, line in enumerate(lines):
#     print(f"Checking line {i}: {line.strip()}")
#     if faultname in line and timestamp in line:
#         start_line = i
#         in_section = True
#         print(f"Found section start at line {i}")
#     elif faultname not in line and timestamp not in line and in_section:
#         end_line = i
#         print(f"Found section and end at line {i}")
#         break
#     if in_section:
#         data_lines.append(line.strip()) # extracting data lines

for i, line in enumerate(lines):
    print(f"Checking line {i}")
    if "ACCL:L3B:3180:CAV:FLTAWF 2022-06-30_15:46:04.712966" in line:
        start_line = i
        in_section = True
        print(f"Found section start at line {i}")
    elif "ACCL:L3B:3180:CAV:FLTAWF 2022-06-30_15:46:04.712966" not in line and in_section:
        end_line = i
        print(f"Found section and end line at {i}")
        break
    if in_section:
        data_lines.append(line.strip()) # extracting data lines

# shows only first 10 to be brief
print(f"Extracted data lines: {data_lines[:10]}...")

# extracting numeric data from each line using regular expressions
data = []
for line in data_lines:
    # using regex to find all numbers in the line
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line) #matches integers or floats
    if numbers:
        # convering the first number found to float and add it to data list
        data.append([float(num) for num in numbers]) # add all numbers in the line to data
    else:
        print(f"Skipping line with no numeric data: {line}")

# convert the data lines to floats
# try:
#     data = [float(line) for line in data_lines]
#     print(f"Converted data: {data}")
# except ValueError as e:
#     print (f"Error converting data: {e}")
#     data = []

# start_line = 52
# end_line = 53
# data_lines = lines[start_line:end_line]
# data = [float(line.strip()) for line in data_lines]

# check that the data is collected
print(f"Total number of data points collected: {len(data)}")
if len(data) > 0: 
    print(f"First few data points: {data[:10]}")
else:
    print("No valid data extracted.")

if data: 
    # check the min and max values of the data
    data_min = np.min(data)
    data_max = np.max(data)
    print(f"Data range: min = {data_min}, max = {data_max}")

    # time axis assuming uniform spacing
    time = list(range(len(data)))

    # plotting the data
    plt.figure(figsize=(14,6))
    plt.plot(time, data, label=filename, color='blue')
    plt.xlabel('Seconds')
    plt.ylabel('MV')
    plt.title('Quench Waveform')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
else:
    print("No data was extracted, no plot will be displayed.")