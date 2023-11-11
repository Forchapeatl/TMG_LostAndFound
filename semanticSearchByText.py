import taipy.gui.builder as tgb
from taipy import Gui


with tgb.Page() as semanticSearchByText:
    tgb.input("{item_name}")
    tgb.button("search" , on_action='search_text_scenario')
    tgb.text("{results_item}")

    tgb.part(partial='{dynamic_content}')



def run(state):
    print("running sematic search")
