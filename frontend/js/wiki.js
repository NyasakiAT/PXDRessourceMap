const res_url = 'http://127.0.0.1:8000/api/ressources/';
const res_cat_url = 'http://127.0.0.1:8000/api/ressource-categories/';

window.onload = function () {
    RessourceCategories()
    Ressources()
}


function Ressources() {
    fetch('http://127.0.0.1:8000/api/ressources/')
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            console.log(data)
            data.forEach(element => {
                document.getElementById("wiki-ressources").innerHTML += `<a href=detail.html?type=ressource&id=${element.id}>${element.name}</a>`;
            });
        });
}

function RessourceCategories() {
    fetch('http://127.0.0.1:8000/api/ressource-categories/')
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            console.log(data)
            data.forEach(element => {
                document.getElementById("wiki-categories").innerHTML += `<a href=detail.html?type=category&id=${element.id}>${element.name}</a>`;
            });
        });
}

