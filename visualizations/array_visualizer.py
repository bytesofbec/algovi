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
def create_bubble_sort_animation(
    steps: list[ExecutionStep]
) -> go.Figure:
    """
    Create an animated Plotly figure from Bubble Sort execution steps.
    """

    if not steps:
        raise ValueError("No execution steps were provided.")

    # Use the first step as the initial chart
    first_step = steps[0]

    initial_values = first_step.state

    initial_colors = [
        "orange" if index in first_step.indices else "lightblue"
        for index in range(len(initial_values))
    ]

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
            "orange" if index in step.indices else "lightblue"
            for index in range(len(step.state))
        ]

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
                ]
            )
        )

    fig.frames = frames

    max_value = max(
        max(step.state)
        for step in steps
    )

    # Animation controls
    fig.update_layout(
        title="Bubble Sort Visualization",

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
                "active": 0,
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