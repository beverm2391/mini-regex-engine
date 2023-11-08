# Core Regex Patterns

1. **Literals**: Matching literal characters exactly as they are.
   - Example: `a` matches 'a'

2. **Character Classes**: Matching any character from a set.
   - Example: `[abc]` matches 'a', 'b', or 'c'

3. **Negated Character Classes**: Matching any character not in a set.
   - Example: `[^abc]` matches any character except 'a', 'b', or 'c'

4. **Dot (.)**: Matching any character except newline.
   - Example: `.` matches 'x', '1', '!', etc.

5. **Anchors**: Matching positions before or after characters.
   - `^` matches the start of the string.
   - `$` matches the end of the string.

6. **Escaped Characters**: Matching characters that are reserved for special use in regex.
   - Example: `\.` matches a literal dot.

7. **Quantifiers**:
   - `*` matches the preceding element zero or more times.
   - `+` matches the preceding element one or more times.
   - `?` matches the preceding element zero or one time.
   - `{n}` matches exactly n occurrences of the preceding element.
   - `{n,}` matches at least n occurrences of the preceding element.
   - `{n,m}` matches from n to m occurrences of the preceding element.

8. **Alternation (|)**: Matching any one of several patterns.
   - Example: `a|b` matches 'a' or 'b'

9. **Groups**:
   - Parentheses `()` are used to define the scope and precedence of the operators and to capture the matched text.

10. **Non-Capturing Groups and Other Group Constructs**:
    - Non-capturing groups `(?:...)` group part of a regex without capturing it.
    - Positive lookahead `(?=...)` asserts that what follows the regex parser's current position must match a certain pattern.
    - Negative lookahead `(?!...)` asserts that what follows the regex parser's current position must not match a certain pattern.

11. **Backreferences**:
    - `\1`, `\2`, etc., match the same string that was matched by a capturing group.

12. **Special Character Classes**:
    - `\d` matches any digit.
    - `\D` matches any non-digit.
    - `\w` matches any alphanumeric character and underscore.
    - `\W` matches any non-word character.
    - `\s` matches any whitespace character.
    - `\S` matches any non-whitespace character.