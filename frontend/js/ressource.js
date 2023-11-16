const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const id = urlParams.get('id')
console.log("ID: " + id);

const ressourceUrl = "http://195.128.103.180:8000/api/ressources/"

function AddIngredient(ingredient) {
    return `<tr><td>${ingredient.amount}</td><td>${ingredient.ingredient.name}</td></tr>`
}

function AddRecipe(rec) {
    return `
        <h4>${rec.name}</h4>
        <table class="table">
        <thead>
            <tr>
                <th>Amount</th>
                <th>Ressource</th>
            </tr>
        </thead>
        ${rec.ingredients.map(ingredient => AddIngredient(ingredient)).join('')}
        </table>
        <p><span>Crafted In: </span>${rec.crafting_station.name}</p>`
}

function AddRessourceDetails(ress) {
    document.title = ress.name
    let content = ""
    content += `<div class="item-header">
        <img style="width: 100px; height: 100px;" src=${ress.image}></img>
        <div class="item-title">
            <h2>${ress.name}</h2>
            <p>${ress.description}</p>
        </div>
    </div>
    <div class="item-body">
        <p class="item-data"><span>Stack Size: </span>${ress.stack_size}</p>
        <p class="item-data"><span>Category: </span>${ress.ressource_category.name}</p>
        <p class="item-data"><span>Obtained From: </span>${ress.obtained_from}</p>
    </div>`;
    if(ress.used_in.length > 0){
        content += `<div class="item-recipies">
        <h3>Recipies</h3>
        ${ress.used_in.map(element => AddRecipe(element)).join('')}
    </div>`
    }
    document.getElementById("detail-container").innerHTML = content;
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
        AddRessourceDetails(data);
    });
