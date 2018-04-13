from Capp import app
from Capp import socketio
from Capp import *

# new bericht afhandelen


@app.route('/home', methods = ['GET', "POST"])
@login_required
def home():
    friendList = Friendlist.query.filter(and_(Friendlist.email_users == session['email'],
     Friendlist.accept == True)).with_entities(Friendlist.email_users_friend, Friendlist.id).all()
    friendList_rev = Friendlist.query.filter(and_(Friendlist.email_users_friend == session['email'],
     Friendlist.accept == True)).with_entities(Friendlist.email_users, Friendlist.id).all()
    lijst = [i[0] for i in (friendList+friendList_rev)]
    friends = Friendlist.query.filter(or_(Friendlist.email_users == session['email'],
                                    Friendlist.email_users_friend ==session['email']
                                            )).all()
    ## ophalen van het aantal
    # ophalen van het aantal ongelezen berichtenniet gelezen berichten.
    mes_dic = defaultdict()
    for friend in friends:
        count = 0
        for chat in friend.chats:
            if chat.see_flag == 'no' and chat.users_receiver == session['email']:
                count= count +1
            email_users = chat.users_send
            try:
                mes_dic[email_users] = count
            except UnboundLocalError:
                print('no conversation pressent in the DB')

    users = User.query.filter(User.email.in_(lijst)).all()
    dataFriend = []

    for i in users:
        try:
            mes_dic[i.email]
        except KeyError:
            mes_dic[i.email] = 0

        if i.login_session == 'online':
            color = '#428bca'
        else:
            color = 'red'

        dataFriend.append({'email_friend': i.email, 'status': color})

    ##### ophalen van niet bevrienden mensen
    users = User.query.all()
    friend = Friendlist.query.filter(and_(or_(Friendlist.email_users == session['email'],
                                    Friendlist.email_users_friend ==session['email']
                                    )), or_(Friendlist.accept == True, Friendlist.accept == None)).with_entities(Friendlist.email_users,
                                        Friendlist.email_users_friend).all()
    friend = [i[0] if i[0] != session['email'] else i[1] for i in friend]
    friend.append(session['email'])
    usersList = []
    for i in users:
        if i.email not in friend:
            usersList.append(i.email)


    ######## ophalen van mensen die nog moeten accepteren #########
    waiting_list = []
    friend_waiting = Friendlist.query.filter(and_(Friendlist.email_users == session['email']
    ),Friendlist.accept == None).with_entities(Friendlist.email_users_friend).all()
    for i in friend_waiting:
        waiting_list.append(i[0])
        print('kakakakaka', i[0])
    print('kkkkk ', waiting_list)
    return render_template('home.html', email=session['email'],
    friendList=dataFriend, mes_dic =mes_dic, usersList = usersList,
    waiting_list = waiting_list)

@app.route("/", methods = ['GET', "POST"])
def index():
    if session.get('email') == None:
        return redirect(url_for('login'))
    return redirect(url_for('home'))


@app.route('/login', methods=['GET' , 'POST'])
def login():
    session['current_room'] = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        print('wat is de user wat ', )
        if user != None and  user.is_correct_password(password):
            print('Logged in..')
            user.login_session = 'online'
            db.session.commit()
            login_user(user)
            session['email'] = email
            session['user'] = user
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            return abort(401)
    else:
        return render_template('login.html')


@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        new_user = User(email , password, 'offline' )
        db.session.add(new_user)
        db.session.commit()
        return Response("Registered Successfully")
    else:
        return render_template('registration.html')



@app.route('/friend', methods=['GET' , 'POST'])
@login_required
def friend():
    if request.method == 'POST':
        # add friend to the database.
        choose = request.form['checkbox']
        user = User.query.filter_by(email=session['email']).first()
        print(user.email)
        user.new_friend(choose)
        return redirect(url_for('home'))
    else:
        users = User.query.all()
        friend = Friendlist.query.filter(and_(or_(Friendlist.email_users == session['email'],
                                        Friendlist.email_users_friend ==session['email']
                                        )), or_(Friendlist.accept == True, Friendlist.accept == None)).with_entities(Friendlist.email_users,
                                         Friendlist.email_users_friend).all()
        friend = [i[0] if i[0] != session['email'] else i[1] for i in friend]
        usersList = []
        for i in users:
            if i.email not in friend:
                usersList.append(i)
        return render_template("friend.html", session=session, users=usersList)

@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.login_session = 'offline'
    db.session.commit()
    logout_user()
    if session['current_room'] != None:
        room_list[session['current_room']].remove(session['email']);
    try:
        del clients_ids[session['email']]
    except KeyError:
        pass
    for key in session.keys():
        session.pop(key)



    return redirect(url_for('login'))



@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    print('Wat is de user ID', user_id)
    return User.query.get(user_id)
