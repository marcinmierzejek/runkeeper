

class ConfigDAO:

    def __init__(self, database):
        self.db = database
        self.sessions = database.sessions

        
    # returns configuration data or None
    def get_config(self):
        config = self.db.config.find_one()
        return config

    # will save access token from the webpage
    def save_access_token(self, new_access_token):
        try:
            self.db.token.delete_many({})
            self.db.token.insert({'token': new_access_token})
        except Exception as e:
            print e
            raise
    
    # will save access token from the webpage
    def get_access_token(self):
        try:
            token = self.db.token.find_one()
            return token
        except Exception as e:
            print e
            return None
    
    
    # get access token
    def get_access_token(self):
        token = self.db.token.find_one()
        return token['token']


        # if session_id is None:
            # return

        # self.sessions.remove_one({'_id': session_id})

        # return

    