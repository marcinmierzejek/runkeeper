import sys
import os
import bottle
import healthgraph
import pymongo
from beaker.middleware import SessionMiddleware

import configDAO
		
# Session Options
sessionOpts = {
    'session.type': 'file',
    'session.cookie_expires': 1800,
    'session.data_dir': '/tmp/cache/data',
    'session.lock_dir': '/tmp/cache/data',
    'session.auto': False,
}

confDB = ''
conf = {}

#consumer_key = '7439d8bf72704084b9c8e08153aa84a3'
#consumer_secret = 'ed8c4dd98cf7436eb2cd9bbb3c7c3a6b'

@bottle.route('/')
def index():
    access_token = confDB.get_access_token()
    sess = bottle.request.environ['beaker.session']
    
    if access_token is not None:
        sess['rk_access_token'] = access_token
        sess.save()
        bottle.redirect('/welcome')
    else:
        rk_auth_mgr = healthgraph.AuthManager(conf['client_id'], conf['client_secret'], 
                                              '/'.join((conf['baseurl'], 'login',)))
        rk_auth_uri = rk_auth_mgr.get_login_url()
        rk_button_img = rk_auth_mgr.get_login_button_url('blue', 'black', 300)
        return bottle.template('index.html', {'rk_button_img': rk_button_img,
                                              'rk_auth_uri': rk_auth_uri,})

@bottle.route('/login')
def login():
    sess = bottle.request.environ['beaker.session']
    code = bottle.request.query.get('code')
    if code is not None:
        rk_auth_mgr = healthgraph.AuthManager(conf['client_id'], conf['client_secret'], 
                                              '/'.join((conf['baseurl'], 'login',)))
        access_token = rk_auth_mgr.get_access_token(code)
        sess['rk_access_token'] = access_token
        sess.save()
        confDB.save_access_token(access_token)
        bottle.redirect('/view')
		
@bottle.route('/welcome')
def welcome():
    sess = bottle.request.environ['beaker.session']
    access_token = sess.get('rk_access_token')
    if access_token is not None:
        user = healthgraph.User(session=healthgraph.Session(access_token))
        profile = user.get_profile()
        records = user.get_records()
        act_iter = user.get_fitness_activity_iter()
        activities = [act_iter.next() for _ in range(10)]
        return bottle.template('welcome.html', 
                               profile=profile,
                               activities=activities, 
                               records=records.get_totals())
    else:
        bottle.redirect('/')	

@bottle.route('/view')
def view():
    sess = bottle.request.environ['beaker.session']
    access_token = sess.get('rk_access_token')
    if access_token is not None:
        remote_addr = bottle.request.get('REMOTE_ADDR')
        return bottle.template('access_token.html',
                               remote_addr=remote_addr,
                               access_token=(access_token 
                                             if remote_addr == '127.0.0.1'
                                             else None))
    else:
        bottle.redirect('/')


def main(argv=None):
    """Main Block - Configure and run the Bottle Web Server."""
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    database = connection.runkeeper
	
    global confDB
    confDB = configDAO.ConfigDAO(database)
    global conf
    conf = confDB.get_config()    

    app = SessionMiddleware(bottle.app(), sessionOpts)
    bottle.run(app=app, host=conf['bindaddr'], port=conf['bindport'])
    
if __name__ == "__main__":
    sys.exit(main())