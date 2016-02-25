/*
orange: #FFA500
aqua: #00FFFF GOOD
orangered: #FF4500
fushia: #FF00FF GOOD
*/

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
        layer.bindPopup(msg);
    }
};


// L.geoJson(geojson_features, {
//     onEachFeature: onEachFeature,
//     style: myStyle
// }).addTo(map);


function getColor(x) {
  return x <= 1     ?    '#00FFFF': // blue
         x <= 2     ?   '#FFFF00': // yellow
         x <= 3     ?   '#FFA500': // orange
         x <= 4    ?   '#FF4500': // orangered
                          '#FF0000'; // red
};

function getOpacity(x) {
  return x <= 1     ?    0.5:
         x <= 2     ?   0.5:
         x <= 3     ?   0.5:
         x <= 4    ?   0.5:
                          0.5;
};

L.geoJson(geojson_features, {
    onEachFeature: onEachFeature,
    style: function (feature) {
        return {
         "color": getColor(feature.properties.color),
         //"opacity": 0.5,
         "opacity": getOpacity(feature.properties.color),
        }}
}).addTo(map);




