"""Factorial Christmas Tree Generator.

This module generates a christmas tree made out of factorials, from the first
to a specified amount. You can either supply an argument to its size or just
run the program and it will ask you for it in the terminal. The trunk is a
fixed size, and if the tree width for a given tree size is smaller than the
base width, there will be some problems.
"""
import sys
import os


def calculate_factorial(number: int) -> int:
    """Calculate the factorial of a given number.

    Args:
        number (int): The number to calculate the factorial of.

    Returns:
        int: The factorial of the given number.
    """
    if number <= 1:
        return number
    else:
        return number * calculate_factorial(number - 1)


def create_tree_head(size: int) -> dict:
    """Create the head of the tree.

    Args:
        size (int): The number of layers in the tree head.

    Returns:
        dict: A dictionary with keys "head" and "span", containing a list of
            strings of the factorials for the christmas tree head and an
            integer representing the span of the tree, respectively.
    """
    # Create a list that holds all the
    # factorials wanted
    factorials = []
    for i in range(size):
        factorials.append(str(calculate_factorial(i+1)))

    # Make the return list that contains the needed modifications for proper
    # output, the first being a fuller character for a balanced tree.
    result = []
    for factorial in factorials:

        # Since the starting factorial is 1, to keep the tree balanced each
        # factorial's length has to have the same parity, that being odd.
        # If the length is even, add a fuller character to balance it.
        if len(factorial) % 2 == 0:
            # The factorial is even, so find the "middle" and insert the
            # fuller character
            middle = int(len(factorial) / 2)
            result.append(factorial[:middle] + "#" + factorial[middle:])

        # No need for a fuller character, so just add it straight in
        else:
            result.append(factorial)

    # The second modification is the needed whitespace so that it doesn't all
    # print off at one side and look like a staircase. Get half the length of
    # the longest factorial (that being the last one) to use as reference.
    length = int(len(result[-1]) / 2)
    for i in range(len(result[:-1])):
        # Calculate  and add the offset with how far half the length of the
        # factorial already goes taken away from the reference length.
        middle = int(len(result[i]) / 2)
        result[i] = (" " * (length - middle)) + result[i]

    # Return both the head and the "span" of the tree. Another function finds
    # the "span" useful information and it is simpler to give it in dict form
    # rather than recalculate.
    return {"head": result, "span": len(result[-1]) - 1}


def create_tree_base(width: int, height: int, tree_span: int) -> list[str]:
    """Create the base of the tree.

    Args:
        width (int): The number of layers in the tree base.
        height (int): The length of each layer in the tree base.
        tree_span (int): The span of the tree.

    Returns:
        list: A list of strings representing the tree base layers.
    """
    # Calculate the offset each layer of the bark needs so that it appears in
    # the middle
    offset = int((tree_span - width) / 2)

    # Create and return the list which contains all the bark layers
    result = [(offset * " ") + ("#" * width)] * height
    return result


if __name__ == "__main__":
    # Either use arguments if any were given or take input from the command
    # line for the christmas tree size
    try:
        tree_head = create_tree_head(int(sys.argv[1]))
    except IndexError:
        tree_head = create_tree_head(int(
            input("How many factorials do you want to make the tree? \n>>> ")))
    except Exception as e:
        # Something has gone wrong, raise that error
        raise e

    # Output tree head
    for layer in tree_head["head"][:-1]:
        print(layer)

    # Small error correction. If the last factorial is just as long as the
    # terminal size, when it outputs it to the screen the newline character
    # continues on to the lext line which leaves a gap between tree head and
    # trunk, so if the last factorial is just that long, don't end the output
    # with a newline.
    if len(tree_head["head"][-1]) == os.get_terminal_size().columns:
        print(tree_head["head"][-1], end="")
    else:
        print(tree_head["head"][-1])

    # Output tree trunk
    tree_base = create_tree_base(9, 7, tree_head["span"])
    for layer in tree_base:
        print(layer)
