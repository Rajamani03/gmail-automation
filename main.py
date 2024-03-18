from email_api import EmailAPI
from db_actions import connect_db, intialise_db, insert_email
import rule_actions

DB_PASS = "YOUR_PASSWORD"
EMAIL_LIMIT = 10

def main():
    email_api = EmailAPI()
    email_ids = email_api.get_all_emails()

    # limiting emails
    email_ids = email_ids[:EMAIL_LIMIT]

    # get all email data
    email_data = []
    for email_id in email_ids:
        email_data.append(email_api.get_email_data(email_id))

    # initialise db connection
    conn = connect_db("localhost", "root", DB_PASS)
    intialise_db(conn)

    # insert email data in db
    insert_email(conn, email_data)

    # get rule list from rules.json
    rule_list = rule_actions.get_rule_list()
    actions_to_perform = rule_actions.rule_action(rule_list, email_data)

    # perform actions on the emails that met the conditions
    rule_actions.perform_actions(email_api, actions_to_perform)
        
    conn.close()

if __name__ == "__main__":
  main()