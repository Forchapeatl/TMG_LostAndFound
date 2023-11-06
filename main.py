import os
import shutil
import taipy.gui.builder as tgb
import taipy as tp
import pymongo
import pandas as pd


from taipy.gui import Gui, notify , Markdown
from taipy import Config , Core

from pymongo import MongoClient
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel
from vertexai.vision_models import MultiModalEmbeddingModel
from vertexai.vision_models import  Image
from dotenv import load_dotenv
from google.cloud.bigquery.client import Client
from form import form_md
from semanticSearchByText import semanticSearchByText 
from semanticSearchByImage import semanticSearchByImage


load_dotenv()


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-credentials.json'
bq_client = Client()
mongodb_connection = os.getenv("MONGODB_CONNECTION_S")
cluster = MongoClient(mongodb_connection)
db = cluster["lostandfound"]
collection = db["items"]
#cursor = db.list_collection_names()

PROJECT_ID= os.getenv("MONGODB_POJECT_ID")

dict_for_items = []

content = ''
message = None
item_name = ''
results_item = None
path = None
input_name = ''
input_item_type = ''
input_date = ''
input_where = ''
input_lost_or_found = ''
input_how = ''
image_url=''
input_circle_account = ''


image_item_name = ''
searched_image_content = ''
image_results_item=''


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


def generate_image_embedding(image):
    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")
    image = Image.load_from_file("35.png")

    embeddings = model.get_embeddings(
        image=image,
        contextual_text='',
    )
    image_embedding = embeddings.image_embedding

    print(len(image_embedding))


#for doc in collection.find({'how':{"$exists": True}}).limit(50):
#    doc['plot_embedding_hf'] = generate_text_embedding(doc['how'])
#    collection.replace_one({'_id': doc['_id']}, doc)


#for doc in collection.find({'how':{"$exists": True}}).limit(50):
#    doc['plot_image_embedding_hf'] = generate_image_embedding(doc['image'])
#    collection.replace_one({'_id': doc['_id']}, doc)


def show_item_info(state,id):
    item_info = dict_for_items[int(id)]
    notify(state, 'info', f"The text is: {item_info['how']}")




with tgb.Page() as itemsPage:
    with tgb.layout("2 2"):
        with tgb.part():
            for i in range(0 , len(dict_for_items) , 2):
                tgb.image(dict_for_items[i]['image'])
                tgb.button({str(dict_for_items[i]['where'])} , id=i, on_action = 'show_item_info')
                tgb.html("p", dict_for_items[i]['how'])
        with tgb.part():
            for i in range(1 , len(dict_for_items) , 2):
                tgb.image(dict_for_items[i]['image'])
                tgb.button({str(dict_for_items[i]['where'])} , id=i, on_action = 'show_item_info')
                tgb.html("p", dict_for_items[i]['how'])



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

    notify(state, 'info', f'The text is: {state.path}')


def submit_scenario(state):
    notify(state, 'info', f'The text is: {state.content}')

    state.scenario.input_name.write(state.input_name)
    state.scenario.input_item_type.write(state.input_item_type)
    state.scenario.input_date.write(state.input_date)
    state.scenario.input_where.write(state.input_where)
    state.scenario.input_lost_or_found.write(state.input_lost_or_found)
    state.scenario.input_how.write(state.input_how)
    state.scenario.path.write(state.path)
    #state.scenario.input_circle_account.write(state.intput_where)


    state.scenario.submit(wait=True)
    state.message = scenario.message.read()

def build_message(name:str ,item:str, when,  where :str, lost_or_found : str , how : str  , image : str):
    collection.insert_one({"username":name, "item": item ,"when": str(when) , "where": where , "lost_or_found" : lost_or_found , "how":how , "image" : image})
    return f"{item}"
    


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



def submit_search_image_scenario(state):
    #image_item_name = ''
    #searched_image_content = ''
    #image_results_item=''

    state.scenario_search_image.searched_image_content.write(state.searched_image_content)


def build_search_image_results(imagePath: str):
    return 



#configure request submit
input_name_data_node_cfg = Config.configure_data_node(id="input_name")
input_item_type_data_node_cfg = Config.configure_data_node(id="input_item_type")
input_when_data_node_cfg = Config.configure_data_node(id="input_date")
input_where_data_node_cfg = Config.configure_data_node(id="input_where")
input_lost_or_found_data_node_cfg = Config.configure_data_node(id="input_lost_or_found")
input_how_data_node_cfg = Config.configure_data_node(id="input_how")
input_where_data_node_cfg = Config.configure_data_node(id="input_where")
image_path_data_node_cfg = Config.configure_data_node(id="path")
message_data_node_cfg = Config.configure_data_node(id="message")
build_msg_task_cfg = Config.configure_task(id="build_msg",
                                            function=build_message,
                                            input=[input_name_data_node_cfg,
                                            input_item_type_data_node_cfg,
                                            input_when_data_node_cfg, 
                                            input_where_data_node_cfg,
                                            input_lost_or_found_data_node_cfg,
                                            input_how_data_node_cfg,
                                            input_where_data_node_cfg,
                                            image_path_data_node_cfg ],output = message_data_node_cfg)
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])



#Configure sematic text search
input_item_name_data_node_cfg = Config.configure_data_node(id="item_name")
results_item_data_node_cfg = Config.configure_data_node(id="results_item")
build_text_search_task_cfg = Config.configure_task(id="build_search",function=build_search_text_results,input=[input_item_name_data_node_cfg ],output = results_item_data_node_cfg)
text_search_scenario_cfg = Config.configure_scenario("scenario_search", task_configs=[build_text_search_task_cfg ])


#configure sematic image Search
input_searched_image_content_data_node_cfg = Config.configure_data_node(id="searched_image_content")
image_results_item_data_node_cfg = Config.configure_data_node(id ="image_results_item")
build_image_search_task_cfg = Config.configure_task(id="build_image_search",function=build_search_image_results,input=[],output = image_results_item_data_node_cfg)
image_search_scenario_cfg = Config.configure_scenario("scenario_search_image", task_configs=[])




pages = {"/": "<|navbar|>",
         'items': itemsPage,
         'SearchByText':semanticSearchByText,
         'Request':form_md,
         'SearchByImage': semanticSearchByImage 

}


if __name__ == "__main__":
    Core().run()
    scenario = tp.create_scenario(scenario_cfg)
    scenario_search = tp.create_scenario(text_search_scenario_cfg)
    scenario_search_image = tp.create_scenario(image_search_scenario_cfg)
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

you cannot search on enter key

markdown vs page builder

date input breaks lines
search on enter key

"""


"""
Google Cloud , service account key

mongodb close brackets (python search query) error on this link - > https://www.mongodb.com/library/vector-search/building-generative-ai-applications-using-mongodb?lb-mode=overlay
"""


