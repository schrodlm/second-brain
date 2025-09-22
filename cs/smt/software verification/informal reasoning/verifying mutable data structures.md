source: https://www.cs.cmu.edu/~15414/s23/s22/lectures/04-ghosts.pdf

How do we specify and verify simple loops that operate on arrays? 

The key construct that we have ([[logical contracts#Loop invariants |loop invariants]] and [[logical contracts#Variant|variant]]) are sufficient but become more complex (than with immutable data structures) because they have to express not only of what we **change** in array but also what does **not change**.

This additional requirement makes reasoning about mutable data structures in many cases more difficult than reasoning about [[verifying mutable data structures| mutable data structures]].

## Simple models of complex data structures
This is a very important technique. 

**Example**
We have a red/black tree implementation of a map. It is very complex and has a lot of internal [[verifying immutable data structures#Invariant |data structure invariants]]. 
### Internal invariants
These invariants are called internal invariants.
In red/black tree this would include:
- *ordering variant* 
	keys in left subtrees are all smaller and keys in right subtree are all larger than key in a node
- *color invariant*
	there are no two ajacent red nodes in the tree

and so on...
- data strucutre must maintain them but the client that uses this data structure does not care about internal implementation, he cares about **correct and efficient implementation**.

We need to find a simpler data structure that has the same intended behaviour. In this case it could be a **map**.

### Purpose of the model
The purpose of the model is to **reason** about data structure, but **not compute** with it. So we want to actually erase the code that maintains the model, because actually computing it would negate all the advantages of efficient implementation.

This is the primary purpose of [[ghosts]].

