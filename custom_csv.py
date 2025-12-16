import io

class CustomCsvReader:
    """
    A custom CSV reader that parses a file-like object acting as an iterator.
    Handles quoted fields, escaped quotes, and embedded newlines.
    """

    def __init__(self, file_obj):
        """
        Initialize the reader with a file object.
        
        Args:
            file_obj: An open file object (opened in text mode).
        """
        self.file = file_obj
        # We wrap the file in a generator to allow char-by-char processing 
        # while keeping the logic clean.
        self._char_gen = self._file_char_generator()
        self._lookahead = None

    def __iter__(self):
        return self

    def _file_char_generator(self):
        """Yields characters one by one from the file object."""
        while True:
            chunk = self.file.read(4096)  # Read in chunks for efficiency
            if not chunk:
                break
            for char in chunk:
                yield char

    def _get_next_char(self):
        """Retrieves next char, handling the lookahead buffer."""
        if self._lookahead is not None:
            char = self._lookahead
            self._lookahead = None
            return char
        return next(self._char_gen, None)

    def _peek_char(self):
        """Peeks at the next character without consuming it."""
        if self._lookahead is None:
            self._lookahead = next(self._char_gen, None)
        return self._lookahead

    def __next__(self):
        """
        Parses and returns the next row as a list of strings.
        Raises StopIteration when no more data is available.
        """
        # Check if we are at EOF before starting a row
        if self._peek_char() is None:
            raise StopIteration

        row = []
        current_field = []
        in_quotes = False
        
        while True:
            char = self._get_next_char()

            if char is None:
                # End of file
                if current_field or row:
                    row.append("".join(current_field))
                break

            if in_quotes:
                if char == '"':
                    # Check next char to see if it is an escaped quote ("")
                    next_char = self._peek_char()
                    if next_char == '"':
                        current_field.append('"')
                        self._get_next_char()  # Consume the second quote
                    else:
                        in_quotes = False  # End of quoted field
                else:
                    current_field.append(char)
            else:
                if char == '"':
                    in_quotes = True
                elif char == ',':
                    row.append("".join(current_field))
                    current_field = []
                elif char == '\n':
                    row.append("".join(current_field))
                    return row
                elif char == '\r':
                    # Handle CRLF or just CR
                    next_char = self._peek_char()
                    if next_char == '\n':
                         self._get_next_char() # Consume \n
                    row.append("".join(current_field))
                    return row
                else:
                    current_field.append(char)
        
        if row:
            return row
        else:
            raise StopIteration


class CustomCsvWriter:
    """
    A custom CSV writer that writes lists of strings to a file-like object.
    Automatically quotes fields containing delimiters, quotes, or newlines.
    """

    def __init__(self, file_obj):
        """
        Initialize the writer with a file object.

        Args:
            file_obj: An open file object (opened in 'w' text mode).
        """
        self.file = file_obj

    def _escape_field(self, field):
        """
        Prepares a single field for CSV writing.
        - Converts non-strings to strings.
        - Escapes double quotes.
        - Wraps in quotes if necessary.
        """
        field_str = str(field)
        
        # Check if quoting is required
        # Trigger: comma, double quote, newline, or carriage return
        needs_quotes = any(c in field_str for c in (',', '"', '\n', '\r'))

        if needs_quotes:
            # Replace single " with double ""
            escaped_str = field_str.replace('"', '""')
            return f'"{escaped_str}"'
        
        return field_str

    def writerow(self, row):
        """
        Writes a single row (list of fields) to the file.
        
        Args:
            row: A list of items to write.
        """
        processed_row = [self._escape_field(field) for field in row]
        line = ",".join(processed_row) + "\n"
        self.file.write(line)

    def writerows(self, rows):
        """
        Writes multiple rows to the file.

        Args:
            rows: An iterable of lists.
        """
        for row in rows:
            self.writerow(row)