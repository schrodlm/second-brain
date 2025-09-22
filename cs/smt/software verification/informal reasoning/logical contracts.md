source: https://www.cs.cmu.edu/~15414/s23/s22/lectures/02-contracts.pdf
For [[imperative programming | imperative programs]] there is a line of research on program logics, that is, logics specifically designed to reason about the correctness of programs.

A program logic must allow us to express the programs we are reasoning about as well as the specification they are supposed to satisfy.

A **proof** in a program logic then is evidence that the program matches its specification.

To even be able to automatically prove that programs satisfy their specification we need to be able to break the problem down into smaller units that whole program - this is the role of **logical contracts**.

Logical contract specify under which circumstances a function may be called (**the precondition**) and what it guarantees for its result (**the postcondition**).

The intuition is that the correctness proof for the rest of the program may only rely on the pre- and post-condition of a function and not **its definition**.

### Variant
Additionally, these logical contracts allow us to express why functions or loops terminate (**the variant**) and which properties are preserved in a loop or data structure (**the invariant**). All of these are critical in making verification possible.

The other critical component is the theorem prover in the background that eventually verifies that the program obeys its contracts.

Let's examine a C mystery functions:
```c
int f(int n)
{
  int i = 0;
  int a = 0;
  int b = 1;

  while(i < n) {
    b = a + b;
    a = b - a;
    i = i + 1;
  }
  return a;
}

```
After a while you can see that this function `f(n)` computes the `n`th Fibonnaci number. The key insight into the correctness of the function will be the **loop invariant**.

Let's look at the **executable contracts** of this function and see how we can translate them into **logical contracts**

## Preconditions
A preconditions for a function imposes a requirement upon any caller, namely that the precondition should be true. For executable contracts, this means that the precondition is a [[pure function]] and evaluates to true.
**For logical contracts it will mean the the condition is true**. In this case, the precondition is the `n >= 0`.
```c
int f(int n)
//@requires n>= 0
{...}
```

## Postconditions
A postcondition for a function expresses what the caller may assume about its result (and, later, about its effect). It is important that the caller cannot "look inside" the function to reason about its behaviour, but must rely only on the postcondition.
This is an important principle allowing us to localize the reasoning in individual functions. In essence, functions represent an abstraction boundary that greatly aids the possibility of [[software verification | program verification]].

In our example the postcondition states that `f` computes the Fibonacci function, but how can we actually say this?

In C0, there is no resource except to define a simple (if highly inefficient) function which we view as the specification. This function must be pure, meaning it can not have any externally observable effects. This is important because a program with executable contracts should behave the same whether contracts are actually checked or not.

```c
int fib(int n)
// @requires n>=0
{
	if (n == 0) return 0;
	else if(n == 1) return 1;
	else /* n >= 2 */ return fib(n-2) + fib(n-1);
}

int f(int n)
//@requires n >= 0
//@ensures \result == fib(n);
{...}
```

The postcondition is always placed in the preamble of a function. That is so that a caller can see what it may assume about the value that is returned. But it is actually checked at every return statement inside the function.

## Loop invariants
In simple words, a loop invariant is some predicate (condition) that holds for every iteration of the loop. For example, let's look at a simple `for` loop that looks like this:

```c
int j = 9;
for(int i=0; i<10; i++)  
  j--;
```

In this example it is true (for every iteration) that `i + j == 9`. A weaker invariant that is also true is that `i >= 0 && i <= 10`.

But it can be so much more, it can present the goal of the loop for example:
For insertion sort, supposing the loop is iterating with `i`, at the end of each loop, the array is ordered until the `i`-th element.

Determining suitable loop invariant is the verification task requiring the most creativity. Here are the critical properties of loop invariants, when we consider them merely executable contracts to be checked dynamically, as the program runs.
**Location** 
	The loop invariant is always checked just before the guard condition. This is to ensure we can rely on the loop invariant in case the loop guard is false. 
	The invariant is always checked with respect to the current values of all variables appearing in them.
**Initialization**
	Just before the loop is entered the first time, the loop invariant must be
	true.
**Preservation**
	When we jump back to the beginning of the loop, the loop invariant must be true.

```c
int f(int n)
//@requires n >= 0;
//@ensures  \result == fib(n);
{
	int i = 0;
	int a = 0;
	int b = 1;
	while(i < n) 
	//@loop_invariant 0 <= i && i <=n
	//@loop_invariant a == fib(i) && b == fib(i+1);
	{
		b = a + b;
		a = b - a;
		i = i + 1;
	}
	...
}
```

Logically we conclude the following facts upon loop exit:
- `O <= i` and `i <= n` (loop invriant at line 9)
- `a == fib(i)` and `b == fib(i+1)` (loop invariant at line 10)
- `i >= n` (loop guard at line 8 is false)

## Assertions
From the information we have when exiting the loop, we can see that `i == n` must be true (because `i <= n` and `i >= n`). In the absence of formal proof, we may not be fully confident of that fast, so we can insert an assertion that is checked dynamically and would raise an exception if `i != n`.
Logically it is also often helpful to state what we know after the loop in a form of an assertion. Assertion must be true and can therefore be assumed subsequently. While it is theoretically redundant, it may be an important lemma for the theorem proved and can make a difference between success and failure.
```c
int f(int n)
//@requires n >= 0;
//@ensures  \result == fib(n);
{
	int i = 0;
	int a = 0;
	int b = 1;
	while(i < n) 
	//@loop_invariant 0 <= i && i <=n
	//@loop_invariant a == fib(i) && b == fib(i+1);
	{
		b = a + b;
		a = b - a;
		i = i + 1;
	}
	//@assert i == n
	return a;
}
```
This dynamic checking of the executable contracts is supported by [C0](https://c0.cs.cmu.edu/docs/c0-reference.pdf), a test language developed in CMU.
If no exception was raised during the executiong, that would mean that the executable contracts always evaluated to true. 
Unfortunately when we move to logical contracts we lose the option of *testing the contracts* bacause they can no longer be executed. 

## From executable to logical contracts
In the preceding section we have been writing executable contracts but explained their meaning in terms of logical contracts.
In this section we will translate from [C0](https://c0.cs.cmu.edu/docs/c0-reference.pdf) to [WhyML](https://www.why3.org/), which is the language used in the Why3 tool chain.
Here the original C0 and the WhyML code are presented side by side and then differences are explained.

```c
int fib(int n)
//@require n >= 0;
{
	if (n==0) return 0;
	else if (n==1) return 1;
	else /* n >= 2 */
		return fib(n-2) + fib(n-1);
}
int f(int n)
//@requires n >= 0;
//@ensures  \result == fib(n);
{
	int i = 0;
	int a = 0;
	int b = 1;
	while(i < n) 
	//@loop_invariant 0 <= i && i <=n
	//@loop_invariant a == fib(i) && b == fib(i+1);
	{
		b = a + b;
		a = b - a;
		i = i + 1;
	}
	//@assert i == n
	return a;
}
```

```whyml
let rec function fib (n: int) : int = 
requires { n > = 0}
variant { n }
if n = 0 then 0
else if n = 1 then 1
else fib(n-2) + fib(n-1)

let f (n:int) : int = 
requires { n  > = 0 }
ensures { result = fib n }

let ref i = 0 in
let ref a = 0 in
let ref b = 1 in
while i  < n do 
	invariant { 0 <= i /\ i <= n }
	invariant { a = fib i /\ b = fib (i+1) }
	variant { n-1 }
	b <- a + b;
	a <- b - a;
	i <- i + 1;
done;
assert { i = n };
a
```
At the top we see the pure function `fib` becomes the function `fib` which is marked as pure with the `function` keyword. This means `fib` can be used in computation as well as in logical contracts. 
The `variant` annotation provides the measure that is decreasing in recursive calls, thereby guaranteeing that the function terminates. This is neccesary for pure functions that can be used in contracts.

The translation of the *requires* and *ensures* clauses in the definition of `f` is pretty straightforward. A definition such as `int i = 0;` is translated to binding `let ref i = 0 in`. This pattern makes `i` assignable in its scope, using the notation `i <- ...`. Formally, `i` will have type `ref int` but uses of the dereference opeator `!` remain implicit to make the code more visually compact.
The while loop and invariants translate also in a straightforward manner, but `&&` is replaced by `/\`. New on the side of WhyML is a variant declaration for loop. It contains a quantity that serves as a termination measure for the loop. If we give an integer quantity, it should be nonnegative and strictly decreasing during each loop iteration.

In the CLI we can now call:
```bash
why3 prove -P alt-ergo fib.mlw
mystery.mlw Mystery f’vc: Valid (0.01s, 17 steps)

```

So how does this work inside Why3 is that we provided things that the program can assume, like assigning variables, or using precondition, and using this knowledge it has to prove that:
1. **loop invariant holds initially**
2. **loop invariants are preserved**
3. **loop variant holds** (termination of the loop)
4. **loop invariants and negated loop guard imply postcondition**
```
let f ( n : int ) : int =
requires { n >= 0 }              (* assume : n >= 0 [ H0 ] *)
ensures { result = fib n }       (* skip for now ... *)
let ref i = 0 in                 (* assume : i = 0 [ H1 ] *)
let ref a = 0 in                 (* assume : a = 0 [ H2 ] *)
let ref b = 1 in                 (* assume : b = 1 [ H3 ] *)
while i < n do                   (* prove : [ H0 -3] -> 0 <= i /\ i <= n *)
invariant { 0 <= i /\ i <= n }
invariant { a = fib i            (* prove : [ H0 -3] -> a = fib i *)
                                 /\ b = fib ( i +1) } (* /\ b = fib ( i +1) *)
variant { n - i }
b <- a + b ;
a <- b - a ;
i <- i + 1
done ;
```
This is a showcase of the first proof. That loop invariants This is explained with more nuance in the source material.

