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

// Pour la carte //

var mymap = L.map('mapid').setView([43.608353, 3.879833], 13); //Initialise la carte sur les coordonnees de setView()

var marker = L.marker([43.628834, 3.861713]).addTo(mymap); //Creation d'un marqeur sur les coordonnees gps en parametres
marker.bindPopup("IG forever").openPopup();


L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZ3Q0MjYiLCJhIjoiY2pxMnk4a2U0MTlpaTN4bXVhenZ3cDBmeCJ9.eJr9J2bb4I1VMM6AlAq1IQ', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoiZ3Q0MjYiLCJhIjoiY2pxMnk4a2U0MTlpaTN4bXVhenZ3cDBmeCJ9.eJr9J2bb4I1VMM6AlAq1IQ'
}).addTo(mymap); //Acces a MapBox grace un a un cle ( un  token )




// ----------- //