import re
import numpy as np

def parse_eyetracking_data(file_string):
  """
  Parses raw eyetracking data from a string, extracting gaze coordinates.
  Lines with 'nan' values are filtered out.

  Args:
    file_string (str): The raw content of the eyetracking data file.

  Returns:
    tuple: A tuple containing two NumPy arrays:
           - left_eye_coords (np.array): Coordinates of the left eye (N, 2).
           - right_eye_coords (np.array): Coordinates of the right eye (N, 2).
  """
  lines = file_string.split('\n')

  # List to store parsed data points (each will be a list of 2 eye coords)
  parsed_data_points = []

  # Regex pattern to find floating point numbers or 'nan' within parentheses,
  # specifically targeting the ((x, y)) format and capturing both numerical and 'nan' values.
  # Group 1 for X, Group 2 for Y.
  pattern = r"\(\(([-]?\d+\.\d+|nan),\s*([-]?\d+\.\d+|nan)\)\)"

  for line in lines:
      # We only care about lines that contain both "Left eye" and "Right eye" data
      if "Left eye: ((" in line and "Right eye: ((" in line:
          # Find all matches for the pattern in the line
          matches = re.findall(pattern, line)
          
          # Check if we found two sets of coordinates (one for each eye)
          if len(matches) == 2:
              left_gaze_str_x, left_gaze_str_y = matches[0]
              right_gaze_str_x, right_gaze_str_y = matches[1]
              
              # Convert strings to floats, handling 'nan'
              left_x = float(left_gaze_str_x) if left_gaze_str_x != 'nan' else np.nan
              left_y = float(left_gaze_str_y) if left_gaze_str_y != 'nan' else np.nan
              right_x = float(right_gaze_str_x) if right_gaze_str_x != 'nan' else np.nan
              right_y = float(right_gaze_str_y) if right_gaze_str_y != 'nan' else np.nan

              parsed_data_points.append([[left_x, left_y], [right_x, right_y]])

  # Convert the list of lists to a NumPy array for easier manipulation
  data_array = np.array(parsed_data_points)

  # Filter out rows where either eye's coordinates contain NaN
  # np.isnan(data_array).any(axis=(1, 2)) checks if any NaN exists in the (x,y) for either eye in a row.
  # We want to keep rows that DO NOT have NaN, so we use ~ (logical NOT).
  valid_samples_mask = ~np.isnan(data_array).any(axis=(1, 2))
  filtered_data = data_array[valid_samples_mask]

  if filtered_data.size == 0: # Check if the filtered array is empty
      return np.array([]), np.array([]) # Return empty arrays if no valid data

  # Separate left and right eye data
  left_eye_coords = filtered_data[:, 0, :]
  right_eye_coords = filtered_data[:, 1, :]

  return left_eye_coords, right_eye_coords