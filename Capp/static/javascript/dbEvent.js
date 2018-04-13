// globale variablen
var friend_list = {};
var notification ;
var socket ;
namespace = '/chat'
var timeIntervalDB = 5000




document.addEventListener('DOMContentLoaded', function() {
  // create the first Connection
  socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
  socket.on('connect', function() {
       socket.emit('my_event', {"data": 'I\'m connected! side bar'});


   });
   const ul = document.querySelector('#sidebar_nav');

   function creat_friend_element(name, online) {
     // maken van een nieuwe vriend in de vreinden lijst als er een request
     // binnen komt
     li = document.createElement("li");
     friend_list[name] = 0 ;

     li.setAttribute('id', 'liItem');
     li.setAttribute('class', 'dropdown class_new_users');

     a = document.createElement('a');
     a.setAttribute('id', name);
     a.setAttribute('class', 'ripple-effect dropdown-toggle friend_list ');
     a.setAttribute('data-friend', name);
     a.setAttribute('data-toggle', 'dropdown');
     span = document.createElement('span');
     span.setAttribute('class', 'glyphicon glyphicon-user icon');
     span.style.color = online;
     a.innerHTML = ` ${name}` ;
     a.insertBefore(span, a.childNodes[0]);
     div = document.createElement('div');
     div.setAttribute('class', `notification_circle ${name}`);
     div.style.visibility = 'hidden'
     div.innerHTML = 0;
     a.appendChild(div);
     a.onclick = function () {
       document.querySelector('#friend_email').innerHTML = name;
       socket.emit('open_chat', {'friend' : name})
     }
     li.appendChild(a);
     ul.appendChild(li);
   }

   dbevent = setInterval(function() {
      socket.emit('dbEvent', {"data": 'zijn er veranderinge in de database'});
   }, timeIntervalDB);

   socket.on('Show_friend_request_notafication', function(msg) {
     console.log(msg);
     clearInterval(dbevent);
     var txt;
     if (confirm(`${msg.data} want you to add!`)) {
       txt = "OK!";
       console.log('kanker', ul);
       creat_friend_element(msg.data, msg.online);


     } else {
       txt = "Cancel!";
     }

     socket.emit('dbEventUpdate', {"data": txt, 'email_user': msg.data});


     dbevent = setInterval(function() {
        socket.emit('dbEvent', {"data": 'zijn er veranderinge in de database'});
     }, timeIntervalDB);

    });





    socket.on('friend_request_ans', function(msg) {
      // terug koppeling naar de persoon die de request verzonden heeft
      document.querySelectorAll('.class_new_users_wait').forEach(function(class_user) {
        console.log(class_user);
        ul.removeChild(class_user);
        });
      if (msg.ans == "OK!"){
        alert(`${msg.data} friend request accepted!!!`);
        creat_friend_element(msg.data, '#428bca')
      }else {
        alert(`${msg.data}: friend request rejected!!!`);
      }




    });
});
