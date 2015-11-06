import sys
import os
import healthgraph
import pymongo
import json

import configDAO
import runkeeperUserDAO
		

def main(argv=None):
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    database = connection.runkeeper
	
    confDB = configDAO.ConfigDAO(database)
    
    access_token = confDB.get_access_token()
    
    if access_token is not None:
        user = healthgraph.User(session=healthgraph.Session(access_token))
        act_iter = user.get_fitness_activity_iter()
        activities = []
        for activity in act_iter:
            activities.append(activity)

        runkeeperDB = runkeeperUserDAO.RunkeeperUserDAO(database)
        runkeeperDB.save_activities(activities)
    else:
        print 'Eror: no access token'

    
    
    
    
    
if __name__ == "__main__":
    sys.exit(main())