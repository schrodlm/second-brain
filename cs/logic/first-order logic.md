**First-order logic (FOL)** is a formal system used in mathematics, computer science, linguistics, and philosophy to describe relationships between objects, properties of objects, and quantification over individual objects. It extends **[[propositional logic]]** by allowing the use of variables, quantifiers, predicates, and functions. A first-order language is a language created using first-order logic. Here's a breakdown of its key components and characteristics:

#### Key Elements of First-Order Logic:

1. **Variables**: These represent individual elements in the domain of discourse (e.g., $x$, $y$, $z$).
    
    - Example: $x$ might represent a person or a number.
2. **Constants**: Specific objects in the domain of discourse.
    
    - Example: $c$ could represent a specific person like "John" or a number like "2".
3. **Predicates (or Relations)**: Functions that return a truth value (True or False) based on the arguments they take. Predicates represent properties of objects or relationships between them.
    
    - Example: $P(x)$ could mean "x is a student," or $R(x, y)$ could mean "x is the parent of y."
4. **Quantifiers**: First-order logic allows quantification over individual elements in the domain of discourse, but not over sets or functions.
    
    - **Universal quantifier** ($\forall$): "For all" — indicates that something holds for every element in the domain.
        - Example: $\forall x , P(x)$ means "for all $x$, $P(x)$ is true."
    - **Existential quantifier** ($\exists$): "There exists" — indicates that there is at least one element in the domain for which a property holds.
        - Example: $\exists x , P(x)$ means "there exists an $x$ such that $P(x)$ is true."
5. **Logical Connectives**: These combine formulas in logical ways.
    
    - **Negation** ($\neg$): "Not."
    - **Conjunction** ($\land$): "And."
    - **Disjunction** ($\lor$): "Or."
    - **Implication** ($\rightarrow$): "If... then."
    - **Biconditional** ($\leftrightarrow$): "If and only if."
6. **Functions**: Functions take one or more arguments and return a single object in the domain.
    
    - Example: $f(x)$ could represent a function that gives the father of $x$.

---

#### Example of a First-Order Logic Formula

Let’s look at an example in a domain where we're talking about people and their relationships:

- $P(x)$: "x is a person."
- $F(x)$: "x is female."
- $M(x)$: "x is male."
- $Parent(x, y)$: "x is the parent of y."

A first-order logic statement could be something like:

$\forall x , (F(x) \rightarrow P(x))$

This reads as: "For all $x$, if $x$ is female, then $x$ is a person." In other words, every female is a person.

Another example:

$\exists x , \exists y , (Parent(x, y) \land M(x))$

This means: "There exists some $x$ and some $y$ such that $x$ is the parent of $y$ and $x$ is male." In simpler terms, there is at least one father.

---

#### How FOL Differs from Propositional Logic:

- **Propositional logic** only deals with true/false propositions and logical connectives. It doesn't allow variables or quantification.
    - Example in propositional logic: $p \land q$, where $p$ and $q$ are statements.
- **First-order logic** allows statements about individuals in a domain and expresses relationships between these individuals using predicates and quantifiers.
    - Example: $\forall x , (P(x) \rightarrow Q(x))$, where $P(x)$ and $Q(x)$ are predicates that involve variables.

---

#### Applications of First-Order Logic:

- **Mathematics**: Defining properties of numbers, sets, and functions.
- **Computer Science**: Expressing conditions in databases, formal verification of software, and artificial intelligence.
- **Linguistics**: Formalizing the meaning of sentences.
- **Philosophy**: Describing logical structures in arguments.

---

### Summary:

First-order logic is a powerful formal system that allows reasoning about objects, their properties, and the relationships between them. It is expressive enough to describe many systems of interest in mathematics and computer science but retains limitations on the types of things it can quantify over (individual elements, not sets or functions).