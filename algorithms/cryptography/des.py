"""
AlgoVi - DES Visualizer
--------------------------
Educational implementation of DES designed to generate
step-by-step visualization states.

DES:
    - 64-bit block size
    - 64-bit input key
    - 56 effective key bits
    - 16 Feistel rounds
"""


# =========================================================
# DES TABLES
# =========================================================

# Initial Permutation
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]


# Final Permutation
FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]


# Expansion permutation
E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]


# Permuted Choice 1
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]


# Permuted Choice 2
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]


# Left rotations for key generation
SHIFT_SCHEDULE = [
    1, 1, 2, 2,
    2, 2, 2, 2,
    1, 2, 2, 2,
    2, 2, 2, 1
]


# P permutation
P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]


# =========================================================
# S-BOXES
# =========================================================

S_BOXES = [

    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],

    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],

    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],

    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],

    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],

    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],

    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],

    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def permute(bits, table):
    """
    Apply a permutation table to a bit string.
    """

    return "".join(
        bits[position - 1]
        for position in table
    )


def xor_bits(a, b):
    """
    XOR two equal-length binary strings.
    """

    return "".join(
        "0" if x == y else "1"
        for x, y in zip(a, b)
    )


def left_rotate(bits, count):
    """
    Circular left rotation.
    """

    return bits[count:] + bits[:count]


def validate_binary(value, length):
    """
    Validate that value is a binary string of a given length.
    """

    if not isinstance(value, str):
        raise TypeError("Input must be a string.")

    if len(value) != length:
        raise ValueError(
            f"Input must contain exactly {length} bits."
        )

    if any(bit not in "01" for bit in value):
        raise ValueError(
            "Input must contain only 0 and 1."
        )


# =========================================================
# KEY GENERATION
# =========================================================

def generate_round_keys(key):
    """
    Generate the 16 DES round keys.

    Returns:
        round_keys
        key_steps
    """

    validate_binary(key, 64)

    key_steps = []

    # PC-1 removes parity bits
    permuted_key = permute(key, PC1)

    key_steps.append({
        "type": "pc1",
        "key": key,
        "permuted_key": permuted_key,
        "message": "Apply Permuted Choice 1",
        "explanation": (
            "The 64-bit key is reduced to 56 bits by "
            "removing the parity bits using PC-1."
        )
    })

    C = permuted_key[:28]
    D = permuted_key[28:]

    round_keys = []

    for round_number, shift in enumerate(
        SHIFT_SCHEDULE,
        start=1
    ):

        C = left_rotate(C, shift)
        D = left_rotate(D, shift)

        combined = C + D

        round_key = permute(combined, PC2)

        round_keys.append(round_key)

        key_steps.append({
            "type": "round_key",
            "round": round_number,
            "C": C,
            "D": D,
            "round_key": round_key,
            "shift": shift,
            "message": (
                f"Generated Round Key K{round_number}"
            ),
            "explanation": (
                f"C and D are rotated left by {shift} "
                f"position(s), then PC-2 generates the "
                f"48-bit round key K{round_number}."
            )
        })

    return round_keys, key_steps


# =========================================================
# S-BOX SUBSTITUTION
# =========================================================

def sbox_substitution(bits):
    """
    Apply all eight DES S-boxes.

    Returns:
        output_bits
        details
    """

    output = ""
    details = []

    for i in range(8):

        block = bits[i * 6:(i + 1) * 6]

        # Row = first and last bit
        row = int(
            block[0] + block[5],
            2
        )

        # Column = middle four bits
        column = int(
            block[1:5],
            2
        )

        value = S_BOXES[i][row][column]

        output_bits = format(value, "04b")

        output += output_bits

        details.append({
            "sbox": i + 1,
            "input": block,
            "row": row,
            "column": column,
            "value": value,
            "output": output_bits
        })

    return output, details


# =========================================================
# FEISTEL FUNCTION
# =========================================================

def feistel(right, round_key, round_number):
    """
    DES Feistel function.

    Returns:
        result
        details
    """

    # Expansion
    expanded = permute(right, E)

    # XOR with round key
    xor_result = xor_bits(
        expanded,
        round_key
    )

    # S-box
    sbox_output, sbox_details = sbox_substitution(
        xor_result
    )

    # P permutation
    p_output = permute(
        sbox_output,
        P
    )

    details = {
        "round": round_number,
        "right": right,
        "expanded": expanded,
        "round_key": round_key,
        "xor": xor_result,
        "sbox_input": xor_result,
        "sbox_output": sbox_output,
        "sbox_details": sbox_details,
        "p_output": p_output
    }

    return p_output, details


# =========================================================
# DES ENCRYPTION
# =========================================================

def des_encrypt(plaintext, key):
    """
    Encrypt a 64-bit plaintext block using DES.

    Parameters
    ----------
    plaintext : str
        64-bit binary plaintext.

    key : str
        64-bit binary key.

    Returns
    -------
    tuple
        (ciphertext, steps)
    """

    validate_binary(
        plaintext,
        64
    )

    validate_binary(
        key,
        64
    )

    steps = []

    # -----------------------------------------------------
    # Generate keys
    # -----------------------------------------------------

    round_keys, key_steps = generate_round_keys(key)

    # Store key-generation information
    steps.append({
        "type": "key_generation",
        "round_keys": round_keys,
        "key_steps": key_steps,
        "message": "Generate 16 round keys",
        "explanation": (
            "DES generates sixteen 48-bit round keys "
            "from the original 64-bit key."
        )
    })

    # -----------------------------------------------------
    # Initial permutation
    # -----------------------------------------------------

    permuted = permute(
        plaintext,
        IP
    )

    steps.append({
        "type": "initial_permutation",
        "input": plaintext,
        "output": permuted,
        "message": "Initial Permutation",
        "explanation": (
            "The 64-bit plaintext is rearranged using "
            "the DES Initial Permutation table."
        )
    })

    # -----------------------------------------------------
    # Split into L0 and R0
    # -----------------------------------------------------

    left = permuted[:32]
    right = permuted[32:]

    steps.append({
        "type": "split",
        "round": 0,
        "left": left,
        "right": right,
        "message": "Split into L0 and R0",
        "explanation": (
            "After the initial permutation, the 64-bit "
            "block is divided into two 32-bit halves."
        )
    })

    # -----------------------------------------------------
    # 16 Feistel rounds
    # -----------------------------------------------------

    for round_number in range(1, 17):

        old_left = left
        old_right = right

        f_output, details = feistel(
            old_right,
            round_keys[round_number - 1],
            round_number
        )

        new_left = old_right

        new_right = xor_bits(
            old_left,
            f_output
        )

        left = new_left
        right = new_right

        # Main round state
        steps.append({
            "type": "round",
            "round": round_number,
            "left_before": old_left,
            "right_before": old_right,
            "left_after": new_left,
            "right_after": new_right,
            "round_key": round_keys[
                round_number - 1
            ],
            "feistel": details,
            "message": (
                f"Round {round_number}"
            ),
            "explanation": (
                f"Round {round_number} uses the Feistel "
                "function. The right half is transformed "
                "and XORed with the previous left half."
            )
        })

        # Individual operations
        steps.append({
            "type": "expansion",
            "round": round_number,
            "input": old_right,
            "output": details["expanded"],
            "message": (
                f"Round {round_number}: Expansion"
            ),
            "explanation": (
                "The 32-bit right half is expanded to "
                "48 bits using the expansion permutation."
            )
        })

        steps.append({
            "type": "key_xor",
            "round": round_number,
            "expanded": details["expanded"],
            "round_key": details["round_key"],
            "output": details["xor"],
            "message": (
                f"Round {round_number}: XOR with K{round_number}"
            ),
            "explanation": (
                "The expanded right half is XORed with "
                f"the 48-bit round key K{round_number}."
            )
        })

        steps.append({
            "type": "sbox",
            "round": round_number,
            "input": details["sbox_input"],
            "output": details["sbox_output"],
            "details": details["sbox_details"],
            "message": (
                f"Round {round_number}: S-Box Substitution"
            ),
            "explanation": (
                "The 48-bit result is divided into eight "
                "6-bit blocks. Each block passes through "
                "an S-box and becomes 4 bits."
            )
        })

        steps.append({
            "type": "pbox",
            "round": round_number,
            "input": details["sbox_output"],
            "output": details["p_output"],
            "message": (
                f"Round {round_number}: P-Box Permutation"
            ),
            "explanation": (
                "The 32-bit S-box output is rearranged "
                "using the P permutation."
            )
        })

        steps.append({
            "type": "round_result",
            "round": round_number,
            "left": left,
            "right": right,
            "message": (
                f"End of Round {round_number}"
            ),
            "explanation": (
                f"Round {round_number} is complete. "
                "The resulting left and right halves "
                "are passed to the next round."
            )
        })

    # -----------------------------------------------------
    # Swap final halves
    # -----------------------------------------------------

    combined = right + left

    steps.append({
        "type": "final_swap",
        "left": left,
        "right": right,
        "combined": combined,
        "message": "Swap final halves",
        "explanation": (
            "After Round 16, the two halves are swapped "
            "before applying the final permutation."
        )
    })

    # -----------------------------------------------------
    # Final permutation
    # -----------------------------------------------------

    ciphertext = permute(
        combined,
        FP
    )

    steps.append({
        "type": "final_permutation",
        "input": combined,
        "output": ciphertext,
        "message": "Final Permutation",
        "explanation": (
            "The final 64-bit block is rearranged using "
            "the inverse of the Initial Permutation."
        )
    })

    # -----------------------------------------------------
    # Complete
    # -----------------------------------------------------

    steps.append({
        "type": "complete",
        "plaintext": plaintext,
        "key": key,
        "ciphertext": ciphertext,
        "message": "DES encryption completed",
        "explanation": (
            "The DES encryption process has completed "
            "and the resulting 64-bit ciphertext is ready."
        )
    })

    return ciphertext, steps


# =========================================================
# EXAMPLE
# =========================================================

if __name__ == "__main__":

    # Standard DES test vector
    plaintext = (
        "00000001001000110100010101100111"
        "10001001101010111100110111101111"
    )

    key = (
        "00010011001101000101011101111001"
        "1001101110111101111111110001"
    )

    # The key above should be exactly 64 bits.
    # Use a known standard test vector instead:
    plaintext = (
        "00000001001000110100010101100111"
        "10001001101010111100110111101111"
    )

    key = (
        "00010011001101000101011101111001"
        "1001101010111100110111101111"
    )

    # Make sure lengths are correct
    print("Plaintext length:", len(plaintext))
    print("Key length:", len(key))

    try:

        ciphertext, steps = des_encrypt(
            plaintext,
            key
        )

        print("\nCiphertext:")
        print(ciphertext)

        print("\nTotal visualization steps:")
        print(len(steps))

        print("\nFirst few steps:")

        for i, step in enumerate(steps[:5]):

            print(
                f"{i + 1}. "
                f"{step['message']}"
            )

    except Exception as error:

        print("Error:", error)