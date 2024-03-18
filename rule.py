class Rule:
    def __init__(self, rule_json={}):
        self.description = rule_json.get('description','')
        self.match_rule = rule_json.get('match','').lower().strip()
        self.conditions = [RuleCondition(rc) for rc in rule_json.get('conditions',[])]
        self.actions = [RuleAction(ra) for ra in rule_json.get('actions',[])]

class RuleCondition:
    def __init__(self, condition_json={}):
        self.field_name = condition_json.get('field_name','').lower().strip()
        self.predicate = condition_json.get('predicate','').lower().strip()
        self.value = condition_json.get('value','')

class RuleAction:
    def __init__(self, action_json={}):
        self.action = action_json.get('action','').lower().strip()
        self.move_to = action_json.get('move_to','').strip()

