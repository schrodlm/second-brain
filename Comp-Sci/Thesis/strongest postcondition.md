source: https://www.cs.cmu.edu/~aldrich/courses/654-sp09/notes/3-hoare-notes.pdf

The **strongest postcondition** refers to the most precise and detailed condition that will hold **after** the execution of a program (or statement), given an initial state ([[logical contracts#Preconditions|precondition]]).

It describes exactly what is true after a program's execution, capturing all the effects of the program in its execution path.

It is the opposite of [[weakest precondition]].

It's particularly useful in tools that perform [[symbolic execution]], where the goal is to track exactly what happens to variables and states during the [[execution path]]. It is used in [[model checking]].

both [[weakest precondition]] and strongest postcondition are closely relates to **[[Hoare's triple]]**

## Formally
The strongest postcondition in Hoare's notation can be defined as $sp(P,C)$ in two parts:
$$
\begin{aligned}
    1. \ & \{ P \} \, C \, \{ sp(P, C) \} \\
    2. \ & \text{If } \{ P \} \, C \, \{ R \}, \text{ then } sp(P, C) \implies R
\end{aligned}
$$
First point means that strongest postcondition of given precondition and program is even a postcondition of these two.
Second point says that **strongest postcondition implies all other postconditions** (it is the most informative). 
We can clearly see that strongest postcondition **relies both on precondition and the program itself**.


## Example
Consider a simple program:
```c
x = x + 1
```
Let's start with the initial precondition:
`Precondition: x = 4`

### Step 1: What is the Strongest Postcondition?

After the statement `x = x + 1` executes, the strongest postcondition describes what is guaranteed to be true about `x`. Since the statement increments `x` by 1, we can deduce:
`Strongest Postcondition: x = 5`
This is the most precise statement about the state of `x` after the statement has been executed. It gives exact information about the final state.
