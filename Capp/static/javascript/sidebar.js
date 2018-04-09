var friend_list = {};
var notification ;
var socket ;

document.addEventListener('DOMContentLoaded', function() {
  namespace = '/chat'
  document.querySelector('#chat_scherm').style.visibility = 'hidden';


  socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
  socket.on('connect', function() {

       socket.emit('my_event', {"data": 'I\'m connected! side bar'});


   });




   // alles niet zichtbaar maken aanpassen voor shit uit database
   //document.querySelectorAll('.notification_circle').forEach(function(circle) {
     //circle.style.visibility = 'hidden';

   //})


  document.querySelectorAll('.friend_list').forEach(function(friend) {
    // kan  evuntiel nog data ophalen uit de database  voor ofline berichten
    friend_list[friend.dataset.friend] = 0 ;

    friend.onclick = function () {
      document.querySelector('#friend_email').innerHTML = friend.dataset.friend;

      socket.emit('open_chat', {'friend' : friend.dataset.friend})
    }

  });

  socket.on('noificatie', function(msg) {
    friend_list[msg.frind_notification] ++;

    notification = document.getElementsByClassName(`${msg.frind_notification}`)
    notification[0].innerHTML = friend_list[msg.frind_notification];

    notification[0].style.visibility = 'visible';
    //email_user_id

   });

});
