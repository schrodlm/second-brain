Process of ensuring that a **program behaves as expected according to its specification**
This also includes checking that software does not have bugs, memory issues or **security vulnerabilities**.
Goal is to **mathematically** prove that the program will always behave correctly for all possible inputs.

How do we know if a program is correct? We can use multiple techniques but all have their disadvantages.
1. testing 
	- probably incomplete -> uncertain answer
	- most of the time it can not be exhaustive (test all possible options)
2. code review
	- humans are fallible, bugs are subtle
	- they have to understand the specification

Much better is that we **prove correctness**
$\text{Specification} \iff \text{Implementation}$

This approach has it own problems:
- specification must be really precise (many subtleties)
- meaning of code must be well-defined
- reasoning must be sound

## Different traditions and techniques in programming languages

1. Functional programmming - **dependent types**
	- proofs are expressed in programs (Agda)
	- proof tactics are expressed as programs (Coq)
2. Imperative programming - **[[logical contracts]]**
	- properties are expressed in contracts
	- reduce correctness to logical propositions (verification condition)
	- use **automated theorem provers** to prove VC (SMT solvers)

What can automatic methods do for us?
- fill in low-level details
- give diagnostic info
They cannot:
- **verify everything** for us
- generate specification
- tell us how to fix bugs

# Role of [[smt]] in software verification
SMT solvers are used as part of the **automated reasoning** required in software verification.

They help to answer question like: 
- "Does there exist an input that can cause this program to crash?" 
- "Is this loop invariant always true?"

It does that by transforming these question into [[logical formulas]]

## Process 
#### 1. Abstraction or Symbolic execution
Software code is abstracted into logical formulas. This may involve using techniques like [[symbolic execution]], where **program inputs are treated as symbolic variables rather then concrete values**

Keep in mind that symbolic execution is only one of the techniques used in this broad term, there are other techniques like:
- [[model checking]]
- [[static analysis]]
- [[testing]]

#### 2. Translation to SMT formulas
The abstracted logic (often in [[first-order logic]]) is exressed in the [[stm-lib]] format, and theories (such as integer arithetic, array, or bit-vectors) are defined based on the properties of the program being verified

#### 3. Checking satisfiability
The SMT solver checks whether the [[logical formulas]] derived from the program are[[logical formulas#satisfiability | satisfiable]]. If they are, it indicated that a bug or a violation of the specification might exist. If the formulas are [[logical formulas#unsatisfiablity | unsatisfiable]], it indicated that program is correct for that specific path.

## Example

Imagine you are verifying a simple program that checks whether an integer is positive:
```c
int foo(int x) {
	if(x > 0) {
		return 1;
	}
	else 
		return -1
}

```
To verify that this function behaves correctly, you might want to ensure it never causes a [[runtime error]]. Let's use an [[SMT solver]] to check if any inputs might lead to an error (e.g., `x > 0` failing when it should pass).
######  1.Translate to logic
The condition `x > 0` can be expressed as a formula in [[first-order logic]]. In SMT-LIB, it could be encoded like this:
```smt-lib
	(declare-const x Int)
	(assert (> x 0))
```
###### 2. Run the SMT solver 
The solver will try to determine whether there exists a value for `x` such that `x > 0` is **false**.

###### 3. Satisfiability check
If the solver find that `x <= 0` is satisfiable (it will), it indicated that there are valid inputs where the function does not return `1` (in this case it would be every negative number). This is correct behaviour of the program, but if we were checking for bugs, the SMT solver could help us verify that the logic holds in all cases.

## Examples of software verification verification tools
Tools like [[CMBC]], [[KLLEE]], or [[Rotor]] server as the front end. These tools translate program's behaviour into logic that the SMT solver understands.

These formulas are then passed to SMT solver (e.g., [[Z3]]), which checks the satisfiability and return a result. 

In summary, SMT solvers play the role of the "proof engine" in software verification.

