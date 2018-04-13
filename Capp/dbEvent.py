from Capp import *



@socketio.on('dbEvent', namespace='/chat')
def dbEvent(message):
    friend_requist = Friendlist.query.filter(and_(Friendlist.email_users_friend == session['email'],
                                Friendlist.accept == None)).with_entities(
                                Friendlist.email_users, Friendlist.id).first()
    if friend_requist != None:
        session['friend_id'] = friend_requist[1]
        print('send to',session['email'] )

        # checken of de vriend online is of niet.
        if clients_ids[friend_requist[0]]  :
            clients_ids[session['email']].emit('Show_friend_request_notafication',
             {'data' :friend_requist[0], 'online': '#428bca'})
        else:
            user = User.query.filter_by(email = friend_requist[0]).first()
            if user.login_session == 'online':
                clients_ids[session['email']].emit('Show_friend_request_notafication',
                             {'data' :friend_requist[0], 'online': '#428bca'})
            else:
                clients_ids[session['email']].emit('Show_friend_request_notafication',
                 {'data' :friend_requist[0], 'online': 'red'})







@socketio.on('dbEventUpdate', namespace='/chat')
def dbEventUpdate(message):
    print(message)


    if clients_ids[message['email_user']] :
        print(message['email_user'], ': is gelukkig online ')
        clients_ids[message['email_user']].emit('friend_request_ans',
            {'data' :session['email'], 'ans': message['data']})

    if message['data'] == 'OK!':
        FL = Friendlist.query.get(session['friend_id'])
        FL.accept = True
        db.session.commit()
    else:
        Friendlist.query.filter_by(id=session['friend_id']).delete()
        db.session.commit()




@socketio.on('friend_request', namespace='/chat')
def friend_request(message):
    friend = message['friend']
    user = User.query.get(session['user_id'])
    user.new_friend(friend)
    if clients_ids[friend] != []:
        print('nu moeten we hem meteen even effen acceptatie steure')
    else:
        print('niet online')
