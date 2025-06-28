In [[OntoUML]], **rigidity** describes whether an entity, once classified under a particular class, must always be an instance of that class in all **possible worlds** (scenarios or contexts). Rigidity defines the **necessity** or **contingency** of an entity's classification across time and different situations. It is closely tied to [[modal logic]] by it's definition.

### Modal Logic Background

In **modal logic**, we use two key modal operators:

- **Necessity** (`□`): A statement is necessarily true, meaning it holds in all possible worlds.
- **Possibility** (`◇`): A statement is possibly true, meaning it holds in at least one possible world.

We can apply these operators to statements about class membership.

### Types of Rigidity in OntoUML 

#### **Rigid Classes (Necessarily True in All Worlds)**:
    
- A class is **rigid** if its instances must always be classified as members of that class across all possible worlds. Once something is an instance of a rigid class, it cannot stop being classified as such in any world.
- **In modal logic terms**: For every instance `x` of a rigid class `C`, the statement "x is an instance of C" is **necessarily true** (`□`), meaning it holds in all possible worlds.

**Example**:

- **Class**: `Person`
- **Instance**: `John`
- If John is classified as a `Person`, he must remain a `Person` in all possible worlds. In[[modal logic| modal]] terms: 
	
	 □John is a Person
	
- This means that no matter what possible world you look at, John is always a `Person`. He can't be anything other than a `Person` because it's an essential, rigid classification.
    
#### Anti-Rigid Classes (Possibly True in Some Worlds)**:
    
- A class is **anti-rigid** if its instances can cease to be classified as members of that class in some possible worlds. In other words, an entity can belong to this class in some contexts but not others, meaning the classification is **contingent** or temporary.
- **In modal logic terms**: For an instance `x` of an anti-rigid class `C`, the statement "x is an instance of C" is **possibly true** (`◇`), meaning it holds in some possible worlds but not in others.

**Example**:

- **Class**: `Student`
- **Instance**: `John`
- John can be classified as a `Student` in some worlds (while enrolled at a university) but may not be a `Student` in other worlds (after graduation). In modal terms: 
	
	 ◇(John is a Student)
	 
- This means there are some possible worlds where John is a student, but there are also worlds where John is not a student (e.g., after he graduates). The classification is **contingent** on the world or scenario.