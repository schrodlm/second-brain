
It is a word-level model checking format for capturing models of hardware and **potentially software**.

It generalizes and extends BTOR format, which is also sort of a generalization of [[AIGER]].

In contrast to BTOR, which is tailored towards [[SMT#bit-vectors]] and one-dimensional [[SMT#bit-vector arrays]], BTOR2 has explicit [[SMT#sort declarations]].

It allows to explicitly initialize registers and memories (this was not possible in BTOR). We can have a look at how it works:
