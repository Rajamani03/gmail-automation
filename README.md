
# Gmail Automation

This is a python script to automate emails in gmail to perform some actions on some predefined conditions

## Reference for gmail api python client

https://developers.google.com/gmail/api/quickstart/python

## Steps to run the script

- Enable your gmail api using the above docs
- Install these packages
  
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install mysql-connector-python
```

- Replace your mysql passowrd in main.py
- Paste your credentials.json in the same directory
- Check and modify rules.json as you wish
- Now open the terminal run the main.py

```bash
python main.py
```
