"""
AlgoVi - Binary Search
-------------------------
Binary Search implementation that generates
step-by-step states for visualization.
"""


def binary_search(array, target):
    """
    Perform Binary Search and generate visualization steps.

    IMPORTANT:
    Binary Search requires the input array to be sorted.

    Parameters
    ----------
    array : list
        Sorted list of numbers.

    target : int/float
        Value to search for.

    Returns
    -------
    tuple
        (result_index, steps)
    """

    arr = array.copy()

    steps = []

    low = 0
    high = len(arr) - 1

    # Initial state
    steps.append({
        "type": "initial",
        "array": arr.copy(),
        "target": target,
        "low": low,
        "mid": None,
        "high": high,
        "indices": [],
        "eliminated_indices": [],
        "message": f"Searching for {target}",
        "explanation": (
            "Binary Search works on a sorted array. "
            "We begin by considering the entire array."
        )
    })

    eliminated_indices = []

    while low <= high:

        mid = (low + high) // 2

        # Show current middle
        steps.append({
            "type": "middle",
            "array": arr.copy(),
            "target": target,
            "low": low,
            "mid": mid,
            "high": high,
            "indices": [mid],
            "eliminated_indices": eliminated_indices.copy(),
            "message": (
                f"Middle element is {arr[mid]}"
            ),
            "explanation": (
                f"The middle position is {mid}, containing "
                f"{arr[mid]}. We compare it with the target "
                f"value {target}."
            )
        })

        # Target found
        if arr[mid] == target:

            steps.append({
                "type": "found",
                "array": arr.copy(),
                "target": target,
                "low": low,
                "mid": mid,
                "high": high,
                "indices": [mid],
                "eliminated_indices": eliminated_indices.copy(),
                "message": (
                    f"Found {target} at index {mid}"
                ),
                "explanation": (
                    f"The middle element {arr[mid]} is equal "
                    f"to the target {target}. "
                    "The search is successful."
                )
            })

            return mid, steps

        # Target is greater
        elif arr[mid] < target:

            # Elements from low to mid can be eliminated
            eliminated_indices.extend(
                range(low, mid + 1)
            )

            steps.append({
                "type": "discard_left",
                "array": arr.copy(),
                "target": target,
                "low": low,
                "mid": mid,
                "high": high,
                "indices": [mid],
                "eliminated_indices": eliminated_indices.copy(),
                "message": (
                    f"{target} is greater than {arr[mid]}"
                ),
                "explanation": (
                    f"The target {target} is greater than "
                    f"the middle value {arr[mid]}. "
                    "Therefore, the left half can be discarded."
                )
            })

            low = mid + 1

        # Target is smaller
        else:

            # Elements from mid to high can be eliminated
            eliminated_indices.extend(
                range(mid, high + 1)
            )

            steps.append({
                "type": "discard_right",
                "array": arr.copy(),
                "target": target,
                "low": low,
                "mid": mid,
                "high": high,
                "indices": [mid],
                "eliminated_indices": eliminated_indices.copy(),
                "message": (
                    f"{target} is smaller than {arr[mid]}"
                ),
                "explanation": (
                    f"The target {target} is smaller than "
                    f"the middle value {arr[mid]}. "
                    "Therefore, the right half can be discarded."
                )
            })

            high = mid - 1

        # Show new search range
        steps.append({
            "type": "new_range",
            "array": arr.copy(),
            "target": target,
            "low": low,
            "mid": None,
            "high": high,
            "indices": [],
            "eliminated_indices": eliminated_indices.copy(),
            "message": (
                f"New search range: {low} to {high}"
            ),
            "explanation": (
                "The search range has been reduced by "
                "approximately half."
            )
        })

    # Target was not found
    steps.append({
        "type": "not_found",
        "array": arr.copy(),
        "target": target,
        "low": low,
        "mid": None,
        "high": high,
        "indices": [],
        "eliminated_indices": eliminated_indices.copy(),
        "message": f"{target} was not found",
        "explanation": (
            f"The search range became empty, so the target "
            f"{target} does not exist in the array."
        )
    })

    return -1, steps


# ---------------------------------------------------------
# Example usage
# ---------------------------------------------------------

if __name__ == "__main__":

    numbers = [2, 5, 8, 12, 17, 21, 29]

    target = 21

    index, visualization_steps = binary_search(
        numbers,
        target
    )

    print("Array:", numbers)
    print("Target:", target)
    print("Result index:", index)

    print("\nVisualization Steps:")

    for i, step in enumerate(visualization_steps):

        print(
            f"Step {i + 1}: "
            f"{step['message']}"
        )