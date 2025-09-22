A verification condition is a [[logical formula]] that expresses some aspect of the correctness of a system.

VC represents a neccesary properties of the program (such as assertions, [[logical contracts#Preconditions | preconditions]], [[logical contracts#Postconditions | postconditions]], or [[logical contracts#Loop invariants| invariants]]) that if proven true, guarantee the correctness of the program with respect to specified behaviour.

### How it Works:

1. **Program Annotations**: The program is often annotated with preconditions, postconditions, and invariants. These annotations describe the expected behavior before, during, and after executing parts of the program.
2. **Generation of Verification Conditions**: A static analysis tool (such as a verification tool) examines the code and generates a set of logical conditions (VCs) that must hold true for the program to meet its specification.
3. **Proving VCs**: The VCs are then handed to an automatic theorem prover (such as Z3 or another SMT solver). If all the VCs are proven true, the program is considered verified.

Alghorhitms to determine VC of a program exist. They use concept of [[weakest precondition]]. 