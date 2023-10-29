## Overview 
### This repository contains a multi-threaded sender and reader software system designed to interact with multiple PostgreSQL database servers simultaneously. It enables users to send and read messages in a distributed environment.

## Sender and Reader files
### **Sender.py**: This script allows users to input messages, which are then randomly assigned to one of the available database connections. Each message, along with the sender's information and timestamp, is stored in the ASYNC_MESSAGES table in the random PostgreSQL database. 
### **Reader.py**:  This script reads messages from the ASYNC_MESSAGES table in all databases that haven't been marked as received. It displays the sender's information, message content, and timestamp. After displaying the message, it updates the corresponding row with the current time.

## db_config.json
### The db_config.json file is used to store credentials of distributed database connections. Users need to desired PostgreSQL database credentials, such as the database name, username, password, host, and port, in this file. Example:
```json
{
    "database": "example_database_name",
    "user": "example_username",
    "password": "example_password",
    "host": "example_host",
    "port": "example_port"
}
```

## Installation and setup
### 1. Clone repository to your folder
```bash
git clone https://github.com/ADA-GWU/processes-and-asynchronous-messaging-Kenwoll.git
```

### 2. Create virtual environment 
```bash
python3 -m venv <env_name>
```

### 3. Activate virtual 
For Linux/Mac
```bash
source <env_name>/bin/activate
```

For Windows
```bash
<env_name>\Scripts\activate
```

### 4. If you dont have pip then install it. You find more information [here](https://www.partitionwizard.com/partitionmanager/install-pip.html)


### 5. Install required packages 

```bash
pip install -r requirements.txt
```

### 6. Run sender and reader files in seperate terminals

```bash
python3 sender.py
```

```bash
python3 reader.py
```