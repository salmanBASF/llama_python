# Install Packages from `requirements.txt` 

1. **Navigate to the Project Directory:**
   - Open Command Prompt (not Powershell !) and navigate to the directory where your Python project is located.
   - Use the `cd` command to navigate to the directory where your Python script `<file>.py` is located or simply use the terminal in the Visual Studio Code.


2. **Activate the Virtual Environment (Recommended):**
   - Virtual environments in Python are used to create isolated environments for Python projects, allowing you to manage dependencies and packages separately for each project.
   - Activate it using the following command:
     ```
     venv\Scripts\activate
     ```

3. **Install Packages from `requirements.txt`:**
   - Use `pip` to install the packages listed in the `requirements.txt` file:
     ```
     pip install -r requirements.txt
     ```

4. **Verify Package Installation:**
   - Check that the required packages are installed correctly:
     ```
     pip list
     ```

5. **Run Python Scripts:**
   - You can now run your Python scripts using the installed packages:
     ```
     python main.py
     ```

