const definition = document.querySelector('#definition')
const word = document.querySelector('#word')
const gameID = document.querySelector('#gameID')
// Start the process of asking the server for the current note once a timer
// expires.
function startTimer() {
  const microseconds = 2000  // 2 seconds
  window.setTimeout(fetchCurrentDef, microseconds)
}

// Ask the server for the current note immediately.
function fetchCurrentDef() {
  console.log("call")
  fetch('/ajax/refresh?gameID=' + gameID.innerHTML)
    // .then(function(response) {
    //   console.log(gameID.innerHTML)
    //
    //   return response.json()
    // })
    // .then(function (myJson) {
    //   // Update the div.
    //   console.log(myJson)
    //   console.log("ajax call successful")
      // Start the timer again for the next request.
      startTimer()
    })
}

if (definition != null) {
  // If note_div is null it means that the user is not logged in.  This is
  // because the jinja template for the '/' handler only renders this div
  // when the user is logged in.  Querying for a note that does not exist
  // returns null.
  console.log("call1")
  // Start by fetching the current note without any delay.
  fetchCurrentDef()
} else {
  console.log(definition)
}
