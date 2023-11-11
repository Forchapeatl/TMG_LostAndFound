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


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'mongodb-403805-3cf96c2ad447.json'
bq_client = Client()
mongodb_connection = os.getenv("MONGODB_CONNECTION_S")
cluster = MongoClient(mongodb_connection)
db = cluster["lostandfound"]
collection = db["items"]
#cursor = db.list_collection_names()

PROJECT_ID= os.getenv("MONGODB_POJECT_ID")

dict_for_items = []
dict_for_searchByText = []
dict_for_searchByImage = []

content = ''
message = None
item_name = ''
results_item = None
path = None
input_contact = ''
input_item_type = ''
input_date = ''
input_where = ''
input_lost_or_found = ''
input_how = ''
image_url=''
input_circle_account = ''


image_item_path = ''
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
    image = Image.load_from_file(image)#1408

    embeddings = model.get_embeddings(
        image=image,
        contextual_text='',
    )
    image_embedding = embeddings.image_embedding

    return image_embedding


def show_item_info(state,id):
    item_info = dict_for_items[int(id)]
    notify(state, 'info', f"{item_info['how']}")


with tgb.Page() as itemsPage:
    with tgb.layout("2 2"):
        with tgb.part():
            for i in range(0 , len(dict_for_items) , 2):
                tgb.image(dict_for_items[i]['image'] , hover_text=dict_for_items[i]['lost_or_found'])
                tgb.button(dict_for_items[i]['contact'] , class_name='plain')
                tgb.text(dict_for_items[i]['lost_or_found'] + " at" ,class_name='plain')                
                tgb.button(dict_for_items[i]['where'] , id=i, on_action = 'show_item_info')
                tgb.html("p", dict_for_items[i]['how'])
        with tgb.part():
            for i in range(1 , len(dict_for_items) , 2):
                tgb.image(dict_for_items[i]['image'] , hover_text=dict_for_items[i]['lost_or_found'])
                tgb.button(dict_for_items[i]['contact'] , class_name='plain')
                tgb.text(dict_for_items[i]['lost_or_found']+ " at " , class_name='plain')                
                
                tgb.button(dict_for_items[i]['where'] , id=i, on_action = 'show_item_info')
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

    return results


def searchItemByImage(imagePath: str):

    query = imagePath

    results = collection.aggregate([
        {"$vectorSearch": {
        "queryVector": generate_image_embedding(imagePath),
        "path": "plot_image_embedding_hf",
        "numCandidates": 100,
        "limit": 4,
        "index": "PlotSemanticImageSearch",
          }}]);

    return results


def upload_image(state):

    filename = state.path[5:]
    shutil.move(state.path, 'photos/'+ filename)
    state.path =  'photos/'+filename
    notify(state, 'info', f'The text is: {state.path}')


def submit_scenario(state):
    notify(state, 'info', f'The text is: {state.content}')

    state.scenario.input_contact.write(state.input_contact)
    state.scenario.input_item_type.write(state.input_item_type)
    state.scenario.input_date.write(state.input_date)
    state.scenario.input_where.write(state.input_where)
    state.scenario.input_lost_or_found.write(state.input_lost_or_found)
    state.scenario.input_how.write(state.input_how)
    state.scenario.path.write(state.path)
    #state.scenario.input_circle_account.write(state.input_circle_account)


    state.scenario.submit(wait=True)
    state.message = scenario.message.read()



def build_message(phone:str ,item:str, when,  where :str, lost_or_found : str , how : str  , image : str):
    

    collection.insert_one({"contact":phone, "item": item ,"when": str(when) ,"where": where , 
                "lost_or_found" : lost_or_found , "how":how , "image" : image ,
                "plot_embedding_hf": generate_text_embedding(how) ,
                "plot_image_embedding_hf": generate_image_embedding(image)})
    return f"{item}"
    


def search_text_scenario(state):
    notify(state, 'info', f'Searching By Text....')

    state.scenario_search.item_name.write(state.item_name)
    state.scenario_search.submit(wait=True)
    state.results_item = scenario_search.results_item.read()

    partial = ''
    for index in range(0, len(dict_for_searchByText) , 4):
        partial+="<|"+dict_for_searchByText[index]+"|image|>"
        partial+="<|"+dict_for_searchByText[index+1]+"|button|>"
        partial+="<|"+dict_for_searchByText[index+2]+"|button|class_name=plain|>"
        partial+="<|"+dict_for_searchByText[index+3]+"|button|class_name=secondary|>"


    state.dynamic_content.update_content(state, partial)



def build_search_text_results(keyword: str):

    results = searchItemByText(keyword)
    output = ""

    for document in results:
        dict_for_searchByText.append(document["image"])
        dict_for_searchByText.append(document["contact"])
        dict_for_searchByText.append(document["lost_or_found"])        
        dict_for_searchByText.append(document["where"])


    return f"{output}"



def submit_search_image_scenario(state):
    #image_item_name = ''
    #searched_image_content = ''
    #image_results_item=''

    filename = state.searched_image_content[5:]
    shutil.move(state.searched_image_content, 'photos/'+ filename)
    state.searched_image_content = 'photos/'+filename


    notify(state, 'info', f'The image search begun {state.searched_image_content}')

    state.image_item_path = state.searched_image_content
    state.scenario_search_image.searched_image_content.write(state.searched_image_content)
    state.scenario_search_image.image_item_path.write(state.image_item_path)
    state.scenario_search_image.submit(wait=True)



    partialImage = ''
    for index in range(0, len(dict_for_searchByImage) , 4):
        partialImage+="<|"+dict_for_searchByImage[index]+"|image|>"
        partialImage+="<|"+dict_for_searchByImage[index+1]+"|button|>"
        partialImage+="<|"+dict_for_searchByImage[index+2]+"|button|class_name=plain|>"
        partialImage+="<|"+dict_for_searchByImage[index+3]+"|button|class_name=secondary|>"


    state.dynamic_content_image.update_content(state, partialImage)



def build_search_image_results(imagePath: str , displayImagePath: str ):
    print(imagePath)
    print(displayImagePath)

    results = searchItemByImage(imagePath)
    output = ""

    for document in results:
        dict_for_searchByImage.append(document["image"])
        dict_for_searchByImage.append(document["contact"])
        dict_for_searchByImage.append(document["lost_or_found"])
        dict_for_searchByImage.append(document["where"])


    print(dict_for_searchByImage)

    return f"{output}"    



#configure request submit
input_contact_data_node_cfg = Config.configure_data_node(id="input_contact")
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
                                            input=[input_contact_data_node_cfg,
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
searched_image_content_data_node_cfg = Config.configure_data_node(id="searched_image_content")
image_item_path_data_node_cfg = Config.configure_data_node(id="image_item_path")
image_results_item_data_node_cfg = Config.configure_data_node(id ="image_results_item")
build_image_search_task_cfg = Config.configure_task(id="build_image_search",function=build_search_image_results,input=[image_item_path_data_node_cfg,searched_image_content_data_node_cfg ],output = image_results_item_data_node_cfg)
image_search_scenario_cfg = Config.configure_scenario("scenario_search_image", task_configs=[build_image_search_task_cfg])




pages = {"/": "<|navbar|>",
         'items': itemsPage,
         'Register':form_md,
         'SearchByText':semanticSearchByText,
         'SearchByImage': semanticSearchByImage 

}


if __name__ == "__main__":
    Core().run()
    scenario = tp.create_scenario(scenario_cfg)
    scenario_search = tp.create_scenario(text_search_scenario_cfg)
    scenario_search_image = tp.create_scenario(image_search_scenario_cfg)
    gui = Gui(pages = pages)
    dynamic_content = gui.add_partial('')
    dynamic_content_image = gui.add_partial('')
    gui.run()


"""
button adds "" <-xters

image upload, ajax -->reflect db changes , file upload ,

aDDING ELEMENTS TO DB DORES NOT REFRECT N PAGE UNLESS WE RELOAD THE SERVER, NOT PAGE , SERVER

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

input nums

markdown vs page builder

date input breaks lines
search on enter key

cANT RELOAD SERVER FROM APP


INPUT FORM DOES NOT RESET AFTER SUBMITTIING


geting started  is mixed up

add element not working on button click

logging does not have line #


Generate csv on fly

enter on auto fill not working

opening on new tap , reuse prev tab

Taipy homepage wasn't made from Taipy


theme change

mongodb vector must me done manually or just do it on button click from atlas

"""


"""
Google Cloud , service account key

mongodb close brackets (python search query) error on this link - > https://www.mongodb.com/library/vector-search/building-generative-ai-applications-using-mongodb?lb-mode=overlay
"""


