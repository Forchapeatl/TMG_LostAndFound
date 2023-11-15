# TMG_LostAndFound
[TMG LostandFound](https://lostandfound.taipy.cloud) is a revolutionary online platform that utilizes cutting-edge semantic vector search to revolutionize the way lost items are found and claimed.
This platform significantly improves the efficiency of reuniting lost items with their owners, reducing frustration and saving time. It promotes a more connected and responsible community, fostering a sense of belonging and shared responsibility.



## System Architecture
The system is build on Taipy , MongoDB and Google Clould.

![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/140e1f22-8858-4160-9170-a8cba9ea6bc2)

- Taipy :
  - Used Taipy's declarative syntax to create a form for users to submit lost item reports.
  - Captured details like item description, location, date of loss, and finder's contact information.
  - Implemented image upload functionality to allow users to attach photos of the lost item.
  - Created a search interface for users to find lost items based on various criteria, such as story similary and Image recognition.
  
- MongoDB Atlas:
    - Used Atlas Vector Search to enable semantic search capabilities for item descriptions and image recognition.
    - Allow users to search for lost items using natural language queries and pictures instead of relying solely on keywords.
    - Utilized the semantic similarity between photos , query terms and item descriptions to retrieve relevant results.

-  Google Cloud:
    -Utilized a  custom model to generate semantic embeddings for lost item descriptions and images.


![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/eebee505-6347-42e5-bbdc-7b93d8e96507)

![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/e72b2d55-512a-4cdd-b02a-02c8ff75fd62)

![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/72779cd1-4e2a-4c30-8179-43be3231a2e8)

![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/48b8ab7c-bbf7-4e08-b56b-bd6dec3c82bb)

# TMG LostandFound installation guide:
## Install Taipy

Install Taipy: Install Taipy using the following command: 
```
pip install taipy
```

Verify Taipy Installation
```
pip show taipy
```

If you see the Taipy version information, it means that Taipy is installed successfully. Now you can start using Taipy to develop your online platform for managing lost and found items.

## Clone this repository and run the app

```
git clone https://github.com/Forchapeatl/TMG_LostAndFound.git
cd TMG_LostAndFound
pip install -r requirements.txt
taipy run main.py
```
##Prerequisites
- Get a mongoDB atlas connection string. Tutorial can be found [here](https://www.mongodb.com/basics/mongodb-atlas-tutorial)  

- Create a Google Cloud Platform service account key and subscribe to the Vertex AI API. The tutorial can be found [here](https://cloud.google.com/iam/docs/keys-create-delete)
  
Add your service key file to the root folder and replace the `'mongodb-403805-3cf96c2ad447.json` file name at line 27

[github.com/Forchapeatl/TMG_LostAndFound/blob/main/main.py?plain=1#L27
](https://github.com/Forchapeatl/TMG_LostAndFound/blob/11b3e53479a0c10c061415df16663300dab91527/main.py#L27)https://github.com/Forchapeatl/TMG_LostAndFound/blob/11b3e53479a0c10c061415df16663300dab91527/main.py#L27  



