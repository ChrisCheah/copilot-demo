# Purpose
#  Parse the BTU log file and extract the data.
#   - The log file is a text file with data lines, no header lines
#   - extract line with the following keywords: "EntranceLast", "ExitLast Changed"
#   - Some data lines are comma separated
#   - Data has non standard date and time information
#   - The data is in the format: "Fri Apr 08 22, 09:17:41 4338 - EntranceLast Changed by 0.000, ExitLast Changed by 0.000"
#   - The data shall be converted into a CSV file with the following columns: "Date", "Time", "TimeDiff"

# import the datetime module
import datetime

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
            line_list = line.split()[1:5]
            # join the list elements into a string
            line_str = " ".join(line_list)
            # append the line to the list
            data_lines.append(line_str)
    return data_lines

# calculate time diff between two lines
# the date is in the format: "MMM DD YY, HH:MM:SS"
def calc_time_diff(line1, line2):
    # convert the date and time into a datetime object
    line1_dt = datetime.datetime.strptime(line1, "%b %d %y, %H:%M:%S")
    line2_dt = datetime.datetime.strptime(line2, "%b %d %y, %H:%M:%S")
    # calculate the time difference
    time_diff = line2_dt - line1_dt
    return time_diff

def calc_time_diff_list(lines):
    # calculate the time difference between the lines
    time_diff_list = []
    for i in range(len(lines)-1):
        time_diff = calc_time_diff(lines[i], lines[i+1])
        # concatenate the time difference to the line, separated by a comma and append to the list
        time_diff_list.append(str(time_diff) + ", " + lines[i+1])
    return time_diff_list

log_file_name = './log/A01/JDC-BTU/JDC301/BoardLogOut.txt'
lines = read_log_file(log_file_name)
lines = extract_data(lines)
lines = calc_time_diff_list(lines)
print(lines)
