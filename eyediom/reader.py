def read_file_to_string(filepath):
    """
    Read a file and return its content as a string.
    
    Args:
        filepath (str): The path to the file to be read.
        
    Returns:
        str: The content of the file.
    """
    with open(filepath, 'r') as file:
        return file.read()