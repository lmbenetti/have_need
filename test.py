# Function that returns the number of rows in a .txt file
def count_lines_in_file(filename):
    with open(filename, 'r') as file:
        return sum(1 for line in file)
    

# Example usage
filename = 'ids_todo_lisandro.txt'
line_count = count_lines_in_file(filename)
print(f'The file "{filename}" has {line_count} lines.')
