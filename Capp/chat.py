from Capp import *
from Capp.views import *

class Socket:
    def __init__(self, sid):
        self.sid = sid
        self.connected = True

    # Emits data to a socket's unique room
    def emit(self, event, data):
        emit(event, data, room=self.sid)




@socketio.on('open_chat', namespace='/chat')
def open_chat(message):
    user_email = session['email']
    # get email addres
    users_friend_email = message['friend']

    friend = Friendlist.query.filter(and_(Friendlist.email_users == session['email'],
                                Friendlist.email_users_friend ==users_friend_email)).first()
    if friend == None:
        friend = Friendlist.query.filter(and_(Friendlist.email_users == users_friend_email  ,
                                    Friendlist.email_users_friend == session['email'])).first()
    # opjecht voor het opslaan van
    friend_object[friend.id] = friend
    if session['current_room'] == None:
        ## er is een nieuwe room gemaakt
        session['current_room'] = friend.id
        join_room(friend.id, sid=None, namespace='/chat')
        room_list[session['current_room']].append(user_email)
        room_list[session['current_room']]=list(unique_everseen(room_list[session['current_room']]))

    elif  session['current_room'] != friend.id:
        leave_room(session['current_room'], sid=None, namespace='/chat')
        room_list[session['current_room']].remove(user_email);
        room_list[friend.id].append(user_email)
        # er wordt van chat scherm gewisseld
        session['current_room'] = friend.id
        room_list[session['current_room']]=list(unique_everseen(room_list[session['current_room']]))

        join_room(friend.id, sid=None, namespace='/chat')
    else:
        # twee gebruikers hebben elkaar gevonden
        pass

    # update the database dat het bericht is gezien
    chat = Chats.query.filter(and_(Chats.users_receiver == session['email'],
                            Chats.see_flag == 'no')).update(dict(see_flag='yes'))
    db.session.commit()

    print('in welke room ben ik', session['current_room'])
    message_list[session['current_room']] = []
    if message_list[session['current_room']] == []:
        # er is nog  geen conversatie plaats gevonden in deze chat in deze session
        chat_history= Chats.query.filter_by(id_Friendlist=session['current_room']).all()[-30:]
        for index, row in enumerate(chat_history):
            if index <= 30:
                message_list[session['current_room']].append({'data' : row.message, 'user' : row.users_send})
            else:
                break
        # test
        #Desmond1991@gmail.com
        from time import sleep
        clients_ids[session['email']].emit('excited_room', {'data' : message_list[session['current_room']]})
    else:
        pass
        # er is al met elkaar gesproken
        # alleen het verschill moet er bij , maar voor nu droppen we alles eerst
        clients_ids[session['email']].emit('excited_room', {'data' : message_list[session['current_room']]})
    # zorgen dat vorige chat geschidenis in geladen wordt

    #emit('new_message',
    #{'data' : message['data']})


# een noificatie  geven als iemand een nieuwe bericht heeft
def new_message_flag(user_send, friend_receive, current_room):
    print('welke vriend krijg  het bericht: ', friend_receive)
    if len(room_list[current_room]) == 1:
        # ontvanger zit in een adnere kamer.
        if clients_ids[friend_receive] != []:
            clients_ids[friend_receive].emit('noificatie', {'frind_notification' : session['email']})
            return 'no'
        else:
            # user is waarschijnlijk uitgelogt
            return 'no'
    elif len(room_list[current_room]) == 2:
        # ontvanger zit in de zelfde kamer.
        return 'yes'
    elif len(room_list[current_room]) > 2:
        # verwijderen van dubbelen mensen
        room_list[session['current_room']]=list(unique_everseen(room_list[session['current_room']]))



@socketio.on('send_message', namespace='/chat')
def send_message(message):
    flag = new_message_flag(session['email'], message['friend_email'], session['current_room'])
    message_list[session['current_room']].append({'data' : message['data'], 'user' : session['email']})
    ob = Friendlist.query.get(session['current_room'])
    ob.new_message(session['email'], message['friend_email'], message['data'], flag)
    # de 30 moet variable zijn
    x=1
    if len(message_list[session['current_room']]) >= x*30:
        message_list[session['current_room']] = message_list[session['current_room']][x*-29:  ]


    emit('new_message',
    {'data' : message['data'], 'user' : session['email']}, room = session['current_room'])


@socketio.on('connect', namespace='/chat')
def test_connect():
    print('we zijn verbonden')
    clients_ids[session['email']] = Socket(request.sid)

    emit('connect_all', {'data' : session['email']}, broadcast=True)


    #friend_requist = Friendlist.query.filter(and_(Friendlist.email_users_friend == session['email'],
    #                            Friendlist.accept == None)).with_entities(
    #                            Friendlist.email_users, Friendlist.id).first()



@socketio.on('logout_acion', namespace='/chat')
def logout(message):
    leave_room(session['current_room'], sid=None, namespace='/chat')
    print('Client is logging out!!!')
    emit('disconnect_all', {'data' : session['email']}, broadcast=True)
#when browser is close
@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    logout_user()
    print(session['email'])
    if session['current_room'] != None:
        leave_room(session['current_room'], sid=None, namespace='/chat')
        room_list[session['current_room']].remove(session['email']);
    #del clients_ids[session['email']]
    print('Client disconnected')
    emit('disconnect_all', {'data' : session['email']}, broadcast=True)
