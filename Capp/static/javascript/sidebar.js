
document.addEventListener('DOMContentLoaded', function() {
  const ul = document.querySelector('#sidebar_nav');


  document.querySelector('#chat_scherm').style.visibility = 'hidden';
   document.querySelector('#logout').onclick = function () {
     console.log('kanker ik moet hier komen');
     socket.emit('logout_acion', {'data': "logingOUt"});

   };





   // maken van de scheiding tussen de nieuwe en ousen
   function new_user_sep() {
     var li_show = document.createElement("li");
     id = 'show_new_users';
     li_show.setAttribute('id', id);
     li_show.setAttribute('class',"divider");
     li_show.setAttribute('role',"separator");
     a = document.createElement('a');
     a.innerHTML = 'add new user';
     a.style.color = "#595959";
     li_show.appendChild(a);
     ul.appendChild(li_show);
     return li_show;
   }
   // alles niet zichtbaar maken aanpassen voor shit uit database
   //document.querySelectorAll('.notification_circle').forEach(function(circle) {
     //circle.style.visibility = 'hidden';

   //})

   // user tonen die nog niet bevriend zijn met de gebruiker
   function new_user(li_show) {
     a = [];
     for (index = 0; index < new_users.length; ++index) {
       li = document.createElement("li");

       li.setAttribute('id', 'liItem');
       li.setAttribute('class', 'dropdown class_new_users');

       a = document.createElement('a');
       a.setAttribute('id', new_users[index]);
       a.setAttribute('class', 'ripple-effect dropdown-toggle friend_list ');
       a.style.color = "#595959";
       a.setAttribute('data-friend', new_users[index]);
       a.setAttribute('data-toggle', 'dropdown');
       a.onclick = function (item) {
         name = item.target.dataset.friend;

         var txt;
         if (confirm(`do you want to add ${name} ?`)) {
           txt = "yes";
           socket.emit('friend_request', {'friend' : name})
           i = new_users.indexOf(name);
           new_users.splice(i, 1);
           liPa = item.target.parentNode;
           liPa.setAttribute('class', 'dropdown class_new_users_wait');
           aPa = item.target;
           console.log(aPa);
           aPa.style.color = "#ff6600";
           span = document.createElement('span');
           span.setAttribute('class', 'glyphicon glyphicon-time wait');
           aPa.insertBefore(span, aPa.childNodes[0]);
         } else {
           txt = "no";
         }
       }
       img = document.createElement('img');
       img.setAttribute('src', '/static/images/add_user.png');
       a.appendChild(img);
       a.innerHTML = new_users[index];
       li.appendChild(a);
       ul.appendChild(li);
       //<span class="glyphicon glyphicon-user icon" style="color:{{ friend.status }}"></span>


         console.log(new_users[index]);
     }

   }

  var input = document.getElementById('inputSearch');
  var counter = 0;

  input.onkeyup = function (event) {

      var filter = input.value.toUpperCase();
      // 8 betekend backspace
      var key = event.keyCode || event.charCode;


      counter++;
      if(counter == 1 && this.value.length == 0 && key == 8 ){
        console.log('back space is in gedrukt met legen string' );
        counter = 0;
        return false;
      }

      if (counter == 1   ){

        console.log('maken');
        li_show = new_user_sep();
        new_user(li_show);
      }else if (this.value.length == 0) {
        counter = 0;
        console.log('verwijderen');
        document.querySelectorAll('.class_new_users').forEach(function(class_user) {
          console.log(class_user);
          ul.removeChild(class_user);
          });
        ul.removeChild(li_show);
      }

      var lis = document.querySelectorAll('#liItem');
      console.log(lis.length);
      for (var i = 0; i < lis.length; i++) {
          console.log(lis[i]);
          var name = lis[i].getElementsByClassName('friend_list')[0].dataset.friend;
          if (name.toUpperCase().indexOf(filter) == 0)
              lis[i].style.display = 'list-item';
          else
              lis[i].style.display = 'none';
      }

  }

  document.querySelectorAll('.friend_list').forEach(function(friend) {
    // kan  evuntiel nog data ophalen uit de database  voor ofline berichten
    friend_list[friend.dataset.friend] = 0 ;
    friend.onclick = function () {
      document.querySelector('#friend_email').innerHTML = friend.dataset.friend;

      socket.emit('open_chat', {'friend' : friend.dataset.friend})
    }

  });

  socket.on('noificatie', function(msg) {




    notification = document.getElementsByClassName(`${msg.frind_notification}`)
    friend_list[msg.frind_notification] = notification[0].innerHTML;

    friend_list[msg.frind_notification] ++;
    notification[0].innerHTML = friend_list[msg.frind_notification];  

    notification[0].style.visibility = 'visible';
    //email_user_id

   });

   socket.on('connect_all', function(msg) {
     console.log(msg['data']);
     el = document.getElementsByClassName(`${msg['data']}`);
     if (typeof(el[0]) != "undefined"){
       el[0].previousElementSibling.style.color = '#428bca';

     }
     friend_name = document.querySelector('#friend_email').innerHTML;
      if (friend_name == msg['data']){
        online = document.querySelector('#online_id');
        online.innerHTML = 'online';
        panel = document.querySelector('#heading_panel');
        panel.className = "panel panel-primary";
      }




    });
    socket.on('disconnect_all', function(msg) {
      console.log(msg['data']);
      el = document.getElementsByClassName(`${msg['data']}`);
      if (typeof(el[0]) != "undefined"){
        el[0].previousElementSibling.style.color = 'red';

      }
      friend_name = document.querySelector('#friend_email').innerHTML;
      console.log(friend_name);
      if (friend_name == msg['data']){
        online = document.querySelector('#online_id');
        online.innerHTML = 'offline';
        panel = document.querySelector('#heading_panel');
        panel.className = "panel panel-danger";
      }

     });


});
