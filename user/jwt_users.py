class JWT_Users:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JWT_Users, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def initialize(self):
        if not self.initialized:
            self.jwt_users = dict()
            self.initialized = True

    def add_user(self, username, jwt):
        self.jwt_users[jwt] = username

    def find_user(self, jwt):
        if jwt not in self.jwt_users:
            return None
        return self.jwt_users[jwt]

