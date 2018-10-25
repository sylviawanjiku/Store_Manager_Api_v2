import re

class Validators:
    def validate_username(self,username):
        """validate username"""
        return re.match("^[a-zA-Z]+$", username)

    def validate_password(self,password):
        """validate password"""
        return re.match("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[a-zA-Z0-9]{8,15}$", password)

    def validate_email(self,email):
        """validate email"""
        return re.match("^[^@]+@[^@]+\.[^@]+$", email)
 
    def validate_inputs(self, string_inputs):
        """ validate for inputs """
        return re.match("^[a-zA-Z0-9-\._@ `]+$", string_inputs)
