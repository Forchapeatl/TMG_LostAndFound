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
  - Created a search interface for users to find lost items based on various criteria, such as story similary and Image similarity.
  
- MongoDB Atlas:
    - Used Atlas Vector Search to enable semantic search capabilities for item descriptions and identification.
    - Allow users to search for lost items using natural language queries and pictures instead of relying solely on keywords.
    - Utilized the semantic similarity between photos , query terms and item descriptions to retrieve relevant results.

-  Google Cloud:
    -Utilized a  custom model to generate semantic embeddings for lost item descriptions and images.


![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/eebee505-6347-42e5-bbdc-7b93d8e96507)

![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/e72b2d55-512a-4cdd-b02a-02c8ff75fd62)

![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/72779cd1-4e2a-4c30-8179-43be3231a2e8)

![image](https://github.com/Forchapeatl/TMG_LostAndFound/assets/24577149/48b8ab7c-bbf7-4e08-b56b-bd6dec3c82bb)

# TMG LostandFound installation guide:
## Creating a virtual environment
To create a virtual environment in Linux and download and install Taipy, follow these steps:

Install Python 3: Ensure you have Python 3 installed on your system. If not, install it using your system's package manager. For example, on Ubuntu or Debian, use the following command:
```sudo apt install python3```

Install virtualenv: Virtualenv is a tool for creating virtual environments in Python. Install it using the following command:
```pip install virtualenv```

Create a virtual environment: Create a directory for your project and create a virtual environment within that directory. For example, if your project is named "lost-and-found", use the following commands:

```
mkdir lost-and-found
cd lost-and-found
virtualenv venv

```
Activate the virtual environment: Activate the virtual environment using the following command:

```
source venv/bin/activate
```

## Install Taipy

    Install Taipy: Install Taipy using the following command:
    
    `pip install taipy`

Verify Taipy Installation

    `pip show taipy`

If you see the Taipy version information, it means that Taipy is installed successfully. Now you can start using Taipy to develop your online platform for managing lost and found items.

## Clone this repository




To have keys on Google Cloud Platform (GCP) to do Vertex AI projects, you can either create a service account key or use a personal access token.

- Creating a service account key

1. Go to the Google Cloud Console and navigate to the IAM & Admin > Service accounts page.
2. Click the "Create Service Account" button.
3. Enter a unique name for the service account and select a project for it.
4. Grant the service account the necessary roles to perform Vertex AI tasks. For example, the "Roles/aiplatform.developer" role allows the service account to create and manage Vertex AI resources.
5. Click the "Create" button to create the service account.
6. Click the "Keys" tab for the newly created service account.
7. Click the "Add key" button and select "Create new key".
8. Choose the key type (JSON or P12) and click the "Create" button.
9. Download the key file and store it securely.


