A powerful technique used in [[software verification]].

Symbolic execution is a method for analyzing programs by treating program inputs as **symbols** rather than **concrete values**. 
Instead of executing program with specific inputs (like running a function with `x = 5`) symbolic execution runs the program with symbolic variables (such as `x = X`, where `X` can **represent any possible input**)

As the program is executed, the behaviour of the program is tracked in term of **symbolic expressions** that describe how the symbolic inputs interact with the program. These **symbolic expressions represent all possible paths the program can take, based on different inputs**.

## How does symbolic execution works

##### 1. Inputs are symbolic variables
Instead of using concrete values for inputs, the program is executed with symbolic variables. 
For example, if we analyze function `add(x,y)`, `x` and `y` are treaded as symbol `X` and `Y`.

##### 2. Path conditions
As the program executes, it accumulates **path conditions** that describe the conditions under which the program takes certain branches. 
For example, if the program has conditional `if (x > 0)` the symbolic execution will generate two potentional paths:
- one path where `x > 0` is true
- one path where `x <= 0` is true
Each path has an associated **path condition** (a logical expression that must hold for that path to be taken)

##### 3. Explore all paths
Symbolic execution explores all possible execution paths through the program, creating logical formulas that represent the **logical constrains** along each path. This can handle complex branching, loops, and function calls.

##### 4. [[SMT solver]] involvement
At each branch point (or after full symbolic execution) the **logical constraints** are sent to SMT solver since they can be represented with logical formulas. The solver checks whether the path condition is [[SMT#satisfiability | satisfiable]]. 
If it is, that means **there exist some input that would case the program to follow that path**. If the path is unsatisfiable, the program will **never** take that path and it can be pruned from the analysis.


## Example
Let's look at this code and see how it's symbolic execution could look like:
```cpp
int foo(int x, int y) {
	if(x > y) {
		return x-y;
	}
	else
		return y-x;
}
```
Let's treat the inputs `x` and `y` as symbolic variables `X` and `Y`.
- Path 1: 
	The condition `x > y` is true, that means `X > Y` is true. The path condition becomes `X > Y` and the result of the function is `X-Y`
- Path 2:
	The condition `x > y` is false. The path condition for that path becomes `X <= Y` and the result of the function is `Y - X`

The SMT solver can be used to check if there is an input that would lead to specific paths, for instance, 
- "Is it possible that `X > Y` ?" 
- "Is there a case where both paths could be followed for the same input?"
The solver would validate or invalidate such constraints.

## Usage
Symbolic execution can analyze **all possible execution paths** in a program, ensuring that all potential behaviours are considered. This is very useful for finding edge cases or tricky bugs.
It can also automatically find inputs that lead to errors, crashed or violations of program specifications (null pointer dereferences, buffer overflows, ...)

## Limitations
#### Path explosion problem
For programs with mayn branches or loops, the number of execution paths can grow exponentially, making it computably hard to explore all paths.
Of course there are some heuristics that can tackle this issue but can only help so much.