import taipy.gui.builder as tgb
from taipy import Gui



with tgb.Page() as semanticSearchByImage:
    tgb.image("{image_item_path}")
    tgb.file_selector("{searched_image_content}" ,label='Upload Item', on_action='submit_search_image_scenario' , extensions='.jpg,.png')
    
    tgb.image("{image_results_item}")
    tgb.part(partial='{dynamic_content_image}')



def run(state):
    print("running sematic search on image")
