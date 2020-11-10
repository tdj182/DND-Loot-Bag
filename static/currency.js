let baseCopper = 0;

function beginCurrencyAdjustment(){
  //only run if input is not empty
  if (checkInput()) {
    currencyInputArr = getInput()
    currencyHistoryArr = getHistory()
    updatedHistoryArr = currencyInputArr.map(function (num, idx) {
      return num + currencyHistoryArr[idx];
    })
    
    updateHistoryHtml(updatedHistoryArr)
    convertCurrency()
  } else {
    alert('Empty convert value not permitted')
  }
}

function checkInput() {
  if ($('input[name=platinum]').val() == "" ||
      $('input[name=gold]').val() == "" ||
      $('input[name=electrum]').val() == "" ||
      $('input[name=silver]').val() == "" ||
      $('input[name=copper]').val() == "") {
      return false
  } else {
    return true
  }
}

function getInput() {
  plat = parseInt($('input[name=platinum]').val())
  gold = parseInt($('input[name=gold]').val())
  electrum = parseInt($('input[name=electrum]').val())
  silver = parseInt($('input[name=silver]').val())
  copper = parseInt($('input[name=copper]').val())
  return [plat,gold,electrum,silver,copper]
}

function getHistory() {
  plat = parseInt($("#platinum-history").text().split(": ").pop())
  gold = parseInt($("#gold-history").text().split(": ").pop())
  electrum = parseInt($("#electrum-history").text().split(": ").pop())
  silver = parseInt($("#silver-history").text().split(": ").pop())
  copper=parseInt($("#copper-history").text().split(": ").pop())
  return [plat,gold,electrum,silver,copper]
}

function updateHistoryHtml(historyArr) {
  $("#platinum-history").text(`Platinum: ${historyArr[0]}`)
  $("#gold-history").text(`Gold: ${historyArr[1]}`)
  $("#electrum-history").text(`Electrum: ${historyArr[2]}`)
  $("#silver-history").text(`Silver: ${historyArr[3]}`)
  $("#copper-history").text(`Copper: ${historyArr[4]}`)
}

function convertCurrency() {
  baseCopper =
    parseInt($("#platinum-history").text().split(": ").pop()) * 1000 +
    parseInt($("#gold-history").text().split(": ").pop()) * 100 +
    parseInt($("#electrum-history").text().split(": ").pop()) * 50 +
    parseInt($("#silver-history").text().split(": ").pop()) * 10 +
    parseInt($("#copper-history").text().split(": ").pop());

  updateConvertedCurrencyHtml()
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


