# [[logical contracts |Logical contracts]] on data structures
So far we were focused on logical contracts of *control structures*: How do functions, assignments and loops give rise to the verification conditions?

But we will focus on reasoning about data structures. We will explore an example with two elementary data structures (**lists** and **queues**) and verify implementation of queues using two lists.

A key concept we need to capture is that of a **data structure invariant**.
- With executable contracts, such invariants are checked by functions.
- With logical contracts they are expressed as logical properties of the data structures.

We can classify data structures as:
- **persistent** (*immutable*)
- **ephemeral** (*mutable*)
Persistent data structures are prevalent in [[functional programming]], while ephemeral data structures are more common in [[imperative programming]].

## Nonexecutable specification

The specification we used in our verification of the mystery function was executable:
```
let rec function fib ( n : int ) : int =
requires { n >= 0 }
variant { n }
if n = 0 then 0
else if n = 1 then 1
else fib (n -2) + fib (n -1)
```
We draw your attention here to three keywords: let rec means that we are defining and executable, recursive function fib. The additional keyword function means that we can use fib in contracts to reason about code. This requires the `fib` function to be **pure** (have no effects, just return a value) and **terminating**. Purity is established simply by
traversing the code, while termination comes from proving the verification condition for variant `{ n }`.
In practice it is mostly the case that our specifications are not **executable but purely logical formulas**. That’s because they are intended to express what the function accomplishes, but abstract away from how. As a example, we can express the defining property of the function `fib` rather than giving its explicit definition.
We start with declaring fib to be a function from integers to integers and then describe three properties as axioms.
```
function fib ( n : int ) : int
axiom fib0 : fib 0 = 0
axiom fib1 : fib 1 = 1
axiom fib2 : forall n : int . fib ( n +2) = fib ( n +1) + fib n
```
## Invariant
In general, it's a property of the program state that is always true. A function or method that ensures that the invariant holds is said to maintain the invariant.