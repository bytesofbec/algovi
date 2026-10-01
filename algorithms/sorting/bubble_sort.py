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

            # Record comparison
            steps.append(
                ExecutionStep(
                    step_number=step_number,
                    state=arr.copy(),
                    action="compare",
                    indices=[j, j + 1],
                    description=f"Comparing {arr[j]} and {arr[j + 1]}."
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
                steps.append(
                    ExecutionStep(
                        step_number=step_number,
                        state=arr.copy(),
                        action="swap",
                        indices=[j, j + 1],
                        description=f"Swapped {left} and {right} because {left} is greater than {right}."
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