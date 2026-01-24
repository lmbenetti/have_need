path = 'ids_todo_lisandro.txt'

def count_lines(path, has_header=True):
    with open(path, "r", encoding="utf-8") as f:
        count = sum(1 for _ in f)
    return count - 1 if has_header else count

print(count_lines(path, has_header=False))