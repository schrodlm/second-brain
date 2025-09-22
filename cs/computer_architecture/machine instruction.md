Instruction is a **single operation of a processing unit** defined in its [[isa|instruction set]].

## Practical use of the term instruction
In practical terms, when somebody mentions an "instruction" they will most likely be reffering to a specific command within a program that "tells" [[CPU]] what to do. As for example `ADD R1, R2` which consist of opcode and operands.

Instead of talking about this practical definition, I would like to explore instruction as it stands in the official definition: **the operation of a processing unit**, that means we can explore how an instruction like `ADD R1, R2` is actually executed by a CPU and what that process encompasses.

## Low level look
At its core a processor consist of millions of transistors arranged to form small functional unit. 
These units can perform really low level operations such as storing/sending information (latches, flip flops, ...) or adding, multiplying or even performing boolean algebra (logic gates, adders, ...).

So finishing an instruction can be viewed as a finishing operation of specific functional unit, that also implies it can be seen as a **state change inside a [[CPU]]**

What instruction can specific CPU execute is specified by its [[isa]]

## Processing instructions (instruction cycle)
Processing of the instruction is done by CPU in a process called instruction cycle (also known as fetch-decode-execute cycle)

This process is repeated from the boot-up until the computer shuts down and it is composed of three main stages: fetch stage, decode stage and execute stage.

Older or simpler CPUs perform instruction cycle sequentially and that makes sense because the code (instructions) is fundamentally sequential as well and instructions often depend on results of previously executed instructions, but in modern CPUs these cycles are executed concurrently and often in parallel. This is possible thanks to methods like [[branch prediction]], [[instruction pipelining]] and other advanced topics.


### Fetch-decode-execute implementation

**Warning**
Before I show a specific implementation of instruction cycle, it is important to mention that while the general flow of **fetch-decode-execute** applies to all processing units based on [[von Neumann architecture]], specific implementations can differ. For example stack-based ISAs instruction cycle operates differenty bacause instruction interact with stack rather than with registers.

Processing of the instruction is done by CPU in a process called **instruction cycle** (also known as **fetch-decode-execute cycle**)

This process is repeated from the boot-up until the computer shuts down and it is composed of three main stages: **fetch stage**, **decode stage** and **execute stage**.

Older or simpler CPUs perform instruction cycle sequentially and that makes sense because the code (instructions) is fundamentally sequential as well and instructions often depend on results of previously executed instructions, but in modern CPUs these cycles are executed concurrently and often in parallel. This is possible thanks to methods like branch prediction, instruction pipelining and other advanced topics.

Instruction cycle uses several specific-purpose registers:

**Program Counter (PC)** - register that hold memory address of next instruction to be executed

**Memory Address Register (MAR)** - holds the address of the data to either be written or fetched

**Memory Data Register (MDR)** - hold the data itself (that was fetched or will be written)

This already implies MAR and MDR work closely together.

**Current Instruction Register (CIR)** - holds the instruction itself (encoded and then decoded)

#### Fetch stage

Memory currently stored in the PC is copied into MAR (PC is then incremented to point to next instruction). CPU will then fetch instruction to which MAR is pointing to and stores it in MDR register. This instruction is then copied right into CIR register.

That is the whole fetch stage. I was first appaled by a very big number of copying between these registers, but since every register has a specific purpose and hardware correspond to that purpose it makes sense. For example, why isn’t instruction at address which PC is holding immediately fetch to CIR? This is due to the architecture and design of the CPU. From what I gathered it used to work like that in older (synchronous) CPUs, but in modern times we need to use every microsecond, you can latch data into MAR and let those lines float while CPU can work on something else, so MAR and MDR essentialy act as buffers.

#### Decode stage

Control unit will decode the instruction stored in the CIR using a binary decoder (implementations can vary), which is essentially a combinational circuit that uses logic gates and converts binary information to signals.

#### Execute stage

Control unit of the CPU will then send a signal to specific functional units that will execute operations of the instruction (reads from registers,mathematical operations, binary shifts,…). Result is then sent to main memory.

Also, in most processors, there can be interruptions. When an interrupt happens, the CPU jumps to an interrupt service routine, does what needs to be done, and then goes back to the main program.

# Coding of instructions
![[Pasted image 20240924210159.png]]![[Pasted image 20240924210229.png]]
![[Pasted image 20240924210252.png]]