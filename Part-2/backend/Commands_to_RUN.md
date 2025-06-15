## Instructions to run 
1. Navigate to the bellow folder
- cd Part-2/backend
2. create a virtual environment
- conda create -p venv python=3.12 -y
3. Activate the environment
- conda activate
4. Install the requirements
- pip install -r requirements.txt
5. Run the fast API app
- uvicorn main:app --host 0.0.0.0 --port 8000 --reload
6. From the bellow link you can find the swagger documentation
- http://127.0.0.1:8000/docs#/
