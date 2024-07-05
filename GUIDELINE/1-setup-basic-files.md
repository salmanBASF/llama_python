# First Setup: 

1. **Open Visual Studio Code:**
   - Launch Visual Studio Code on your system.

2. **Open Project Directory:**
   - Open the created project directory in Visual Studio Code.

3. **Create Data Folder:**
   - Inside the project directory, create a `data` folder to store data files.
     ```
     mkdir data
     ```

4. **Create .env File:**
   - Create a `.env` file in the project directory to store environment variables.
     - Add the necessary environment variables to the `.env` file.

     ```
     OPENAI_API_KEY=sk-proj-YJfIghXUvkuWwAZOgAVcT3BlbkFJSboe6GLdcYRb9AdsIqW3
     ```

5. **Create main.py:**
   - Create a `main.py` Python script in the project directory as the main entry point for the project.


6. **Create requirements.txt:**
   - Create a `requirements.txt` file in the project directory to list project dependencies.
     - Add the required Python packages and their versions to the `requirements.txt` file.

    ```
        llama-index==0.10.*
        python-dotenv==1.*
        chromadb
        llama-index-vector-stores-chroma
    ```
