L.mapbox.accessToken = 'pk.eyJ1Ijoiamh0MjExNSIsImEiOiJwcUU0M0pVIn0.q3ouTrQNRmI7VZrvSc7BXQ';

var map_id = 'jht2115.lcgo8fe5' // Dark style
//var map_id = 'jht2115.pc1g2g8b' // Streets Classic style
// var map_id = 'jht2115.pc47h7no' // Satellite streets style
// var map_id = 'jht2115.pc49o1fj' // Satellite style
// var map_id = 'jht2115.pc79e463' // Pencil style
// var map_id = 'jht2115.pc7a395c' // Light style



var map = L.mapbox.map('map', map_id)
    .setView([lat_center_map, lon_center_map], 13);