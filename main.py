import os
import shutil
import taipy.gui.builder as tgb
import taipy as tp

from taipy.gui import Gui, notify , Markdown
from taipy import Config , Core

import pymongo
from pymongo import MongoClient
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel
from dotenv import load_dotenv
from google.cloud.bigquery.client import Client


import pandas as pd

load_dotenv()


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_CLOUD_CREDENTIALS')
bq_client = Client()
mongodb_connection = os.getenv('MONGODB_CONNECTION_STRING')
cluster = MongoClient(mongodb_connection)
db = cluster["lostandfound"]
collection = db["items"]
#cursor = db.list_collection_names()

PROJECT_ID= os.getenv('MONGODB_POJECT_ID')

dict_for_items = []


for obj in collection.find({}):
    dict_for_items.append(obj)
    print(obj)


print(dict_for_items)


def generate_text_embedding(sentence) -> list:
    """Text embedding with a Large Language Model."""
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([sentence])
    for embedding in embeddings:
        vector = embedding.values
        print(f"Length of Embedding Vector: {len(vector)}")
    return vector


#for doc in collection.find({'how':{"$exists": True}}).limit(50):
#    doc['plot_embedding_hf'] = generate_text_embedding(doc['how'])
#    collection.replace_one({'_id': doc['_id']}, doc)

def show_item_info(state,id):
    item_info = dict_for_items[int(id)]
    notify(state, 'info', f"The text is: {item_info['how']}")


item_name = "Phone"
results_item = None

with tgb.Page() as itemsPage:
    with tgb.layout("2 2 1"):
        with tgb.part():
            for i in range(0 , len(dict_for_items)):
                tgb.button({str(dict_for_items[i]['where'])} , id=i, on_action = 'show_item_info')
                tgb.html("p", dict_for_items[i]['how'])
        with tgb.part():
            tgb.input("{item_name}", label="search lost item")
            tgb.button("search" , on_action ='search_text_scenario')
            tgb.text("results_item")





input_name = "Taipy"
input_date = ""
input_where = ""
input_lost_or_found = ""
input_how = " "
image_url=""
input_circle_account = ""
dt=''
content = ''
message = None

page = """

name: <|{input_name}|input|>
when: <|{input_date}|date|>
where: <|{input_where}|input|>
lost/found: <|{input_lost_or_found}|input|>
how: <|{input_how}|input|multiline|>
circle: <|{input_circle_account}|input|>


<|{content}|file_selector|label=Upload File|on_action=upload_image|extensions=.jpg,.png|drop_message=Drop Message|>


<|submit|button|on_action=submit_scenario|>

Message: <|{message}|text|>


"""
searchPage = """

<|{item_name}|input|>
<|search|button|on_action=search_text_scenario|>
<|{results_item}|text|>

"""




def searchItemByText(keyword: str):

    query = keyword

    results = collection.aggregate([
        {"$vectorSearch": {
        "queryVector": generate_text_embedding(query),
        "path": "plot_embedding_hf",
        "numCandidates": 100,
        "limit": 4,
        "index": "PlotSemanticSearch",
          }}]);

    #for document in results:
    #    print(f'Found Item: {document["how"]}\n')

    return results


def upload_image(state):

    filename = state.content[5:]

    shutil.move(state.content, 'photos/'+ filename)

    notify(state, 'info', f'The text is: {state.content}')


def submit_scenario(state):
    notify(state, 'info', f'The text is: {state.content}')

    state.scenario.input_name.write(state.input_name)
    state.scenario.input_date.write(state.input_date)
    state.scenario.input_where.write(state.input_where)
    state.scenario.input_lost_or_found.write(state.input_lost_or_found)
    state.scenario.input_how.write(state.input_how)
    #state.scenario.input_circle_account.write(state.intput_where)


    state.scenario.submit(wait=True)
    state.message = scenario.message.read()

def build_message(name:str , when,  where :str, lost_or_found : str , how : str ):
    collection.insert_one({"name":name,"when": str(when) , "where": where , "lost_or_found" : lost_or_found , "how":how })
    return 

    


def search_text_scenario(state):
    notify(state, 'info', f'The text is: {state.content}')

    state.scenario_search.item_name.write(state.item_name)
    state.scenario_search.submit(wait=True)
    state.results_item = scenario_search.results_item.read()

def build_search_text_results(keyword: str):

    results = searchItemByText(keyword)
    output = ""

    for document in results:
        output += document["how"]
        output +='\n'

    return f"{output}"


#input configure
input_name_data_node_cfg = Config.configure_data_node(id="input_name")
input_when_data_node_cfg = Config.configure_data_node(id="input_date")
input_where_data_node_cfg = Config.configure_data_node(id="input_where")
input_lost_or_found_data_node_cfg = Config.configure_data_node(id="input_lost_or_found")
input_how_data_node_cfg = Config.configure_data_node(id="input_how")
input_where_data_node_cfg = Config.configure_data_node(id="input_where")

#input items
input_item_name_data_node_cfg = Config.configure_data_node(id="item_name")





#output configure
results_item_data_node_cfg = Config.configure_data_node(id="results_item")
build_text_search_task_cfg = Config.configure_task(id="build_search",function=build_search_text_results,input=[input_item_name_data_node_cfg ],output = results_item_data_node_cfg)
text_search_scenario_cfg = Config.configure_scenario("scenario_search", task_configs=[build_text_search_task_cfg ])


message_data_node_cfg = Config.configure_data_node(id="message")
build_msg_task_cfg = Config.configure_task(id="build_msg",function=build_message,input=[input_name_data_node_cfg,input_when_data_node_cfg, input_where_data_node_cfg ,input_lost_or_found_data_node_cfg ,input_how_data_node_cfg , input_where_data_node_cfg ],output = message_data_node_cfg)
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])

page+="""<|toggle|theme|>"""

pages = {"/": "<|navbar|>",
         'items': itemsPage,
         'Search':searchPage,
         'Request': page,
}


if __name__ == "__main__":
    Core().run()
    scenario = tp.create_scenario(scenario_cfg)
    scenario_search = tp.create_scenario(text_search_scenario_cfg)
    Gui(pages = pages).run()


"""

image upload, ajax -->reflect db changes , file upload ,

input does not reset on submit

place holder , search ,
sessions , request

with page and string styling

text area multiline typing / delete not working
checkbox or select option

cant notify without state

if you don't return from the build message , you get NULL in mongodb
ssh connection works only after dropping app

comment on markdown

markdown up , functions down but function must come before markdown if used

Dialog content with tgb page

"""


"""
Google Cloud , service account key

mongodb close brackets (python search query) error on this link - > https://www.mongodb.com/library/vector-search/building-generative-ai-applications-using-mongodb?lb-mode=overlay
"""


