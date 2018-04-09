from Capp import app
from Capp import socketio
from Capp import *

# new bericht afhandelen




@app.route('/home', methods = ['GET', "POST"])
@login_required
def home():
    if request.method == 'POST':
        message = request.form.get('message')
        print (request.form.get('message'))

    friendList = Friendlist.query.filter_by(email_users=session['email']).with_entities(Friendlist.email_users_friend, Friendlist.id).all()
    friendList_rev = Friendlist.query.filter_by(email_users_friend=session['email']).with_entities(Friendlist.email_users, Friendlist.id).all()
    return render_template('home.html', email=session['email'],friendList=friendList+friendList_rev)


@app.route("/", methods = ['GET', "POST"])
def index():
    if session.get('login') == None:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=['GET' , 'POST'])
def login():
    session['current_room'] = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        print('wat is de user wat ', user)
        if user != None and user.password == password:
            print('Logged in..')
            login_user(user)
            session['email'] = email
            return redirect(url_for('home'))
        else:
            return abort(401)
    else:
        print('waarom komje hier' )
        return render_template('login.html')


@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        new_user = User(email=email , password=password )
        db.session.add(new_user)
        db.session.commit()
        return Response("Registered Successfully")
    else:
        return render_template('registration.html')



@app.route('/friend', methods=['GET' , 'POST'])
@login_required
def friend():
    if request.method == 'POST':
        choose = request.form['checkbox']
        user = User.query.filter_by(email=session['email']).first()
        print(user.email)
        user.new_friend(choose)
        return redirect(url_for('home'))
    else:
        users = User.query.all()

        return render_template("friend.html", session=session, users=users)







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
