



document.addEventListener('DOMContentLoaded', function() {



  namespace = '/chat';
  // ophalen van de gebruikers email adderes. meschien even ombouweden naar
  // request naar de server
  const email_user = document.querySelector('#email_user_id').innerHTML;
  // body...

// test of er connection is onstaan
  socket.on('my_response', function(msg) {
    document.querySelector('#log').innerHTML = `hebben wat: ${msg.data}`;
   });




   // maak een leeg new chat scherm aan
   socket.on('new_room', function(msg) {
     console.log('we moeten een new chat scherm maken');
     var panel_body = document.querySelector('#panel_body');
     while (panel_body.firstChild) {
       panel_body.removeChild(panel_body.firstChild);
     }
    document.querySelector('#chat_scherm').style.visibility = 'visible';
     //document.querySelector('#panel_body').innerHTML = '';

   });

   //het inladen van bestaan gespreken
   socket.on('excited_room_test', function(msg) {
     Array_msg = Object.values(msg);
     console.log(Array_msg);
     alert("geen print")
    });

   //het inladen van bestaan gespreken
   socket.on('excited_room', function(msg) {

     Array_msg = Object.values(msg);
     // dit moet verandert worden
     var panel_body = document.querySelector('#panel_body');

     while (panel_body.firstChild) {
       panel_body.removeChild(panel_body.firstChild);
     }

      Array_msg[0].forEach(function (message) {
        const div  = document.createElement('div');
        const blockquote = document.createElement('blockquote');
        div.className = "clearfix";
        blockquote.className = (message.user == email_user) ? 'me pull-right' : 'you pull-left';
        blockquote.innerHTML = `${message.data}`;
        div.appendChild(blockquote);
        document.querySelector('#panel_body').append(div);


      });
      var var_friend_email = document.querySelector('#friend_email').innerHTML;
      notification = document.getElementsByClassName(`${var_friend_email  }`)
      friend_list[msg.frind_notification] = 0;
      notification[0].style.visibility = 'hidden';
      // naar bendeden halen van het chat scherm
      var myChatBox = document.getElementById("panel_body");
      myChatBox.scrollTop = myChatBox.scrollHeight;

      document.querySelector('#chat_scherm').style.visibility = 'visible';
    });


   // ontvang een nieuw bericht en verwerkt op de html pagina
   socket.on('new_message', function(msg) {
     console.log(`ontvang een bericht: ${msg.data}`);
     const div  = document.createElement('div');
     const blockquote = document.createElement('blockquote');
     div.className = "clearfix";
     blockquote.className = (msg.user == email_user) ? 'me pull-right' : 'you pull-left';

     blockquote.innerHTML = `${msg.data}`;
     div.appendChild(blockquote);
     document.querySelector('#panel_body').append(div);
     var myChatBox = document.getElementById("panel_body");
     myChatBox.scrollTop = myChatBox.scrollHeight;

    });

    //

    // noificatie voor user specefieke GEBRUIKER




    // send een new bericht naar de webserver
   document.querySelector('#sendsubmit').disabled = true;

   document.querySelector('#message').onkeyup = function () {
     if (document.querySelector('#message').value.length > 0){
       document.querySelector('#sendsubmit').disabled = false;
     }else {
       document.querySelector('#sendsubmit').disabled = true;
     }
   };

   document.querySelector('#sendform').onsubmit = function () {
     message = document.querySelector('#message').value;
     var var_friend_email = document.querySelector('#friend_email').innerHTML;
     socket.emit('send_message', {"data" : message, 'friend_email' : var_friend_email});
     document.querySelector('#message').value = '';
     document.querySelector('#sendsubmit').disabled = true;
     return false;


   };



});
