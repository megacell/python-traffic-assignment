
// var myStyle = {
//     color: "#00FFFF",
//     weight: 1,
//     opacity: 0.5
// };

var highlightStyle = {
    color: '#FF00FF', 
    weight: 1,
    opacity: 1,
};

// got from this website
// http://palewi.re/posts/2012/03/26/leaflet-recipe-hover-events-features-and-polygons/

function onEachFeature(feature, layer) {
    
    //(function(layer, properties) {
    //  layer.on("mouseover", function (e) {layer.setStyle(highlightStyle);});
    //  layer.on("mouseout", function (e) {layer.setStyle(myStyle); });
    //})(layer, feature.properties);

    if (feature.properties) {
    	var msg = ""
    	if (feature.properties.user_id) {
    	    msg = msg.concat("user_id: ")
    	    msg = msg.concat(feature.properties.user_id)
    	    msg = msg.concat("<br>")
    	}
        if (feature.properties.distance) {
            msg = msg.concat("length: ")
    	    msg = msg.concat(feature.properties.distance)
    	    msg = msg.concat("<br>")
        }
        if (feature.properties.duration) {
            msg = msg.concat("duration: ")
    	    msg = msg.concat(feature.properties.duration)
    	    msg = msg.concat("<br>")
        }
        if (feature.properties.number_points) {
            msg = msg.concat("#points: ")
    	    msg = msg.concat(feature.properties.number_points)
    	    msg = msg.concat("<br>")
        }
        if (feature.properties.flow_over_capacity) {
            msg = msg.concat("flow/capacity: ")
            msg = msg.concat(feature.properties.flow_over_capacity)
            msg = msg.concat("<br>")
        }
        if (feature.properties.tt_over_fftt) {
            msg = msg.concat("tt/fftt: ")
            msg = msg.concat(feature.properties.tt_over_fftt)
            msg = msg.concat("<br>")
        }
        if (feature.properties.capacity) {
            msg = msg.concat("capacity: ")
            msg = msg.concat(feature.properties.capacity)
            msg = msg.concat("<br>")
        }
        if (feature.properties.freespeed) {
            msg = msg.concat("freespeed: ")
            msg = msg.concat(feature.properties.freespeed)
            msg = msg.concat("<br>")
        }
        if (feature.properties.speed) {
            msg = msg.concat("speed: ")
            msg = msg.concat(feature.properties.speed)
            msg = msg.concat("<br>")
        }
        if (feature.properties.flow) {
            msg = msg.concat("flow: ")
            msg = msg.concat(feature.properties.flow)
            msg = msg.concat("<br>")
        }
        if (feature.properties.fftt) {
            msg = msg.concat("fftt: ")
            msg = msg.concat(feature.properties.fftt)
            msg = msg.concat("<br>")
        }
        if (feature.properties.length) {
            msg = msg.concat("length: ")
            msg = msg.concat(feature.properties.length)
            msg = msg.concat("<br>")
        }
        if (feature.properties.r_routed) {
            msg = msg.concat("ratio routed: ")
            msg = msg.concat(feature.properties.r_routed)
            msg = msg.concat("<br>")
        }
        if (feature.properties.r_non_routed) {
            msg = msg.concat("ratio non-routed: ")
            msg = msg.concat(feature.properties.r_non_routed)
            msg = msg.concat("<br>")
        }
        if (feature.properties.co2) {
            msg = msg.concat("CO2: ")
            msg = msg.concat(feature.properties.co2)
            msg = msg.concat("<br>")
        }
        if (feature.properties.local) {
            msg = msg.concat("local: ")
            msg = msg.concat(feature.properties.local)
            msg = msg.concat("<br>")
        }
        if (feature.properties.link_id) {
            msg = msg.concat("link id: ")
            msg = msg.concat(feature.properties.link_id)
            msg = msg.concat("<br>")
        }
        if (feature.properties.max_id) {
            msg = msg.concat("max id: ")
            msg = msg.concat(feature.properties.max_id)
            msg = msg.concat("<br>")
        }
        if (feature.properties.inc) {
            msg = msg.concat("increase: ")
            msg = msg.concat(feature.properties.inc)
            msg = msg.concat("<br>")
        }
        if (feature.properties.dec) {
            msg = msg.concat("decrease: ")
            msg = msg.concat(feature.properties.dec)
            msg = msg.concat("<br>")
        }
        if (feature.properties.city) {
            msg = msg.concat("city: ")
            msg = msg.concat(feature.properties.city)
            msg = msg.concat("<br>")
        }
        if (feature.properties.county) {
            msg = msg.concat("county: ")
            msg = msg.concat(feature.properties.county)
            msg = msg.concat("<br>")
        }
        layer.bindPopup(msg);
    }
};

// L.geoJson(geojson_features, {
//     onEachFeature: onEachFeature,
//     style: myStyle
// }).addTo(map);


// blue, yellow, orange, orange-red, red
var colors = ['#00FFFF', '#FFFF00', '#FFA500', '#FF4500', '#FF0000']
// green, green-yellow, yellow, orange, red
// var colors = ['#2CC200', '#8CD100', '#E0C700', '#EF6A00', '#FF0000'];


function getColor(x) {
  return x <= 1     ?    colors[0]:
         x <= 2     ?   colors[1]:
         x <= 3     ?   colors[2]:
         x <= 4    ?   colors[3]:
                          colors[4];
};

function getOpacity(x) {
  return x <= 1     ?    1.0:
         x <= 2     ?   1.0:
         x <= 3     ?   1.0:
         x <= 4    ?   1.0:
                          1.0;
};

function getWeight(x) {
  return x <= 1     ?    1:
         x <= 2     ?   2:
         x <= 3     ?   3:
         x <= 4    ?   4:
                          5;
};

L.geoJson(geojson_features, {
    onEachFeature: onEachFeature,
    style: function (feature) {
        return {
         "color": getColor(feature.properties.color),
         //"opacity": 0.5,
         //"weight": 2,
         "weight": getWeight(feature.properties.weight),
         "opacity": getOpacity(feature.properties.color),
        }}
}).addTo(map);




