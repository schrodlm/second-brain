Pieces of code or data that exist solely for the purpose of verification and do not contribute to the outcome of the computation. This has to be checked by the verification engine. Ghost variables, or ghost fields of records, can only be used in other ghost computations. Otherwise, erasing them before the program is run would lead to incorrect code.

They are essentially auxiliary variables used for reasoning about the code's correctness, typically to track some property or behavior during verification. These variables are eliminated before the program is executed, as they are irrelevant to the final computation.

### Example:

Consider a program where you want to verify that a sorting function is correct. You could introduce a ghost variable to store a copy of the array before sorting to compare it with the result.

Here is a simple example in pseudo-code:

```pseudo
function sort(array A) {
    // Ghost variable: it will not be part of the actual program execution
    ghost variable originalArray = copy(A)
    
    // Sort the array
    performSorting(A)
    
    // Verification: Check if the sorted array has the same elements as the original array
    assert(sameElements(A, originalArray))
    
    return A
}

function sameElements(array A, array B) {
    // Check if both arrays contain the same elements (ignoring order)
    return true if they contain the same elements
}

```
In this example:

- `originalArray` is a **ghost variable**. It is used to verify that the sorted array contains the same elements as the original (to ensure that sorting doesn't add or remove elements).
- `assert(sameElements(A, originalArray))` is a **verification step** to ensure correctness.

This ghost variable will be eliminated before the program is run, but it's essential for the verification process. During verification, the tool would check that the `assert` statement always holds. If the check fails, the sorting function would not pass the verification. However, during actual execution, `originalArray` would not be included, and its existence would have no impact on the program's output.
