import re
import numpy as np

def parse_eyetracking_data(file_string):

  lines = file_string.split('\n')
  lines = [line.split('\t') for line in lines]

  pattern = r"(\d+\.\d+)"

  parsed = [[[float(x) for x in re.findall(pattern, field)] for field in line] for line in lines]

  filtered= [line for line in parsed if len(line) == 2 and len(line[0]) == 2 and len(line[1]) == 2]

  data= np.array(filtered)

  left_eye = data[:, 0, :]
  right_eye = data[:, 1, :]

  return left_eye, right_eye