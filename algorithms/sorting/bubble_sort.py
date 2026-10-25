"""
AlgoVi - Bubble Sort
-----------------------
Bubble Sort implementation that generates
step-by-step states for visualization.
"""
from models.steps import ExecutionStep


def bubble_sort_steps(data: list[int]) -> list[ExecutionStep]:
    """
    Perform Bubble Sort and generate an execution step
    for each important operation.
    """

    arr = data.copy()
    steps = []

    step_number = 1

    # Record the initial state
    steps.append(
        ExecutionStep(
            step_number=step_number,
            state=arr.copy(),
            action="initial",
            indices=[],
            description="Initial array before Bubble Sort begins."
        )
    )

    step_number += 1

    n = len(arr)

    # Bubble Sort
    for i in range(n - 1):

        swapped = False

        for j in range(n - i - 1):

            # Determine comparison outcome description based on actual values
            # (Points changed:
            #  1. Checked whether arr[j] is bigger than arr[j + 1] to give an exact explanation.
            #  2. Formatted description to state whether a swap is required based on which element is bigger/smaller.)
            if arr[j] > arr[j + 1]:
                comparison_description = (
                    f"Comparing {arr[j]} and {arr[j + 1]}. "
                    f"Since {arr[j]} is bigger and {arr[j + 1]} is smaller, they need to be swapped."
                )
            else:
                comparison_description = (
                    f"Comparing {arr[j]} and {arr[j + 1]}. "
                    f"Since {arr[j]} is smaller than or equal to {arr[j + 1]}, no swap is needed."
                )

            # Record comparison
            steps.append(
                ExecutionStep(
                    step_number=step_number,
                    state=arr.copy(),
                    action="compare",
                    indices=[j, j + 1],
                    description=comparison_description
                )
            )

            step_number += 1

            # Check whether swapping is required
            if arr[j] > arr[j + 1]:

                left = arr[j]
                right = arr[j + 1]

                # Perform swap
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

                swapped = True

                # Record swap
                # (Points changed:
                #  1. Clarified swap description to explicitly state that the bigger element was swapped with the smaller element.)
                steps.append(
                    ExecutionStep(
                        step_number=step_number,
                        state=arr.copy(),
                        action="swap",
                        indices=[j, j + 1],
                        description=f"Swapped {left} and {right} because {left} is bigger than {right}."
                    )
                )

                step_number += 1

        # Record completion of this pass
        steps.append(
            ExecutionStep(
                step_number=step_number,
                state=arr.copy(),
                action="pass_complete",
                indices=[],
                description=f"Pass {i + 1} completed."
            )
        )

        step_number += 1

        # If no swap occurred, the array is already sorted
        if not swapped:
            break

    # Record final state
    steps.append(
        ExecutionStep(
            step_number=step_number,
            state=arr.copy(),
            action="complete",
            indices=[],
            description="Bubble Sort completed. The array is now sorted."
        )
    )

    return steps