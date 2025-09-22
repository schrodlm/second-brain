Semantics basically means "**the meaning of**".

It may help to look at a more familiar case to explain the term.

Consider:

```cpp
int a = 3;
int b = 5;

int c = a + b;
```

The value of `a + b` is `8` because the **semantics** of the `+` operator is to take the _numerical sum_ of its operands.

Now consider this:

```cpp
std::string a = "hello";
std::string b = "world";

std::string c = a + b;
```

The value of `a + b` is `"helloworld"` because the **semantics** of the `+` operator is to _concatenate_ its operands.

The `+` operator, when used with `std::string` is said to have _different_ **semantics** from when it is used with numerical types.

It has a different **meaning**.

Now consider _copy_ and _move_ semantics:

```cpp
std::string a = "hello";
std::string b;

b = a; // b receives a copy of a's value

b = std::string("hello"); // the temporary value is moved into b
```

We have the same operator `=` which has a different **meaning** in different situations. Again we say is has _different_ **semantics**.

The first case has _copy semantics_ and the second case has _move semantics_.