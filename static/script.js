$( document ).ready(function() {
  const BASE_URL = "https://api.open5e.com/";
  let selectGroup;
  let baseCopper = 0;
  const currLootbag = $('.title').attr('id');

  async function processForm(evt) {
    evt.preventDefault()
    $('#select-block').empty()
    const search = $("#search").val();
    // Do nothing if the string is empty
    if (!search) {
      console.log('empty string')
      return;
    }
    console.log(search)
    search
    const res = await axios.get(`${BASE_URL}search/?text=${search}`);
    handle5eResponse(res.data)
  }

  /** handleResponse: deal with response from our lucky-num API. */

  function handle5eResponse(data) {
    console.log(data.results)
    selectGroup = data.results
    for (const item in selectGroup) {
      buildItemSelectHtml(selectGroup[item])
    }
  }

  // Convert Currency
  function convertCurrency() {
    baseCopper =
      parseInt($("#platinum-history").text().split(": ").pop()) * 1000 +
      parseInt($("#gold-history").text().split(": ").pop()) * 100 +
      parseInt($("#electrum-history").text().split(": ").pop()) * 50 +
      parseInt($("#silver-history").text().split(": ").pop()) * 10 +
      parseInt($("#copper-history").text().split(": ").pop());

    updateConvertedCurrencyHtml()
    console.log(baseCopper);
  }

  function updateConvertedCurrencyHtml() {
    $("#platinum-converted").html(`Platinum: ${Math.floor(
      baseCopper / 1000
    )} <i class="fas fa-coins platinum-coin"></i>`)
    $("#gold-converted").html(`gold: ${Math.floor(
      baseCopper / 100
    )} <i class="fas fa-coins gold-coin"></i>`)
    $("#electrum-converted").html(`electrum: ${Math.floor(
      baseCopper / 50
    )} <i class="fas fa-coins electrum-coin"></i>`)
    $("#silver-converted").html(`silver: ${Math.floor(
      baseCopper / 10
    )} <i class="fas fa-coins silver-coin"></i>`)
    $("#copper-converted").html(`copper: ${Math.floor(
      baseCopper
    )} <i class="fas fa-coins copper-coin"></i>`)
  }

  // Add the HTML to select which item to add
  function buildItemSelectHtml(item) {
    $('#select-block').append(`
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">${item.name}</h5>
        <h6 class="card-subtitle mb-2">Rarity: ${item.rarity} ${item.requires_attunement}</h6>
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



  $("#item-search-form").on("submit", processForm);

  convertCurrency()
});