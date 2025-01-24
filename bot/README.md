# Bot server

Core service. Process inbound messages:
- Sends to a LLM asking for extracting expense details
- Sends back a response about the expense processed
- Keeps track of the processed messages with their results for further audit process 

## Set up

### LLM

- This implementation uses Cohere model [details here](https://dashboard.cohere.com/). It offers a free tier enough for this challenge.

- Once you get registered, generates an API key and set it to the `.env` file.

### Server
For local code adjustments

- This project requires [Python](https://www.python.org/downloads/) version 3.10+ installation
- After installation. Optionally create a virtual env. Open a terminal and run

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install the project dependencies

```bash
pip install -r requirements.txt
```
