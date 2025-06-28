System specification can be seen as a contract between the consumer and the system developer.
Natural langauge is commonly used to describe the requirements from the system, but it is very susceptible to ambiguity. The use of **formal specification** allows a unique interpretation, as well as developing model checking algorithms. As in modeling, the use of different notations (natural language and specification formalism) may cause a potential discrepancy.

Although **[[Comp-Sci/SMT/software verification/model checking/model checking]]** has been around since the 1980s, there is still debate about which **specification formalism** to use because of a key tradeoff:

- **More expressive formalisms** can describe a wider range of behaviors but make verification **more computationally difficult**.
- **Simpler formalisms** are easier to check but may not be able to express everything you want to verify about the system. 
This ongoing debate is a core challenge in the development of model checking techniques.