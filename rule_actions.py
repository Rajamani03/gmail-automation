import json
from rule import Rule
import email
from datetime import datetime 
from dateutil.relativedelta import relativedelta

def get_rule_list(file_name='rules.json'):
    with open(file_name, 'r') as f:
        rule_list = json.load(f)

    all_rules = []
    for rule in rule_list:
        all_rules.append(Rule(rule))

    return all_rules
       
def does_condition_match(email, conditions, match_case):
    for condition in conditions:
        email_field_value = ""
        match condition.field_name:
            case "from":
                email_field_value = email.from_id
            case "subject":
                email_field_value = email.subject
            case "received date/time":
                email_field_value = email.received_date
            case "message":
                email_field_value = email.message
            case _:
                raise ValueError("Field name should be 'from' or 'subject' or 'received date/time' or 'message'")
       
        result = False
        current_date = datetime.now()
        match condition.predicate:
            case "contains":
                result = (condition.value in email_field_value)
            case "does not contain":
                result = (condition.value not in email_field_value)
            case "equals":
                result = (condition.value == email_field_value)
            case "does not equal":
                result = (condition.value != email_field_value)
            case "less than for days":
                delta = relativedelta(days=int(condition.value))
                result = ((current_date - delta) < email_field_value)
            case "greater than for days":
                delta = relativedelta(days=int(condition.value))
                result = ((current_date - delta) > email_field_value)
            case "less than for months":
                delta = relativedelta(months=int(condition.value))
                result = ((current_date - delta) < email_field_value)
            case "greater than for months":
                delta = relativedelta(months=int(condition.value))
                result = ((current_date - delta) > email_field_value)
            case _:
                raise ValueError("Predicate should be 'contains' or 'does not contain' or 'equals' or 'does not equal'")
            
        if match_case == 'any' and result:
            return True
        elif match_case == 'all' and not result:
            return False 

    if match_case == 'any':
        return False
    elif match_case == 'all':
        return True  
    else:
        raise ValueError("Match should be either any or all")

def rule_action(rule_list, emails):
    actions = {"mark_as_read": [], "mark_as_unread": [], "move_message": []}
    for rule in rule_list:
        for email in emails:
            email_match = does_condition_match(email, rule.conditions, rule.match_rule)
            if not email_match:
                continue
            for rule_action in rule.actions:
                match rule_action.action:
                    case "mark as read":
                        actions["mark_as_read"].append(email.message_id)
                    case "mark as unread":
                        actions["mark_as_unread"].append(email.message_id)
                    case "move message":
                        actions["move_message"].append((email.message_id, rule_action.move_to))
                    case _:
                        raise ValueError("Field name should be 'mark as read' or 'mark as unread' or 'move message'")

    return actions

def perform_actions(email_api, actions):
    for message_id in actions["mark_as_read"]:
        email_api.mark_as_read(message_id)
    for message_id in actions["mark_as_unread"]:
        email_api.mark_as_unread(message_id)
    for message_data in actions["move_message"]:
        email_api.move_email(message_data[0], message_data[1])
    