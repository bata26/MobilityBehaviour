import plotly.graph_objects as go
class LearningReport:

    def __init__(self, losses):
        self.title = "MSE chart for classifier error"
        self.y = losses

    def show_plot(self):
        fig = go.Figure(layout_title_text="Accuracy error MSE")
        fig.add_trace(
            go.Scatter(
                y=self.y,
                mode="lines+markers",
                name = "error",
                showlegend=True
            )
        )

        fig.write_image("./images/learning_plot.png")
