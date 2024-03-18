
# Gmail Automation

This is a python script to automate emails in gmail to perform some actions on some predefined conditions

## Reference for gmail api python client

<https://developers.google.com/gmail/api/quickstart/python>

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

## Guide to use rules.json

- rules.json is array of rules and each rule have condition that should match to perform the action provided
- A Rule 3 main parameters
  - match
  - conditions
  - actions
- Match is used to tell whether all the condition in conditions match or any condition can match
- Match should be 'Any' or 'All'
- Conditions array of hash which have field_name, predicate and value
- Field names should be 'Subject', 'From', 'Received date/time' or 'Message'
- Predicate should be 'contains', 'does not contain', 'equals', 'does not equal', 'less than for days', 'greater than for days', 'less than for months' or 'greater than for months'
- Value can be any string to relate with field name using predicate
- Actions are array of hash which have action and move to
- Action should have 'mark as read', 'mark as unread' or 'move message'
- If move message action is used then populate the move_to key with any destination label
