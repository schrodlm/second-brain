source: https://www.researchgate.net/publication/220689159_Model_Checking
It is an effective technique for comparing a **system description against its formal specification**, by essentially creating a model of system.

It is integrated in the **hardware design** process, and in development of compilcated protocols and **software**.

It is a very intratable problem that is the ground for very active research.

It can be seen as a more exhaustive validation attempt than testing, and being automatic, as a more practical method than theorem proving.

It is important to keep in mind, that an assurance of correctness is gained when errros are not found by model checking, this does not exclude the existence of errors. Model checking can miss inconsistencies between the checked model and the specification, or report *false positives*
Errors reported by the model checker thus need to be further checked against the actual implementation.

## Limitations
Model checking has some strict limitations. As only a ***model*** is being verified rather than the system itself. Discrepancies betwen the two mayaffect verification result. Similarly, the properties against which the system is to be checked, written in some mathematical formalis (logic, automata), may not precisely fit the intention of less formal requirements, given in natural language.

It is an NP-hard problem, altought there are many cases of applying model checking succesfully, there are also many difficult instances where one or more of the existing methods fails to work efficiently.

## Techniques
Several techniques for model checking exist. They try to increase the size of system that can be verified given the available memory and reasonable execution time. 

[[Explicit state space methods]]
- they examine the reachable states using search techniques, the search space represents both the states of the model and the checked property.
[[Symbolic model checking]]
- uses an efficient data structure called [[BDD]] to store sets of states, and progresses from one set of states to another rather than state by state.
[[bounded model checking]]
- encodes a counterexamples as a SAT formula and uses the power of modern SAT solvers.
- thus approach conquers new ground by using capabilities of SAT solvers enriched with decidable theories (SMT) in order to verify system with an infinite state space


## Modelling
In order to validate a sytem using model checking tools, the system has first to be modelel into the internal representation of that tool.
This can be done either:
- manually
- automatically (by a compiler)

In many cases, the internal representation used by the tool is different from the original description of the system.
Reason for that is that internal formalisms of tools often reflect some contraints such as dealing with finite states, and is also related to optimizations available by such tools.

### Repesenting finite state systems
There are many ways to represent finite state systems. The differences are
being manifested in the kind of observations that are made about the possible executions and the way the executions are related to one another.

**The modeling also affects the complexity of the verification**; it is tempting to use a modeling formalism that is very expressive, however, there is a clear tradeoff between expressiveness and complexity.

In order to model systems, we work with [[first-order logic | first-order languages]]![[modelling_system_example.pdf]]
this execution model in example is called the ***interleaving model*** and can be used to represent sequential as well as [[concurrency | concurrent]] executions.
For an intuitive explanation of the interleaving view, assume that the order of occurrences of transitions represent the moment when their effect is taking place.

Another way to represent the model could be with [[LTL (linear temporal logic)]] 
#### State graph from transition system
Given a transition system, its **state graph** can be defined, which is a graph of states reachable from any of its initial state.
Each directed edge can be annotated by the transition that is executed to transform its incoming state into its outgoing state.
Generating the state graph from the transition system can be done with a
search method, e.g., Depth First Search (DFS) or Breadth First Search (BFS),
starting at initial states and moving from one the to another by applying the
enabled transitions. The state graph can be used already to check for simple
properties. For example, one can check for deadlocks (states where no transition
is enabled and that are not intended to be terminating), whether some bad states
are reachable, or for dead code (code that is never executed).

### Atomicity
An important modeling decision is on the level of atomicity of the transi-
tions. According to the interleaving model, at each state, an enabled transition is selected for execution and is performed entirely (atomically), without being able to observe intermediate changes. If the level of atomicity is too fine, we may needlessly increase the size of the state space and the memory required for performing the verification. If the atomicity is too coarse, there may be observable state changes that are not captured by the transition system, including additional interleaving that may be missed. Again, it is the **job of the person performing the modeling to make the right choice**.

#### Example
Two processors want both to increment a shared variable `x` by 1.
Modeling this increment as a single atomic transition may reflect the behavior of the actual system if, e.g., the variable `x` is implemented as a register (this is possible, e.g., in the C language). On the other hand, it is also possible that `x` stored in some physical memory location is being first copied into an internal register (in each [[process]], separately), which is incremented before the new value is being copied back to the memory location that holds `x`. In this case, if the initial value is 0, both processes will read the value 0, store it, increment it, and
store 1 back to `x`; a loss of one increment.

## [[system specification| Specification]]
Very important part of creating a model of a system is to have that system's specification.
