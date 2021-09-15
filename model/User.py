from model.UserRule import UserRule


class User:
    def __init__(self, chat_id, rules: [UserRule]):
        self.chat_id = chat_id
        self.rules = rules

    def add_rule(self, hour, minute, msg, name_rule) -> UserRule:
        rule = UserRule(hour, minute, msg, name_rule)
        self.rules.append(rule)
        return rule

    def exists_rule(self, name_rule):
        for elem in self.rules:
            if elem.name_rule == name_rule:
                return True
        return False

    def get_str_rules(self):
        s = ""
        for rule in self.rules:
            s += '\n-'+rule.name_rule + ' ' + rule.msg + ' at ' + str(rule.hour)+':'+str(rule.minute)
        return s