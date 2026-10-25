import plotly.graph_objects as go

from models.steps import ExecutionStep


def create_array_figure(
    step: ExecutionStep,
    title: str = "Bubble Sort"
) -> go.Figure:
    """
    Create a Plotly visualization for one execution step.
    """

    values = step.state
    active_indices = set(step.indices)

    # Highlight elements involved in the current operation
    bar_colors = [
        "orange" if index in active_indices else "lightblue"
        for index in range(len(values))
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=list(range(len(values))),
            y=values,
            text=values,
            textposition="outside",
            marker_color=bar_colors,
            hovertemplate=(
                "Index: %{x}<br>"
                "Value: %{y}<extra></extra>"
            )
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Array Index",
        yaxis_title="Value",
        xaxis=dict(
            tickmode="linear",
            dtick=1
        ),
        yaxis=dict(
            range=[
                0,
                max(values) + max(1, max(values) * 0.2)
            ]
        ),
        height=500,
        showlegend=False,
        margin=dict(
            l=40,
            r=40,
            t=80,
            b=60
        )
    )

    return fig


# (Points changed in array_visualizer.py:
#  1. Added current_step_index (default 0) so the chart displays the exact step matching the explanation.
#  2. Set initial values, colors, and title from steps[current_step_index] dynamically for any array.
#  3. Added dynamic title in each frame so video playback displays the ongoing step explanation.
#  4. Synced slider active position with current_step_index.)
def create_bubble_sort_animation(
    steps: list[ExecutionStep],
    current_step_index: int = 0
) -> go.Figure:
    """
    Create an animated Plotly figure from Bubble Sort execution steps.
    """

    if not steps:
        raise ValueError("No execution steps were provided.")

    # Select the current step to visualize according to the ongoing explanation
    current_step_index = max(0, min(current_step_index, len(steps) - 1))
    current_step = steps[current_step_index]

    initial_values = current_step.state
    initial_colors = [
        "salmon" if (current_step.action == "swap" and index in current_step.indices)
        else "orange" if index in current_step.indices
        else "lightgreen" if current_step.action == "complete"
        else "lightblue"
        for index in range(len(initial_values))
    ]

    initial_title = (
        f"Bubble Sort Visualization - Step {current_step.step_number}/{len(steps)}: "
        f"{current_step.description}"
    )

    fig = go.Figure(
        data=[
            go.Bar(
                x=list(range(len(initial_values))),
                y=initial_values,
                text=initial_values,
                textposition="outside",
                marker_color=initial_colors,
                hovertemplate=(
                    "Index: %{x}<br>"
                    "Value: %{y}<extra></extra>"
                )
            )
        ]
    )

    # Create one Plotly frame for every execution step
    frames = []

    for step in steps:

        colors = [
            "salmon" if (step.action == "swap" and index in step.indices)
            else "orange" if index in step.indices
            else "lightgreen" if step.action == "complete"
            else "lightblue"
            for index in range(len(step.state))
        ]

        frame_title = (
            f"Bubble Sort Visualization - Step {step.step_number}/{len(steps)}: "
            f"{step.description}"
        )

        frames.append(
            go.Frame(
                name=str(step.step_number),
                data=[
                    go.Bar(
                        x=list(range(len(step.state))),
                        y=step.state,
                        text=step.state,
                        textposition="outside",
                        marker_color=colors
                    )
                ],
                layout=go.Layout(
                    title=frame_title
                )
            )
        )

    fig.frames = frames

    max_value = max(
        max(step.state)
        for step in steps
    )

    # Animation controls
    fig.update_layout(
        title=initial_title,

        xaxis=dict(
            title="Array Index",
            tickmode="linear",
            dtick=1
        ),

        yaxis=dict(
            title="Value",
            range=[0, max_value + max(1, max_value * 0.2)]
        ),

        height=500,

        showlegend=False,

        margin=dict(
            l=40,
            r=40,
            t=80,
            b=100
        ),

        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "x": 0.1,
                "y": -0.18,
                "xanchor": "left",
                "yanchor": "top",

                "buttons": [
                    {
                        "label": "▶ Play",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {
                                    "duration": 500,
                                    "redraw": True
                                },
                                "transition": {
                                    "duration": 300
                                },
                                "fromcurrent": True
                            }
                        ]
                    },
                    {
                        "label": "⏸ Pause",
                        "method": "animate",
                        "args": [
                            [None],
                            {
                                "frame": {
                                    "duration": 0,
                                    "redraw": False
                                },
                                "mode": "immediate"
                            }
                        ]
                    }
                ]
            }
        ],

        sliders=[
            {
                "active": current_step_index,
                "x": 0.1,
                "y": -0.05,
                "xanchor": "left",
                "yanchor": "top",

                "currentvalue": {
                    "prefix": "Step: "
                },

                "steps": [
                    {
                        "label": str(step.step_number),
                        "method": "animate",
                        "args": [
                            [str(step.step_number)],
                            {
                                "mode": "immediate",
                                "frame": {
                                    "duration": 300,
                                    "redraw": True
                                },
                                "transition": {
                                    "duration": 200
                                }
                            }
                        ]
                    }
                    for step in steps
                ]
            }
        ]
    )

    return fig