# ------------------------------------------------------------------
# State machine testing the UserDB class
#
# Pedro Vasconcelos, 2025
# ------------------------------------------------------------------
from userdb import UserDB
from hypothesis import assume, event, settings, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, \
    rule, precondition


class UserDBStateMachine(RuleBasedStateMachine):    
    def __init__(self):
        super().__init__()
        self.db = UserDB()
        self.model = []  # empty table

    def teardown(self):
        self.db.close()

    users = st.integers(min_value=1, max_value=10)
    emails = st.emails()
        
    @rule(user=users, email=emails)
    def add(self, user, email):
        # --- implementation ---
        self.db.add(user, email)
        # --- model ---
        if (user,email) not in self.model:
            self.model.append((user,email))

    @rule(user=users)
    def get(self, user):
        # --- implementation
        answer = self.db.get(user)
        # --- model
        expect = [email for (other,email) in self.model
                  if other==user]
        # -- postcondition        
        assert answer == expect

    @precondition(lambda self: self.model != [])
    @rule(user=users, email=emails)
    def remove(self, user, email):
        # --- precondition
        assume((user,email) in self.model)
        # --- implementation
        self.db.remove(user,email)
        # --- model
        self.model.remove((user,email))
        
    @rule(user=users)
    def delete(self,user):
        # --- implementation
        self.db.delete(user)
        # --- model
        self.model = [(other,email) for (other,email)
                      in self.model if other!=user]

Test = UserDBStateMachine.TestCase
