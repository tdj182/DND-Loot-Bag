
const currLootbag = $('.title').attr('id');

function addItemHtml(item) {
    $('#item-list').append(`
    <div class="card" style="width: 18rem;">
      <div class="card-body">
        <h5 class="card-title">
          ${item.name} <small>1</small>
          <small><i>${item.requires_attunement}</i></small>
        </h5>
        <h6 class="card-subtitle mb-2 text-muted">Rarity: ${item.rarity}</h6>
        <h6 class="card-subtitle mb-2">Type: ${item.type}</h6>
  
        <div class="edit-delete">
          <form>
            <a data-toggle="collapse" href="#details-${item.id}" role="button" aria-expanded="false" aria-controls="details-${item.id}}" class="card-link btn fas fa-info-circle  text-primary">Details</a>
          </form>
          
        </div>
        
        <div class="collapse" id="details-${item.id}">
          <div class="card card-body">${item.text}.</div>
        </div>
      </div>
    </div>
    `)
}

function addItemCreationHtml(item) {
  if (item.length == 6) {
    console.log(item.length)
  }


  item.splice(3, 0, 'n')
  console.log(item)

  $('#item-list').append(`
  <div class="card" style="width: 18rem;">
    <div class="card-body">
      <h5 class="card-title">
        ${item[1].value} <small>1</small> 
      </h5>
      <h6 class="card-subtitle mb-2 text-muted">Rarity: ${item[2].value}</h6>
      <h6 class="card-subtitle mb-2">Type: ${item[5].value}</h6>

      <div class="edit-delete">
        <form>
          <a data-toggle="collapse" href="#details-${item}" role="button" aria-expanded="false" aria-controls="details-${item}}" class="card-link btn fas fa-info-circle  text-primary">Details</a>
        </form>

      </div>
      
      <div class="collapse" id="details-${item}">
        <div class="card card-body">${item[4].value}.</div>
      </div>
    </div>
  </div>
  `)
}

// Add the HTML that shows a list of items that can be added
function buildItemSelectHtml(item) {
  if (item.route === 'magicitems/' || item.route === 'weapons/'){
    $('#select-block').append(`
    <div class="card" style="width:18rem;">
      <div class="card-body">
        <h5 class="card-title">
          ${item.name}
          <small><i>${item.requires_attunement}</i></small>
        </h5>
        <h6 class="card-subtitle mb-2">Rarity: ${item.rarity}</h6>
        <h6 class="card-subtitle mb-2">Type: ${item.type}</h6>
        <form id="form-${item.slug}" action="/lootbag/${currLootbag}/add-item" method="POST">
          <input hidden type="text" name="item_name" value="${item.name}">
          <input hidden type="text" name="rarity" value="${item.rarity}">
          <input hidden type="text" name="requires_attunement" value="${item.requires_attunement}">
          <input hidden type="text" name="slug" value="${item.slug}">
          <input hidden type="text" name="text" value="${item.text}">
          <input hidden type="text" name="type" value="${item.type}">
          <button type="submit" class="btn btn-primary btn-add-item" id="button-${item.slug}" formmethod="post" formaction="/lootbag/${currLootbag}/add-item">Add Item</button>
        </form>

        <a data-toggle="collapse" href="#${item.slug}" role="button" aria-expanded="false" aria-controls="${item.slug}" class="card-link">Read More</a>
        <div class="collapse" id="${item.slug}">
          <div class="card card-body">${item.text}</div>
        </div>
      </div>
    </div>
    `)
  }
}
