# SHARN Student Cloud
A Simple CTF Challenge that expects user to do SQL Injection Attack
## Requirements
Language Used = Python3<br />
Modules/Packages used:
* json
* hashlib
* flask
* mysql-connector-python
* random
* string
* colorama
<!-- -->
Install the dependencies:
```bash
pip install -r requirements.txt
```
## Solution
* Do SQL Injection on route /searchRoll (found in /search)
* After SQL Injection retrive USERS Table (Login Details)
* Login with User **kaptaan**
* Flag is there