
const currLootbag = $('.title').attr('id');
// Add the HTML to select which item to add
function buildItemSelectHtml(item) {
  $('#select-block').append(`
  <div class="card">
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
        <button type="submit" class="btn btn-primary" id="button-${item.slug}" formmethod="post" formaction="/lootbag/${currLootbag}/add-item">Add Item</button>
      </form>

      <a data-toggle="collapse" href="#${item.slug}" role="button" aria-expanded="false" aria-controls="${item.slug}" class="card-link">Read More</a>
      <div class="collapse" id="${item.slug}">
        <div class="card card-body">${item.text}.</div>
      </div>
    </div>
  </div>
  `)
  // Prevent the page from refreshing
  $( `#form-${item.slug}`).submit(function( event ) {

  });
}