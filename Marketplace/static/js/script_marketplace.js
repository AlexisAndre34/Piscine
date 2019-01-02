$(document).ready(function(){
    $('select').formSelect();
  });
  
 $(document).ready(function(){
    $('.sidenav').sidenav();
});

$(document).ready(function(){
    $('.tooltipped').tooltip();
  });

$(".dropdown-trigger").dropdown();

$('.carousel.carousel-slider').carousel({
    fullWidth: true,
    indicators: true
  });

$(document).ready(function(){
    $('.carousel').carousel();
  });

$(document).ready(function(){
    $('.collapsible').collapsible();
  });

$(document).ready(function(){
    $('.materialboxed').materialbox();
  });

$(document).ready(function(){
   $('textarea').addClass("materialize-textarea")
});

$('#gpsbutton').click(function() {
  var adresse = $('#id_ruecommerce').val()+', '+$('#id_codepostalcommerce').val()+' '+$('#id_villecommerce').val()+', France'  //On concatene la rue et la ville du commerce
  var mapboxClient = mapboxSdk({ accessToken: 'pk.eyJ1IjoiZ3Q0MjYiLCJhIjoiY2pxMnk4a2U0MTlpaTN4bXVhenZ3cDBmeCJ9.eJr9J2bb4I1VMM6AlAq1IQ' });
  mapboxClient.geocoding.forwardGeocode({
    query: adresse,
    limit: 2
  })
  .send()
  .then(response => {
    const match = response.body;
    $('#id_gpslatitude').val(match.features[0].center[1])
    $('#id_gpslongitude').val(match.features[0].center[0])
  });
});

$('#btn_reduction').click(function(){
    if ($('#code_reduction').val()>0  && $('#id_reservation').val()>0){
        $.ajax({
            type: "POST",
            url: "/gestion/reservation/paiement/reduction/",
            data: {
                code_reduction: $('#code_reduction').val(),
                id_reservation: $('#id_reservation').val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken").val()

            },
            dataType: 'json',
            success: function( result ) {
                console.log(result);
                confirm(result.message);
            }
        });
    }
});

// Pour la carte //

var mymap = L.map('mapid').setView([43.608353, 3.879833], 13); //Initialise la carte sur les coordonnees de setView()

var greenIcon = new L.Icon({ //Création d'un icon de localisation vert
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZ3Q0MjYiLCJhIjoiY2pxMnk4a2U0MTlpaTN4bXVhenZ3cDBmeCJ9.eJr9J2bb4I1VMM6AlAq1IQ', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoiZ3Q0MjYiLCJhIjoiY2pxMnk4a2U0MTlpaTN4bXVhenZ3cDBmeCJ9.eJr9J2bb4I1VMM6AlAq1IQ'
}).addTo(mymap); //Acces a MapBox grace un a un cle ( un  token )

var marker_utilisateur;
$('#btn_localisation').click(function(){
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            marker_utilisateur = L.marker([position.coords.latitude,position.coords.longitude],{icon: greenIcon}).addTo(mymap); // Creation du marker avec les coordonnées gps de l'utilisateur
            marker_utilisateur.bindPopup("Vous êtes ici").openPopup();
        });
    }else {
        alert("Le service de géolocalisation n'est pas disponible sur votre ordinateur.");
    }
});
var res;
$('#btn_commerces').click(function(){
    $.ajax({
        type: "POST",
        url: "/carte/commerces/affichage",
        data: {
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken").val()
        },
        dataType: 'json',
        success: function( result ) {
            Commerces = JSON.parse(result.commerces)
            $.each(Commerces, function (cle, valeur){
                var commerce_marker;
                commerce_marker = L.marker([Commerces[cle].fields.gpslatitude, Commerces[cle].fields.gpslongitude]).addTo(mymap);
                commerce_marker.bindPopup(Commerces[cle].fields.nomcommerce);
            });
        }
    });
});

$('#btn_search_map').click(function(){
    $.ajax({
        type: "POST",
        url: "/carte/commerces/search",
        data: {
            recherche: $('#search_map').val(),
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken").val()

        },
        dataType: 'json',
        success: function( result ) {
            Commerces = JSON.parse(result.commerces)
            $.each(Commerces, function (cle, valeur){
                var commerce_marker;
                commerce_marker = L.marker([Commerces[cle].fields.gpslatitude, Commerces[cle].fields.gpslongitude]).addTo(mymap);
                commerce_marker.bindPopup(Commerces[cle].fields.nomcommerce);
            });
        }
    });
});





// ----------- //