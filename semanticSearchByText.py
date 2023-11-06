from taipy.gui import Markdown



semanticSearchByText = Markdown("""

<|{item_name}|input|>
<|search|button|on_action=search_text_scenario|>
<|{results_item}|text|>

""")

def run(state):
    print("running sematic search")