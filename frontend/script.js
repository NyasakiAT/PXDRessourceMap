const map_url = 'http://127.0.0.1:8000/api/maps/';
const res_type_url = 'http://127.0.0.1:8000/api/ressource-types/';
const ressources_url = 'http://127.0.0.1:8000/api/maps/<map_id>/nodes/';

window.L_DISABLE_3D = true;

const map = L.map('map', {
  preferCanvas: true,
  crs: L.CRS.Simple,
  minZoom: -4,
});

const map_markers = [];

const map_select = document.getElementById("maps");
const ressource_select = document.getElementById("ressources");

window.onload = function () {
  map_select.addEventListener('change', function () {
    draw_map(map_select.value, ressource_select.value);
  });
  ressource_select.addEventListener('change', function () {
    draw_map(map_select.value, ressource_select.value);
  });

  populate_maps_dropdown(map_select);
  populate_ressource_dropdown(ressource_select);
};

function populate_maps_dropdown(select) {
  fetch(map_url)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then((data) => {
      data.results.forEach(map => {
        const optionElement = document.createElement('option');
        optionElement.value = map.id;
        optionElement.text = map.name;
        select.add(optionElement);
      });

      // Automatically draw the map for the first option
      draw_map(map_select.value, ressource_select.value);
    });
}

function populate_ressource_dropdown(select) {
  fetch(res_type_url)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then((data) => {
      data.results.forEach(map => {
        const optionElement = document.createElement('option');
        optionElement.value = map.id;
        optionElement.text = map.name;
        select.add(optionElement);
      });

      // Automatically draw the map for the first option
      draw_map(map_select.value, ressource_select.value);
    });
}

function draw_map(map_index, type_index = null) {
  fetch(map_url + map_index)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then((data) => {
      const imageUrl = data.image;

      // Preload the map image
      const img = new Image();
      img.src = imageUrl;
      img.onload = function () {
        const imageWidth = img.width;
        const imageHeight = img.height;

        map.on('click', function (e) {
          console.log(e.latlng.lng, imageHeight - e.latlng.lat);
        });

        map_markers.forEach(marker => map.removeLayer(marker));
        map_markers.length = 0;

        const bounds = [[0, 0], [imageHeight, imageWidth]];
        const image = L.imageOverlay(imageUrl, bounds).addTo(map);
        map.fitBounds(bounds);

        const ressource_api = ressources_url.replace("<map_id>", map_index) + ((type_index != null) ? type_index : "");;

        fetch(ressource_api)
          .then((response) => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then((data) => {
            data.results.forEach(ressource_node => {
              fetch(ressource_node.ressource_type)
                .then((response) => {
                  if (!response.ok) {
                    throw new Error('Network response was not ok');
                  }
                  return response.json();
                })
                .then((ressourceData) => {
                  var name = ressourceData.name;
                  var icon = ressourceData.icon;
                  const icon_img = new Image();
                  icon_img.src = icon;
                  icon_img.onload = function () {
                    const iconWidth = icon_img.width;
                    const iconHeight = icon_img.height;

                    var ressource_icon = L.icon({
                      iconUrl: icon,

                      iconSize: [iconWidth, iconHeight], // size of the icon
                      iconAnchor: [iconWidth/2, iconHeight/2], // point of the icon which will correspond to marker's location
                      popupAnchor: [0, 0] // point from which the popup should open relative to the iconAnchor
                    });

                    const marker_pos = L.latLng([imageHeight - ressource_node.y, ressource_node.x]);
                    const marker = L.marker(marker_pos, {icon: ressource_icon}).addTo(map).bindPopup(name);
                    map_markers.push(marker);
                  }
                })
                .catch((error) => {
                  console.error('Fetch error:', error);
                });
            });
          })
          .catch((error) => {
            console.error('Fetch error:', error);
          });
      };

      img.src = imageUrl;
    })
    .catch((error) => {
      console.error('Fetch error:', error);
    });
}