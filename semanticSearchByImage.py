from taipy.gui import Markdown



semanticSearchByImage = Markdown("""

<|{image_item_name}|image|>
<|{searched_image_content}|file_selector|label=Upload Item|on_action=submit_search_image_scenario|extensions=.jpg,.png|drop_message=Drop Message|>
<|{image_results_item}|image|>

""")

def run(state):
    print("running sematic search on image")