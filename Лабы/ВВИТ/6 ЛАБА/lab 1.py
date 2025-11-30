class UserAccount:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.__password = password
    
    def set_password(self, old_password, new_password):
        if self.__password == old_password:
            self.__password = new_password
            return True
        return False
    
    def check_password(self, password):
        if self.__password == password:
            return True
        return False
    
Me = UserAccount("DYF", "me@dyf.com", "1234")
print(Me.set_password("1234", "0987"))
print(Me.check_password("1234"))