##########################################
#         Abiquo Events Notifier         #
##########################################

1. Introduction

Python script that monitors Abiquo Database and notifies new events based on rules.
Rules are stored in a SQLite database, which is queried by Notifier.

2. Configuration

    * Edit notifier.cfg and put correct values.
    
    * Grant access to the Abiquo MySQL
    
        # mysql kinton
        > GRANT select ON kinton.* TO 'root'@'events-notifier-server-ip';

3. Basic example

    * Init rules db

        # ./init_rules.py

    * Create a rule that monitor VAPP_CREATE and VAPP_DELETE actions performed by user mmorata, and notify it to user sgirones. Note that sgirones must have a valid email.

        # ./add_rule.py --user sgirones --action VAPP_CREATE,VAPP_DELETE --owner mmorata

    * Verify rules are correctly created:

        # ./list_rules.py 

            --------------------------------------------------
            User: sgirones
            Actions: ['VAPP_CREATE', 'VAPP_DELETE']
            Owners: ['mmorata']
            --------------------------------------------------

    * Run the Events Notifier

        # ./main.py &
        
4. Final notes

    * Add rules while Notifier is running is ALLOWED. It will load rules every time it analizes events.
    * Valid actions are those listed by:
    
        # ./add_rule.py --list-actions
