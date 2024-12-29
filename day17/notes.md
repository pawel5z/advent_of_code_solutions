### Puzzle's machine equivalent in pseudocode

```
A <- ?
B <- 0
C <- 0

B <- A mod 8
B <- B xor 1
C <- A div pow(2, B)
B <- B xor 4
A <- A div 8         # shift right by one octal digit
B <- B xor C
print B mod 8        # print least significant octal digit
if A is not 0:
    repeat
```

### Analysis

Let $d$ be the current least significant octal digit of $A$ register, i.e. $A \mod 8$.
Then the printed digit is equal to
$$[(d \oplus 5) \oplus (A \div 2^{d \oplus 1})] \mod 8$$
where $\oplus$ is bitwise XOR and $\div$ is integer division.
