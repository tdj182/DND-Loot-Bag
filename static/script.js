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
      buildItemSelectHtml(selectGroup[item])
    }
  }

  $("#item-search-form").on("submit", processForm);
  $('#btn-convert').on("click", beginCurrencyAdjustment);
  
  $('#select-block').on('click', ".btn-add-item", function() {
    selectedItem = $(this).siblings("[name=slug]")
    for (const item in selectGroup) {
      if (selectGroup[item].slug == selectedItem[0].defaultValue){
        addItemHtml(selectGroup[item])
      }
    }
  })
  
  $('#item-list').on('click', '.fa-trash', function() {
    $(this).parents("[class=card]").remove()
  })

  // set value to 0 on focus
  $('input[type=number]').on('focusin', function() {
    this.value = '0';
  });


  convertCurrency()
});