import streamlit as st

from algorithms.sorting.bubble_sort import bubble_sort_steps
from visualizations.array_visualizer import create_bubble_sort_animation


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AlgoVi",
    page_icon="🔍",
    layout="wide"
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "steps" not in st.session_state:
    st.session_state.steps = []

if "current_step" not in st.session_state:
    st.session_state.current_step = 0


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("AlgoVi")

st.write(
    "Interactive Algorithm Visualization Platform"
)

st.divider()


# --------------------------------------------------
# Bubble Sort Module
# --------------------------------------------------

st.header("Bubble Sort")

st.write(
    "Enter numbers of your choice and generate "
    "the step-by-step execution of Bubble Sort."
)


# --------------------------------------------------
# User Input
# --------------------------------------------------

input_text = st.text_input(
    "Enter numbers separated by commas",
    value="5, 2, 8, 1"
)


# --------------------------------------------------
# Generate Steps
# --------------------------------------------------

if st.button("Generate Visualization"):

    try:
        # Convert text input into integers
        data = [
            int(value.strip())
            for value in input_text.split(",")
            if value.strip()
        ]

        # Check for empty input
        if not data:
            st.error("Please enter at least one number.")

        else:
            # Generate execution steps
            st.session_state.steps = bubble_sort_steps(data)

            # Start from the first step
            st.session_state.current_step = 0

    except ValueError:
        st.error(
            "Please enter only numbers separated by commas."
        )


# --------------------------------------------------
# Display Execution
# --------------------------------------------------

if st.session_state.steps:

    steps = st.session_state.steps
    current_index = st.session_state.current_step

    current_step = steps[current_index]

    st.subheader(
        f"Step {current_index + 1} / {len(steps)}"
    )

    st.write("### Visualization")

    fig = create_bubble_sort_animation(steps)

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )

    st.subheader("Step Explanation")
    
    st.write(
        f"**Action:** {current_step.action.upper()}"
    )
    
    st.write(
        f"**Explanation:** {current_step.description}"
    )
    
    if current_step.indices:
        st.write(
            f"**Active indices:** {current_step.indices}"
        )
    
    if current_step.action == "compare":
        st.info("The algorithm is comparing these two elements.")
    
    elif current_step.action == "swap":
        st.warning("The two elements are being exchanged.")
    
    elif current_step.action == "pass_complete":
        st.success("This pass is complete.")
    
    elif current_step.action == "complete":
        st.success("Bubble Sort has finished.")
        st.divider()


    # --------------------------------------------------
    # Navigation
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Previous",
            disabled=(current_index == 0)
        ):
            st.session_state.current_step -= 1

    with col2:

        if st.button(
            "Next →",
            disabled=(current_index == len(steps) - 1)
        ):
            st.session_state.current_step += 1