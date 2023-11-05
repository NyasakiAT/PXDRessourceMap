const map_url = 'http://127.0.0.1:8000/api/maps/';
const res_type_url = 'http://127.0.0.1:8000/api/ressources/';
const ressources_url = 'http://127.0.0.1:8000/api/maps/<map_id>/nodes/';

window.L_DISABLE_3D = true;

const map = L.map('map', {
  preferCanvas: true,
  crs: L.CRS.Simple,
  minZoom: -4,
});

const map_markers = [];
let selected_pos = [];
const map_select = document.getElementById("maps");
const ressource_select = document.getElementById("ressources");

const addButton = document.getElementById("btn-add")

addButton.addEventListener('click', function () {
  const mapSelectValue = map_select.value; // Get the selected map ID
  const ressourceSelectValue = ressource_select.value; // Get the selected ressource type ID
  const token = getCookie('auth_token'); // Replace 'auth_token' with the actual cookie name

  if (!mapSelectValue || !ressourceSelectValue) {
    alert('Please select a map and a ressource before adding.'); // Provide a message to the user if a map or ressource is not selected
    return;
  }

  // Define the data you want to send in the POST request
  console.log(selected_pos)
  console.log(ressourceSelectValue)
  const postData = {
    x: selected_pos[0], // Set your desired x-coordinate value
    y: selected_pos[1], // Set your desired y-coordinate value
    ressource: `http://127.0.0.1:8000/api/ressources/${ressourceSelectValue}/`, // Use the selected ressource type ID
    map: `http://127.0.0.1:8000/api/maps/${mapSelectValue}/`,
  };

  fetch('http://127.0.0.1:8000/api/ressource-nodes/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`,
    },
    body: JSON.stringify(postData), // Convert the data to a JSON string
  })
    .then((response) => {
      if (response.status === 201) {
        draw_map(map_select.value, ressource_select.value);
      } else {
        alert('Failed to add ressource. Please try again.'); // Provide an error message to the user
      }
    })
    .catch((error) => {
      console.error('Fetch error:', error);
      alert('An error occurred while adding the ressource.'); // Provide an error message to the user
    });
});

window.onload = function () {
  const loginLink = document.getElementById('login-link');

  loginLink.addEventListener('click', function (event) {
    openPopup()
  });

  map_select.addEventListener('change', function () {
    draw_map(map_select.value, ressource_select.value);
  });
  ressource_select.addEventListener('change', function () {
    draw_map(map_select.value, ressource_select.value);
  });

  populate_maps_dropdown(map_select);
  populate_ressource_dropdown(ressource_select);
};

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function checkAuthStatus() {
  const token = getCookie('auth_token'); // Replace 'auth_token' with the actual cookie name

  // Make an API request to check the user's authorization
  return fetch('http://127.0.0.1:8000/api/auth/isauthenticated', {
    method: 'GET',
    headers: {
      'Authorization': `Token ${token}`,
    },
  })
    .then((response) => {
      if (response.status === 200) {
        document.getElementById('admin-controls').style.display = "block";
        return true; // User is authorized
      } else if (response.status === 401) {
        return false; // User is not authorized
      } else {
        throw new Error('Network response was not ok');
      }
    })
    .catch((error) => {
      console.error('Fetch error:', error);
      return false; // An error occurred, consider the user not authorized
    });
}

function populate_maps_dropdown(select) {
  fetch(map_url)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then((data) => {
      console.log(data)
      data.forEach(map => {
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
      data.forEach(map => {
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
          var label = document.getElementById("pos-label")
          selected_pos = [Math.floor(e.latlng.lng), Math.floor(imageHeight - e.latlng.lat)]
          label.innerText = `(${Math.floor(e.latlng.lng)}, ${Math.floor(imageHeight - e.latlng.lat)})`
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
            data.forEach(ressource_node => {
              fetch(ressource_node.ressource)
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
                      iconAnchor: [iconWidth / 2, iconHeight / 2], // point of the icon which will correspond to marker's location
                      popupAnchor: [0, 0] // point from which the popup should open relative to the iconAnchor
                    });

                    const marker_pos = L.latLng([imageHeight - ressource_node.y, ressource_node.x]);
                    const marker = L.marker(marker_pos, { icon: ressource_icon }).addTo(map).bindPopup(name);
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