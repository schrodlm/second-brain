---

layout: post

title: "Instruction 101"

date: 2025-02-14 18:14:10 +0100

categories: jekyll update

---
## What is an instruction?
  
Instruction as defined in English dictionary is “an outline or manual of technical procedure”. In computer science its meaning is a little bit more specific. It is a **single operation of a processing unit** defined in its **instruction set**.

That can give us an interesting idea that every program ever written is just a collection of instructions. Thus meaning that if we take instruction as the most primitive programming language construct, every program will then fall into [Infinite monkey theorem](https://en.wikipedia.org/wiki/Infinite_monkey_theorem). This theorem states that a monkey hitting keys (instructions) at random on a keyboard for an infinite amount of time will almost surely produce any given text (program), such as the entire codebase of Windows OS. It is not really important, but it is certainly a really interesting theoretical concept.

## Practical use of the term “instruction”
In practical terms, when somebody mentions an “instruction” they will most likely refer to a specific command within a program that “tells” CPU what to do. As for example `ADD R1, R2` which consist of opcode and operands.

Instead of talking about this practical definition, I would like to explore instruction as it stands in the official definition: the operation of a processing unit, that means exploring how and instruction like `ADD R1, R2` is actually executed by a CPU and what that process encompasses.
## Low level look
At its core a processor consists of millions of transistors arranged to form small functional units.

These units can perform really low level operations such as storing/sending information (latches, flip-flops,…) or adding, multiplying or even performing boolean algebra (logic gates, adders, …)

So finishing an instruction can be viewed as a finishing operation of specific functional unit, that also implies it can also be seen as a state change inside a CPU.

What instructions can specific CPU execute is specified by its ISA (Instruction set architecture)
### ISA - Instruction set architecture
A instruction set is a list of all operations (instructions), with all their variations, that processor can execute.

I always thought that once the CPU is designed and the first prototypes are created, then and only then it is time to create the ISA for that specific CPU. That was a very wrong assumption, and I would say this a very common misconception among CS students.

ISA is an abstract model the defines supported instructions, data types, registers and all fundamental features that CPU needs to have and basically serves as a blueprint for manufacturers on what a CPU design should look like.

This means that two processors with very different processor design techniques (microarchitectures) can share a common ISA. For example, the Intel Pentium and the AMD Athlon implement nearly identical versions of the x86 instruction set, but they have radically different internal designs.

Selfie compiles into RISC-U (reduced RISC-V) machine code, that means instruction and their encodings should be supported by hardware designed to comply to RISC-V ISA.

### Processing instructions
Processing of the instruction is done by CPU in a process called instruction cycle (also known as fetch-decode-execute cycle)

This process is repeated from the boot-up until the computer shuts down and it is composed of three main stages: fetch stage, decode stage and execute stage.

Older or simpler CPUs perform instruction cycle sequentially and that makes sense because the code (instructions) is fundamentally sequential as well and instructions often depend on results of previously executed instructions, but in modern CPUs these cycles are executed concurrently and often in parallel. This is possible thanks to methods like branch prediction, instruction pipelining and other advanced topics.

Let's look at an example using a simplified CPU design based used in universities, keep in mind, in reality things are much more complex nowadays, and different microarchitectures can handle this process differently.

Instruction cycle uses several specific-purpose registers:

<ins>Program Counter (PC)</ins> - register that hold memory address of next instruction to be executed

<ins>Memory Address Register (MAR)</ins> - holds the address of the data to either be written or fetched

<ins>Memory Data Register (MDR)</ins> - hold the data itself (that was fetched or will be written)

This already implies MAR and MDR work closely together.

Current Instruction Register (CIR) - holds the instruction itself (encoded and then decoded)
### Fetch stage
Memory currently stored in the PC is copied into MAR (PC is then incremented to point to next instruction). CPU will then fetch instruction to which MAR is pointing to and stores it in MDR register. This instruction is then copied right into CIR register.

That is the whole fetch stage. I was first appaled by a very big number of copying between these registers, but since every register has a specific purpose and hardware correspond to that purpose it makes sense. For example, why isn’t instruction at address which PC is holding immediately fetch to CIR? This is due to the architecture and design of the CPU. From what I gathered it used to work like that in older (synchronous) CPUs, but in modern times we need to use every microsecond, you can latch data into MAR and let those lines float while CPU can work on something else, so MAR and MDR essentialy act as buffers.

### Decode stage
Control unit will decode the instruction stored in the CIR using a binary decoder (implementations can vary), which is essentially a combinational circuit that uses logic gates and converts binary information to signals.

### Execute stage
Control unit of the CPU will then send a signal to specific functional units that will execute operations of the instruction (reads from registers,mathematical operations, binary shifts,…). Result is then sent to main memory.

Also, in most processors, there can be interruptions. When an interrupt happens, the CPU jumps to an interrupt service routine, does what needs to be done, and then goes back to the main program.
## Conclusion
Processing an instruction involves several steps that enable a CPU to execute any command from simple data movements to complex calculations. The instruction cycle, fetch, decode, execute, is fundamental in understanding how CPUs operate. This cycle not only allows the CPU to carry out commands but also manages how these instructions interact with different parts of the system architecture.