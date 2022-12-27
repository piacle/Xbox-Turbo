from shutil import get_terminal_size

def spaces(length: int) -> str:
    return " " * length

def center_x(text: str = None) -> str:
    columns = get_terminal_size().columns
    if text is None:
        return spaces(columns // 2 - 1 // 2)
    else:
        return '\n'.join([f"{spaces(columns // 2 - len(line) // 2)}{line}" for line in text.splitlines()])


def center_y(text: str = None, return_only_lines: bool = True) -> str:
    newlines = "\n".join(['' for _ in range(get_terminal_size().lines // 4)])
    if return_only_lines:
        return newlines
    else:
        if text is None:
            return newlines
        return newlines + text


def center(text: str = None) -> str:
    if text is None:
        raise TypeError
    return center_y() + center_x(text=text)  # y over x duh I learned this in grade 2
