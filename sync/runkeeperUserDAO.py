

class RunkeeperUserDAO:

    def __init__(self, database):
        self.db = database
        self.sessions = database.sessions
   
    # will save access token from the webpage
    def save_activities(self, activities):
        try:
            for activity in activities:
                #print str(activity['start_time']) + '\t' + str(activity['type']) + '\t' + str(activity['duration']) + '\t' + str(activity['total_distance']) + '\t' + str(activity['total_calories'])
                self.db.activities.insert(activity)
        except Exception as e:
            print e
            raise
    
