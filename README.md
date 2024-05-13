## How to run project


# step:1. Virtual Environment

## on Ubuntu
### Install python3
- sudo add-apt-repository ppa:deadsnakes/ppa
- sudo apt install python3.11

- sudo apt-get install python3-pip
- sudo pip3 install virtualenv
- virtualenv venv
- virtualenv --python python3 venv
- source venv/bin/activate

## On Unix/Linux/macOS
- python3 -m venv venv
- source venv/bin/activate

## On Windows
- python -m venv venv or py -m venv venv
- venv\Scripts\activate

# step:2. Install dependencies
- pip install -r requirements.txt

# step:3 Running the Project
- py main.py