OntoUML is a language for Ontology-driven [[conceptual modelling]]. It is built as a [UML] extension based on the [[UFO]].

It integrates formal ontology principles into UML to create more semantically precise and semantically rich models. 

## OntoUML vs [[UML]]
| Aspect               | UML                                           | OntoUML                                                     |
| -------------------- | --------------------------------------------- | ----------------------------------------------------------- |
| **Purpose**          | General-purpose software and system modeling  | Ontology-driven conceptual modeling with semantic precision |
| **Foundation**       | Primarily based on software engineering needs | Rooted in formal ontology and philosophical concepts        |
| **Stereotypes**      | Limited to standard UML stereotypes           | Introduces ontological stereotypes like Kind, Role, etc.    |
| **Semantic Depth**   | Focuses on structural and behavioral aspects  | Emphasizes ontological distinctions and semantic clarity    |
| **Type Hierarchies** | Supports generalization/specialization        | Distinguishes between rigid and anti-rigid categories       |
**Example**
![[Pasted image 20241009113118.png]]

## Classes and atributtes
- Classes in OntoUML are based on the UML concept of classes, which describe the shared properties of certain entities, referred to as class instances.
- Class instances contain values of variables defined by their class, in accordance with the attribute's characteristics, such as type and multiplicity.
- Attributes represent (more or less intrinsic) properties shared by the instances of a class.
![[Pasted image 20241009132152.png|500]]

## Instances
Instances of classes have specific values of attributtes. It is called [[instance-level modelling]]
They are used for validation, simulation and prototyping.
![[Pasted image 20241009132328.png|300]]

## Relation between instances and classes

In OntoUML, there can be more complex relationships between classes and instances (unlike in [[UML]] strict 1:1). For example, an instance might belong to multiple classes simultaneously, or the classification might change over time.
```
Class 1: Person
Attributes: name, age

Class 2: Employee
Attributes: job title, salary

Instance: [name: "Alice", age: 30, job title: "Engineer", salary: 60,000]
```

## Class attributes

## [[OntoUML rigidity ||Rigidity]]


