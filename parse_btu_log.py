# Purpose
#  Parse the BTU log file and extract the data.
#   - The log file is a text file with data lines, no header lines
#   - extract line with the following keywords: "EntranceLast", "ExitLast Changed"
#   - Some data lines are comma separated
#   - Data has non standard date and time information
#   - The data is in the format: "Fri Apr 08 22, 09:17:41 4338 - EntranceLast Changed by 0.000, ExitLast Changed by 0.000"
#   - The data shall be converted into a CSV file with the following columns: "Date", "Time", "TimeDiff"

# read the log file in lines
def read_log_file(log_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()
    return lines

def extract_data(lines):
    # extract the data lines
    data_lines = []
    for line in lines:
        if "EntranceLast" in line or "ExitLast Changed" in line:
            # split the line with spaces, keep the first 5 elements
            line_list = line.split()[0:5]
            # join the list elements into a string
            line_str = " ".join(line_list)
            # append the line to the list
            data_lines.append(line_str)
    return data_lines

log_file_name = './log/A01/JDC-BTU/JDC301/BoardLogOut.txt'
lines = read_log_file(log_file_name)
lines = extract_data(lines)
print(lines)
