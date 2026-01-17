def count_lines(path, has_header=True):
    with open(path, "r", encoding="utf-8") as f:
        count = sum(1 for _ in f)
    return count - 1 if has_header else count

def read_and_update_value(path, new_value):
    with open(path, "r", encoding="utf-8") as f:
        old_value = f.read().strip()
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(new_value))
    return int(old_value)

extracted = count_lines("releases_have_want.tsv")
last = read_and_update_value("last.txt", extracted)
total = extracted - last

print("Last check, {last} lines were extracted. Now {extracted} lines are extracted. Therefore, {total} new lines were added.".format(last=last, extracted=extracted, total=total))


