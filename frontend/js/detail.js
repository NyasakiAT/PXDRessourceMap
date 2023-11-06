const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const id = urlParams.get('id')
console.log("ID: " + id);
const type = urlParams.get('type')
console.log("Type:" + type);

const categoryUrl = "http://127.0.0.1:8000/api/ressource-categories/"
const ressourceUrl = "http://127.0.0.1:8000/api/ressources/"



function AddRessourceDetails(ress) {
    document.getElementById("detail-container").innerHTML += `
    <div class="tile tile-centered">
        <div class="tile-icon">
            <div class="example-tile-icon">
                <img class="icon icon-file centered" src=${ress.icon}></img>
            </div>
        </div>
        <div class="tile-content">
            <div class="tile-title">${ress.name}</div>
            <small class="tile-subtitle text-gray">${ress.description}</small>
        </div>
    </div>
    `;
}

switch (type) {
    case "ressource":
        fetch(ressourceUrl + id)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                console.log(data)
                AddRessourceDetails(data);
            });


        break;
    case "category":
        fetch(categoryUrl + id)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((cat) => {
                console.log(cat)
                cat.ressources.forEach(ress => {
                    AddRessourceDetails(ress);
                });
            });
        break;
    default:
        break;
}