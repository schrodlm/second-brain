**Endianness** refers to the order in which bytes are arranged within larger data types (such as integers) when stored in computer memory. It is important when reading or writing multi-byte data to or from memory, particularly when data is shared between systems with different architectures.

## Big endian
In big endian system, the **most significant byte (MSB)** is stored first (at the lowest memory address)
#### Example
(remember that an address can store 1 byte, larger data types are stored across multiple consecutive addresses)
Consider the 4-byte hexadecimal number `0x12345678`
**Memory**
```
Address: 00 01 02 03
Value:   12 34 56 78
```
## Little endian
In little endian systems, the **least significant byte (LSB)** is stored first (at the lowest memory point)
#### Example
Using the same example `0x12345678`
**Memory**
```
Address: 00 01 02 03
Value:   78 56 34 12
```
## Endiannes in systems

**Big endian**
	- traditionally used in system like older PowerPC and soem network protocols ([[TCP/IP]], [[Internet Protocol]])
**Little endian**
	- used in x86 processors, ARM processors and most modern computers

## Why is little endianness more advantageous for modern PCs
- In little-endian systems, when reading or writing multi-byte values (e.g., 16-bit, 32-bit, 64-bit), the **least significant byte** (LSB) is stored first at the lowest memory address. This order allows the CPU to perform operations more easily on small parts of the data, such as reading only the least significant byte for certain calculations.
- For example, if you want to increment a number, little-endian architecture allows you to start with the **lowest byte**, which is the most likely to change, and avoid having to read all higher bytes unless they need to be updated (in cases where there’s an overflow).

### Significance of Endianness

Endianness matters when:
- Transferring data between systems with different endianness
- Working with low-level data manipulation, like network communication, file formats, or hardware devices
- Interpreting memory dumps or debugging low-level software

Programs and systems that communicate over a network often standardize on **big-endian**, also known as **network byte order**, to ensure consistent data transmission across different systems.