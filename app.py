import gradio as gr
from classifier import ThemeClassifier
from characters import CharacterNetworkGenerator, NamedEntityRecognizer

def process(theme_list, subtitles_path, save_path):

    if not save_path:
        save_path = "cache"
    
    if not subtitles_path:
        subtitles_path = "data/subs"

    theme_list = theme_list.split(",")
    themes = [theme.lower().strip() for theme in theme_list]
    clf = ThemeClassifier(themes)

    output_df = clf.get_themes(subtitles_path,save_path)
    output_df = output_df[themes]

    output_df = output_df[themes].sum().reset_index()
    output_df.columns = ['Theme','Score']

    output_chart = gr.BarPlot(
        output_df,
        x="Theme",
        y="Score",
        title="Series Themes",
        tooltip=["Theme","Score"],
        vertical=False,
        width=500,
        height=260
    )

    return output_chart
    

def get_char_network(subtitles_path, save_path):

    char_network = CharacterNetworkGenerator()
    ner = NamedEntityRecognizer()

    if not save_path:
        save_path = "cache"
    
    if not subtitles_path:
        return char_network.defaultGraph(save_path)

    ner_df = ner.get_ners(subtitles_path, save_path)
    df = char_network.generate_char_network(ner_df)
    html = char_network.draw_char_network(df)

    return html
    

def main():

    # Theme Classification (Zero Shot Classifier):
    with gr.Blocks() as iface:
        with gr.Row():
            with gr.Column():
                gr.HTML('<h1>How I Met Your Mother</h1><h2>Theme Classification (Zero Shot Classifier)</h2>')
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()
                    with gr.Column():
                        theme_list = gr.Textbox(label="Themes")
                        subtitles_path = gr.Textbox(label="Subtitles or script Path")
                        save_path = gr.Textbox(label="Save Path")

                        get_theme = gr.Button("Go")
                        get_theme.click(process, inputs=[theme_list, subtitles_path, save_path], outputs=[plot])
    
    # Character Network:
        with gr.Row():
            with gr.Column():
                gr.HTML('<h2>Character Network</h2>')
                with gr.Row():
                    with gr.Column():
                        network = gr.HTML()
                    with gr.Column():
                        subtitles_path = gr.Textbox(label="Subtitles or script Path")
                        save_path = gr.Textbox(label="Save Path")
                        get_network = gr.Button("Go")
                        get_network.click(get_char_network, inputs=[subtitles_path, save_path], outputs=[network])
        
    iface.launch(share=True)

if __name__ == "__main__":
    main()

# drama, vulgar, sex, sacrifice, happy, romance, love, friendship, sad, anger, betrayel, narration, funny