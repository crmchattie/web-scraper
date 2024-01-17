# Define a function to check if the content is 'empty'
def is_content_empty(value, key):
    if key in ['title', 'name', 'meta_description', 'navigation', 'main_content']:
        return value.startswith("No") and value.endswith("found")
    elif key == 'headings':
        return value == {'h1': [], 'h2': [], 'h3': [], 'h4': [], 'h5': [], 'h6': []}
    elif key == 'links':
        return value == {'internal': []}
    return False

def truncate_string(input_string, max_length=5000):
    """Truncate a string to a maximum length, adding an ellipsis if truncated."""
    return (input_string[:max_length] + '...') if len(input_string) > max_length else input_string

def simplify_structure(data):
    return truncate_string(str(data))  # Convert other types to string

def display_top(statistics, limit=10):
    print("Top {} lines".format(limit))
    for index, stat in enumerate(statistics[:limit], 1):
        frame = stat.traceback[0]
        filename = getattr(frame, 'filename', 'unknown')
        lineno = getattr(frame, 'lineno', 'unknown')
        print(f"#{index}: {filename}:{lineno}: {stat.size / 1024:.1f} KiB")
        for line in stat.traceback.format():
            print(line)

    other = statistics[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print(f"{len(other)} other: {size / 1024:.1f} KiB")
    total = sum(stat.size for stat in statistics)
    print(f"Total allocated size: {total / 1024:.1f} KiB")