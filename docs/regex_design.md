# Regex Support Design for UTTR

## Syntax Design

### Regex Literal Syntax
Following UTTR's natural language philosophy, regex patterns will use a readable syntax:

```uttr
$ Basic regex literal using r"pattern" syntax (like Python raw strings)
put r"\d{3}-\d{4}" in phone_pattern;
put r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}" in email_pattern;
```

**Rationale**: The `r"..."` prefix is familiar to Python developers and clearly indicates a regex/raw string.

### Built-in Regex Functions

Following UTTR's natural naming conventions:

1. **regex_match(pattern, text)** - Check if pattern matches from start
   ```uttr
   put regex_match(r"hello", "hello world") in result;  $ Returns true
   ```

2. **regex_search(pattern, text)** - Search for pattern anywhere
   ```uttr
   put regex_search(r"\d+", "I have 42 apples") in found;  $ Returns match object
   ```

3. **regex_replace(pattern, replacement, text)** - Replace matches
   ```uttr
   put regex_replace(r"\d+", "X", "I have 42 apples") in new_text;  $ "I have X apples"
   ```

4. **regex_findall(pattern, text)** - Find all matches
   ```uttr
   put regex_findall(r"\d+", "I have 42 apples and 13 oranges") in numbers;  $ ["42", "13"]
   ```

5. **regex_split(pattern, text)** - Split by pattern
   ```uttr
   put regex_split(r"\s+", "hello   world  test") in words;  $ ["hello", "world", "test"]
   ```

### Match Object Properties

When a regex operation finds a match, it returns a match object with:
- `matched_text` - The matched string
- `start_pos` - Starting position of match
- `end_pos` - Ending position of match
- `groups` - List of captured groups (if any)

```uttr
put regex_search(r"(\d{3})-(\d{4})", "Call 555-1234") in match;
when match:
    show match @ "matched_text";  $ "555-1234"
    show match @ "groups";         $ ["555", "1234"]
end;
```

### Pattern Matching (Future Enhancement)

Integrate with UTTR's switch-case syntax for pattern matching:

```uttr
put input() in user_input;

check user_input:
    whether matches r"^\d{3}-\d{4}$":
        show "Valid phone number!";
    end
    whether matches r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$":
        show "Valid email!";
    end
    default:
        show "Unknown format";
    end
end;
```

## Implementation Components

### 1. Token Type
- Add `TT_REGEX` token type for regex literals

### 2. Lexer
- Recognize `r"..."` syntax
- Handle escape sequences properly
- Support both single and double quotes: `r"..."` and `r'...'`

### 3. AST Node
- `RegexNode` class with pattern and flags properties

### 4. Runtime Value
- `RegexValue` class wrapping Python's `re` module
- Store compiled regex pattern for efficiency
- Provide match/search/replace methods

### 5. Match Object Value
- `MatchValue` class representing regex match results
- Dictionary-like interface for accessing match properties

## Error Handling

Invalid regex patterns should produce clear errors:

```uttr
attempt:
    put r"[invalid(" in bad_pattern;
    put regex_match(bad_pattern, "test") in result;
end
handle as error:
    show "Regex error: " + error_message(error);
end;
```

## Example Use Cases

### Email Validation
```uttr
make function is_valid_email(email):
    put r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" in pattern;
    give regex_match(pattern, email);
end;
```

### Phone Number Formatting
```uttr
make function format_phone(number):
    put regex_replace(r"(\d{3})(\d{3})(\d{4})", r"(\1) \2-\3", number) in formatted;
    give formatted;
end;
```

### Data Extraction
```uttr
put "Prices: $42.99, $13.50, $99.99" in text;
put regex_findall(r"\$\d+\.\d{2}", text) in prices;
cycle each price through prices:
    show price;
end;
```
