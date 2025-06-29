---

layout: post

title: "Turing machines and whatnot"

date: 2024-12-20 20:31:01 +0100

categories: jekyll update

project: proj_2

---
# Turing Machine
Abstract computational models were first described as *a-machines* by Alan Turing in his paper "On Computable Numbers, With An Application To The Entscheidungsproblem" in 1936. They are considered one of the foundational models of computability.

Turing machine in its universal form encapsulates the fundamental principles of the stored-program all-purpose digital computer.

I will use a more modern definition of a Turing machine than what Turing described in his paper.

This machine has a **finite number of states and an infinite tape and infite number of time**, that is partitioned into cells into which you can write or read from. This machine is capable of following operations:

- `L` - move the tape head one square to the left.

- `R` - move the tape head one square to the right.

- `P_x` - print the symbol `x` onto the current tape square.

Depending on what is read a new symbol can be written into that cell and machine is able to move one cell to the left or one cell to the right, and transition into a different state. This process is called a state transition the execution of a "program" on such a machine can be described by a state transition table. Following table describes a Turing Machine that will compute the sequence `01010101...` .

| **State** | **Symbol** | **Operations** | **Next state** |
| --------- | ---------- | -------------- | -------------- |
| a         | None       | P0, R          | b              |
| b         | None       | P1, R          | a              |

**Table:** State transition table for the Turing machine, adapted and modernized

from Turing's 1936 paper.

## Deterministic and Non-Deterministic Turing Machines
A Turing machine is deterministic (**DTM**) if, for any given state and input symbol, there is exactly one defined transition. A non-deterministic Turing machine (**NTM**) allows multiple possible transitions for the same state and input symbol. Conceptually, such a machine can explore all possible transitions simultaneously.

While deterministic Turing machines serve as models for real-world computers with finite resources, non-deterministic machines are theoretical constructs and cannot be physically realized. They are, however, invaluable for studying computational complexity.
### Equality of DTMs and NTMs
Deterministic Turing machines (DTMs) and non-deterministic Turing machines (NTMs) are equivalent in terms of computational power: both can compute the same class of functions and solve the same decision problems. However, they differ significantly in how they operate and in their computational efficiency:
**Key Differences:**
- Non-Deterministic Turing Machines (NTMs): Conceptually explore multiple computational paths simultaneously, as if branching into parallel processes. This allows NTMs to solve certain problems more efficiently in theory.
- Deterministic Turing Machines (DTMs): Must simulate all possible computational paths sequentially. This simulation can introduce exponential time overhead.

The idea of their equivalence dates back to the foundations of computation, including Alan Turing's seminal work, but was formalized by Marvin Minsky in his book "Computation: Finite and Infinite Machines" (1967).