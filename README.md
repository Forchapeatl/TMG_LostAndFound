# TMG_LostAndFound
TMG LostandFound is an online platform where people can turn in items they have found and search items that have been found.


## System Architecture
The system is build on Taipy , MongoDB and Google Clould.

![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/140e1f22-8858-4160-9170-a8cba9ea6bc2)

- Taipy :
  - Used Taipy's declarative syntax to create a form for users to submit lost item reports.
  - Captured details like item description, location, date of loss, and finder's contact information.
  - Implemented image upload functionality to allow users to attach photos of the lost item.
  - Created a search interface for users to find lost items based on various criteria, such as story similary and Image similarity.
  
- MongoDB Atlas:
    - Used Atlas Vector Search to enable semantic search capabilities for item descriptions and identification.
    - Allow users to search for lost items using natural language queries and pictures instead of relying solely on keywords.
    - Utilized the semantic similarity between photos , query terms and item descriptions to retrieve relevant results.

-  Google Cloud:
    -Utilized a  custom model to generate semantic embeddings for lost item descriptions and images.
    
![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/e72b2d55-512a-4cdd-b02a-02c8ff75fd62)

![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/72779cd1-4e2a-4c30-8179-43be3231a2e8)

![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/48b8ab7c-bbf7-4e08-b56b-bd6dec3c82bb)


![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/eebee505-6347-42e5-bbdc-7b93d8e96507)
