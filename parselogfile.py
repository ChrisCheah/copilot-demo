# import regex
import re

from pkg_resources import cleanup_resources

# read log file and parse it


# read log file
def read_log_file(log_file):
    with open(log_file, 'r') as f:
        log_lines = f.readlines()
    return log_lines

def get_lines_with_keywords(log_lines, keywords):
    lines_with_keywords = []
    for line in log_lines:
        for keyword in keywords:
            if keyword in line:
                lines_with_keywords.append(line)
                break # fix duplicate lines
    return lines_with_keywords

def get_lines_with_keyword(log_lines, keyword):
    lines_with_keyword = []
    for line in log_lines:
        if keyword in line:
            lines_with_keyword.append(line)
    return lines_with_keyword

# use regex to replace "Thu Jul 01 21, 07:55:06 4885 " with "Thu, 21/Jul/01, 07:55:06, 4885 "
def convert_time_format_1(log_lines):
    lines = []
    for line in log_lines:
        line = re.sub(r'(\w+)\s(\w+)\s(\w+)\s(\d+),\s(\d+):(\d+):(\d+)\s(\d+)', r'\1,\4/\2/\3,\5:\6:\7,\8', line)
        lines.append(line)
    return lines


# use regex to replace "Thu Jul 01 21, 07:55:06 4885 - EntranceLast Changed by 0.000, ExitLast Changed by 0.000\n" with "Thu, 21/Jul/01,07:55:06, 4885, EntranceLast Changed by 0.000, ExitLast Changed by 0.000\n"
def convert_time_format_2(log_lines):
    lines = []
    for line in log_lines:
        # line = re.sub(r'(\w+)\s(\w+)\s(\w+)\s(\d+),\s(\d+):(\d+):(\d+)\s(\d+)\s-\s(.*)', r'\1,\4/\2/\3,\5:\6:\7,\8,\9', line)
        line = re.sub(r'(\w+)\s(\w+)\s(\w+)\s(\d+),\s(\d+):(\d+):(\d+)\s(\d+)\s-\s(.*)\n', r'\4/\2/\3,\5:\6:\7', line)
        lines.append(line)
    # return log_lines
    return lines

# calcualte time difference in seconds between two lines with date and time information
def calculate_time_diff_between_two_lines(line1, line2):
    time_diff = 0
    line1_date = line1.split(',')[0]
    line1_time = line1.split(',')[1]
    line2_date = line2.split(',')[0]
    line2_time = line2.split(',')[1]
    if line1_date == line2_date:
        time_diff = (int(line2_time.split(':')[0]) - int(line1_time.split(':')[0])) * 3600 + (int(line2_time.split(':')[1]) - int(line1_time.split(':')[1])) * 60 + (int(line2_time.split(':')[2]) - int(line1_time.split(':')[2]))
    else:
        time_diff = (int(line2_time.split(':')[0]) - int(line1_time.split(':')[0])) * 3600 + (int(line2_time.split(':')[1]) - int(line1_time.split(':')[1])) * 60 + (int(line2_time.split(':')[2]) - int(line1_time.split(':')[2]))
    return time_diff

# def add_time_diff_to_log_lines_0(log_lines, line_index):
#     log_lines_from_log_file = []
#     for i in range(line_index, len(log_lines)-1):
#         line1 = log_lines[line_index]
#         line2 = log_lines[line_index + 1]
#         time_diff = calculate_time_diff_between_two_lines(line1, line2)
#         log_lines_from_log_file.append(log_lines[i] + str(time_diff))
#     return log_lines_from_log_file

def add_time_diff_to_log_lines(log_lines):
    log_lines_from_log_file = []
    for i in range(len(log_lines)-1):
        line1 = log_lines[i]
        line2 = log_lines[i + 1]
        time_diff = calculate_time_diff_between_two_lines(line1, line2)
        log_lines_from_log_file.append(log_lines[i] + ',' + str(time_diff) + '\n')
    return log_lines_from_log_file

# def read_two_lines_from_log_file(log_lines, line_index):
#     line1 = log_lines[line_index]
#     line2 = log_lines[line_index + 1]
#     return line1, line2


# split file path into array of strings
def split_file_path(file_path):
    file_path_array = file_path.split('/')
    return file_path_array

# construct filename from array of strings
def construct_filename(file_path_array):
    filename = './' + file_path_array[2] + '_' + file_path_array[3] + '_' + file_path_array[4] + '.csv'
    return filename

# write to file
def write_to_file(log_lines_from_log_file, filename):
    with open(filename, 'w') as f:
        header = 'Date,Time,TimeDiff\n'
        f.write(header)
        for line in log_lines_from_log_file:
            f.write(line)

# default file from log path
log_file = './log/A01/JDC-BTU/JDC301/BoardLogOut.txt'
keywords = ['EntranceLast', 'ExitLast Changed']
log_lines = read_log_file(log_file)
log_lines = get_lines_with_keywords(log_lines, keywords)
log_lines = convert_time_format_2(log_lines)
log_lines = add_time_diff_to_log_lines(log_lines)
filename = construct_filename(split_file_path(log_file))
write_to_file(log_lines, filename)
print(log_lines)