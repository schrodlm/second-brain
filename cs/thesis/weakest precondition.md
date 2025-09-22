source: https://www.cs.cmu.edu/~aldrich/courses/654-sp09/notes/3-hoare-notes.pdf


The **weakest precondition** (WP) is a concept in **[[formal verification]]** and **program correctness**. It a special type of a [[logical contracts#Preconditions|precondition]]

It refers to the least restrictive condition that must hold before the execution of a program (or part of it) to ensure that a specific[[logical contracts#Postconditions | postcondition]] will hold after the program's execution. 

In simpler terms, the weakest precondition **is the minimal condition required to guarantee a desired outcome**.

both [[weakest precondition]] and strongest postcondition are closely related to **[[hoare logic]]**, they can be seens as methods to reason about or calculate parts of a Hoares Triple.

---
## Formally
The strongest postcondition in Hoare's notation can be defined as $sp(P,C)$ in two parts:
$$
\begin{aligned}
    1. \ & \{ wp(C,Q) \} \, C \, \{ Q \} \\
    2. \ & \text{If } \{ R \} \, C \, \{ Q \}, \text{ then } R \implies wp(C, Q) 
\end{aligned}
$$
First point means that weakest precondition of given postcondition and program is even precondition of these two.
Second point says that **all other preconditions implies this weakest precondition** (it is the least restrictive and allows for the most inputs). 
We can clearly see that weakest precondition **relies both on postcondition and the program itself**.


## Example
Consider the following simple program:
```c
x = x + 1;
```
You want to ensure that after this statement executes, the postcondition is:
```
Postcondition: x > 5
```
### Step 1: What is the Weakest Precondition?

To determine the weakest precondition, you need to reason backward from the postcondition to figure out what must be true about `x` **before** executing `x = x + 1` in order to ensure that `x > 5` after the execution.

- After the statement `x = x + 1`, we want `x > 5`.
- Before the statement `x = x + 1` is executed, we can deduce that `x` must be greater than `4` (since `x + 1` will be greater than 5 if `x` is greater than 4).

So, the **weakest precondition** in this case is:
```
WP(x = x + 1, x > 5): x > 4
```
This means that, for the postcondition `x > 5` to hold after `x = x + 1` is executed, the weakest precondition (or minimal requirement) before executing that statement is `x > 4`.