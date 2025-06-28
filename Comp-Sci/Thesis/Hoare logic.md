source: https://www.cs.cmu.edu/~aldrich/courses/654-sp09/notes/3-hoare-notes.pdf

It is a formal system with a set of logical rules to for **reasoning rigorously about the correctness** of a computer programs.

# Hoare triple
The central feauture of Hoare logic is the Hoare triple. A triple describes how the execution of a piece of code changes the state of the computation. 

It looks like this:
$$ \{P\}C\{Q\} $$
where $P$ is a [[logical contracts#Preconditions|precondition]] and $Q$ is a [[logical contracts#Postconditions|postcondition]]. $C$ is the program relating $P$ to $Q$.

It means that when precondition $P$ is met C is executed, it will establish the postcondition.

### Partial and total correctness
Using standard Hoare logic, only [[partial correctness]] can be proven. [[total correctness |Total correctness]] additionally requires termination, which can be proven separately or with an extended version of the While rule.

The implementation of a function is **partially correct** with respect to its specification if, assuming the **precondition is true** just before the function executes, then if the function terminates, the postcondition is true. The implementation is totally correct if, again assuming the precondition is true before function executes, the function is **guaranteed to terminate** and when it does, the **postcondition is true**. Thus **total correctness** is partial correctness + termination.

Note that if the function is called without its preconditions fullfilled, the function can behave in any way at all and still be correct.

## [[strongest postcondition|Strongest postcondition]] and [[weakest precondition]]

Consider the Hoare triple:$$ \{x = 5\} x:= x \cdot 2 \{x >0\} $$
This triple is clearly correct, because if $x=5$ and we multiply $x$ by $2$ we get $x = 10$ which clearly implies that $x>0$. However, even thought it is correct, this Hoare triple is not as precise as we might like. Specifically, we could write a **stronger postcondition**. One that implies $x > 0$. For example $$ (x > 5)  \land (x < 20) $$
is stronger, because it is more informative;it pins down the value of $x$ more precisely than $x > 0$. The strongest postcondition possible is $x = 10$; this is the most useful postcondition.

We can reason in the opposite direction as well, definining the weakest precondition. Meaning a one that allows for the most inputs. 

## Verifying loops

How to verify partial correctness of loops of the form `while b do S`, we come up with an [[logical contracts#Loop invariants|invariants]] $I$ such that the following conditions hold:
1. $P\implies I$ - this invariant must initially be true
2. $\{Inv \land B\} S \{Inv\}$ - each execution of the loop preserver the invariant
3. $(Inv \land \lnot{B}) \implies Q$ - the invariant and the loop exit condition imply the postcondition

We can verify [[full correctness]] by coming up with an integer-valued variant function $v$ that fulfils the following conditions:
1. $Inv \land B \implies v > 0$ - if we are entering the loop body (loops condition B == true) and the invariant holds, then $v$ must be strictily positive
2. $\{Inv \land B \land v = V\} S \{v < V\}$ - the value of the variant function decreases each time the loop body executes

This basically implies that the loop always **terminates**, thus if we prove **partial correctness** **and** we prove **termination**, we proved **full correctness**.
