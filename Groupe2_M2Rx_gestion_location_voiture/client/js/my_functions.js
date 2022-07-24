function disconnect_current_user() {
  localStorage.removeItem("token");
  localStorage.removeItem("login");
  localStorage.removeItem("password");
  location.href = "index.html";
}

function padTo2Digits(num) {
  return num.toString().padStart(2, '0');
}

function charge_menu() {
  var html = '<li><a href="home.html"><i class="icon-home"></i><span>Home</span></a></li>';
  html += '<li><a href="javascript:void(0);" class="has-arrow"><i class="icon-user-follow"></i>';
  html += '<span>Users</span> </a><ul><li><a href="#" class="users_link">Tous les Clients</a></li>';
  if (localStorage.getItem('login') === 'Admin') {
    html += '<li><a href="new_client.html">Ajouter/a></li>';
  }
  html += '</ul></li><li><a href="javascript:void(0);" class="has-arrow">';
  html += '<i class="icon-user-follow"></i><span>Voitures</span> </a><ul><li><a href="#" class="cars_link">Afficher</a></li>';
  if (localStorage.getItem('login') === 'Admin') {
    html += '<li><a href="new_voiture.html">Ajouter</a></li>';
  }
  html += '</ul></li><li><a href="javascript:void(0);" class="has-arrow"><i class="icon-user"></i><span>Locations</span> </a>';
  html += '<ul><li><a href="#" class="rents_link">Afficher</a></li></ul></li>';
  $('#my_menu').html(html);
}

function initialisation() {
  if (!localStorage.getItem("login")) {
    location.href = "index.html";
  }

  $("#my_username").html(localStorage.getItem("login"));

  $(".disconnection").click(function () {
    disconnect_current_user();
  });

  $(".users_link").click(function () {
    // alert(token);
    location.href = "clients.html";
  });
  $(".cars_link").click(function () {
    // alert(token);
    location.href = "voitures.html";
  });
  $(".rents_link").click(function () {
    // alert(token);
    location.href = "locations.html";
  });
}
