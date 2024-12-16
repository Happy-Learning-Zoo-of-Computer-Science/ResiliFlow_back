# ResiliFlow backend service

## Description
This is the backend service of ResiliFlow.

## Installation

1. Clone the repository: 
    ```sh
    git clone https://github.com/Happy-Learning-Zoo-of-Computer-Science/ResiliFlow_back.git
    cd resiliflow_back
    ```

2. Install dependencies:
    ```sh
    # Python version 3.12.1
    # Use virtual environment if you want.
    pip install requirements.txt
    ```

3. Start backend service:
    ```sh
    python app.py
    ```

## Test

### Unit test
1. Clone the repository and install dependencies.
2. Direct to the project folder.
3. Run unit tests:
    ```sh
    python -m unittest discover -v -s test -p test_*.py
    ```
4. If the test fails, please check is port 5000 occupied.

## Structure
* /app/\__init\__.py: initialize Flask application.
* /app/routes: API routes
* /app/services: API logic
* run.py: main function.