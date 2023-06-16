from shiny import App, reactive, render, ui
import numpy as np
from matplotlib import pyplot as plt


app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_action_button("value", "noise"),
            ui.input_slider("smooth", "Smoothness", 1, 100, 1, step=1),
            ui.output_text("value")
        ),
        ui.panel_main(
            ui.output_plot("nice_sine"),
            ui.output_plot("nice_cos"),
            ui.output_plot("nice_tan")
        )

    ),
    
)



def server(input, output, session):
    x = reactive.Value("Welcome to your chatbot, please enter a question:\n\n")

    @output
    @render.text
    @reactive.event(input.value)
    def value():
        a = np.random.randint(1,11)
        return str(a)

    @output
    @render.plot
    @reactive.Calc
    def nice_sine():
        z = input.smooth()
        x = np.linspace(0,10,z)
        y = np.sin(x)
        return plt.plot(x,y)
    
    @output
    @render.plot
    @reactive.Calc
    def nice_cos():
        z = input.smooth()
        x = np.linspace(0,10,z)
        y = np.cos(x)
        return plt.plot(x,y)
    
    @output
    @render.plot
    @reactive.Calc
    def nice_tan():
        z = input.smooth()
        x = np.linspace(0,10,z)
        y = np.tan(x)
        return plt.plot(x,y)

   


app = App(app_ui, server)