const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const id = urlParams.get('id')
console.log("ID: " + id);

const ressourceUrl = "http://127.0.0.1:8000/api/ressource-categories/"

function AddCategoryDetails(cat) {
    document.title = cat.name
    let content = ""
    content += `<a href=ressource.html?id=${cat.id}>${cat.name}</a>`;
    document.getElementById("detail-container").innerHTML += content;
}


fetch(ressourceUrl + id)
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        console.log(data)
        data.ressources.forEach(element => {
            AddCategoryDetails(element);
        });
    });
