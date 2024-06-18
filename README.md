# Developer agent with Flask FE Starter

## Introduction
Build out some UI / API to interact with our agent

## Prerequisites
Before you begin, ensure you have met the following requirements:
- You have installed Python 3.6+.

## Setup Instructions

### Step 1: Clone the Repository
First, clone the repository to your local machine using the following command:
```bash
git clone [repository-url]
cd [repository-name]
```

### Step 2: Create a Python Virtual Environment
Create a virtual environment using `venv`:
```bash
python3 -m venv venv
```

### Step 3: Activate the Virtual Environment
Activate the virtual environment:
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On MacOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### Step 4: Install Required Packages
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

### Step 5 option 1: Create a `.env` File
Create a `.env` file in the root directory of the project. Use the `.env.sample` file as a reference:
```bash
cp .env.sample .env
```
Open the `.env` file and update the key values as necessary.

### Step 5 option 2: Export the Variables Inside Your Environment
Run the environment setup script:
```bash
export OPENAI_API_KEY=[your-key-here]
export LANGCHAIN_API_KEY=[your-key-here]
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_PROJECT=default
```

## Usage

### Running the agent
```bash
python agent_code.py
```

### running the api
```bash 
python app.py
```