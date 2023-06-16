from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    {"id":"main-content"},
    ui.panel_title("VGR Chatbot"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_text_area("text", "Enter your question"),
            ui.input_action_button("toggle", "Send")
        ),
        ui.panel_main(
            ui.output_text_verbatim("txt")
        )

    ),
    
)



def server(input, output, session):
    x = reactive.Value("Welcome to your chatbot, please enter a question:\n\n")

    @reactive.Effect
    @reactive.event(input.toggle)
    def _():
        x.set(x() + 
              "You asked: " + str(input.text()) + 
              "\n\n" +
              "\tIm sorry I dont have an api key yet :(" +
              "\n\n"
              )

    @output
    @render.text
    def txt():
        return str(x())

app = App(app_ui, server)