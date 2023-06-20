from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    {"id": "main-content"},
    ui.h2("Dynamic UI"),
    ui.input_action_button("btn", "Trigger insert/remove ui"),
    #ui.output_ui("dyn_ui"),
)


def server(input, output, session):
    
    # One way of adding dynamic content is with @render.ui.
    @output
    @render.ui
    def dyn_ui():
        return get_bot_cell()

    # Another way of adding dynamic content is with ui.insert_ui() and ui.remove_ui().
    # The insertion is imperative, so, compared to @render.ui, more care is needed to
    # make sure you don't add multiple copies of the content.
    @reactive.Effect
    def _():
        #btn = input.btn()
        
        ui.remove_ui(selector="div:has(> #justbtn)")
        ui.insert_ui(
            ui.div({"id": "inserted-cell"}, get_bot_cell()),
            selector="#main-content",
            where="beforeEnd",
        )
        ui.insert_ui(
            ui.div({"id": "inserted-cell"}, get_human_cell()),
            selector="#main-content",
            where="beforeEnd",
        )
        ui.insert_ui(
            ui.div({"id": "inserted-cell"}, ui.input_action_button("justbtn", "Trigger insert/remove ui")),
            selector="#main-content",
            where="beforeEnd",
        )
        justbtn = input.justbtn()
        
    
    def get_bot_cell():
                return ui.markdown(
            """
            # Here is some markdown
            ## And some more
            some text \n
            Here comes some code: `print("Hello World")`
            """
            
        )
    
    def get_human_cell():
          return ui.input_text("prompt",
                f"""
                Type your question
                """

          )
          



app = App(app_ui, server)