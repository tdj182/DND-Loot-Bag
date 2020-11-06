$( document ).ready(function() {
  const BASE_URL = "https://api.open5e.com/";
  let selectGroup;

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
      buildHtml(selectGroup[item])
    }
  }

  // async function addItem(itemObj) {
  //   console.log(typeof itemObj)
  //   console.log(typeof itemObj)

  //   const res = await axios.post("http://127.0.0.1:5000/add-item", form = {
  //     Name: 'Fred',
  //     Age: '23'
  //   })
  //   console.log(res.data)
  // }

  // Add the HTML to select which item to add
  function buildHtml(item) {
    $('#select-block').append(`
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">${item.name}</h5>
        <h6 class="card-subtitle mb-2">Rarity: ${item.rarity} ${item.requires_attunement}</h6>
        <h6 class="card-subtitle mb-2">Type: ${item.type}</h6>
        <form id="form-${item.slug}" action="/add-item method="POST">
          <input hidden type="text" name="name" value="${item.name}">
          <input hidden type="text" name="rarity" value="${item.rarity}">
          <input hidden type="text" name="requires_attunement" value="${item.requires_attunement}">
          <input hidden type="text" name="slug" value="${item.slug}">
          <input hidden type="text" name="text" value="${item.text}">
          <input hidden type="text" name="type" value="${item.type}">
          <button type="submit" class="btn btn-primary" id="button-${item.slug}" formmethod="post" formaction="/add-item">Add Item</button>
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
      alert(`Handler for ${item.slug} called` );
      event.preventDefault();
    });
  }



  $("#item-search-form").on("submit", processForm);

  // $("#select-block").on('click', 'button',  function(event){
    
  //   addItem($(this).data())
  // })
  // $("#test-button").on('click', {
  //   "itemName": itemName,
  //   "rarity": rarity,
  //   "requires_attunement": requires_attunement,
  //   "slug": slug, 
  //   "text": text,
  //   "type": type
  // }, addItem)
});