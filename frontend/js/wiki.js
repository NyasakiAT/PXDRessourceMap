const res_url = 'http://195.128.103.180:8000/api/ressources/';
const res_cat_url = 'http://195.128.103.180:8000/api/ressource-categories/';

window.onload = function () {
    RessourceCategories()
    //Ressources()
}


/*function Ressources() {
    fetch('http://195.128.103.180:8000/api/ressources/')
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            console.log(data)
            data.forEach(element => {
                if(element.is_crafted == false)
                    document.getElementById("wiki-ressources").innerHTML += `<a href=ressource.html?id=${element.id}>${element.name}</a>`;
            });
        });
}*/

function AddRessource(ress){
    return `
        <div class="ress-card">
            <img src=${ress.image}></img>
            <a href=ressource.html?id=${ress.id}>${ress.name}</a>
        </div>`
}

function RessourceCategories() {
    fetch('http://195.128.103.180:8000/api/ressource-categories/')
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            console.log(data)
            data.forEach(element => {
                document.getElementById("wiki-categories").innerHTML += `
                <div class="ressource-cat-container">
                    <a href=category.html?id=${element.id}><h3>${element.name}</h3></a>
                    <div class="ressource-container">
                        ${element.ressources.map(element => AddRessource(element)).join('')}
                    </div>
                </div>
                `;
            });
        });
}

