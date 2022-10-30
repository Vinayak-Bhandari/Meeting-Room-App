
function gotouserProfile() {
    fetch("http://127.0.0.1:5000/alreadyBooked", {
        // Adding method type
        method: "GET",
        // Adding body or contents to send
        // body: JSON.stringify({
        //     room_category: room_category
        // }),
        // Adding headers to the request
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })

        // Converting to JSON
        .then(response =>
            response.json())
        .then(json => {
            bookedDatas = json.bookedData;
            console.log(bookedDatas)
            // console.log(roomDatas)
            if(bookedDatas == ''){
                swal("Not-Found!", "Rooms are not booked yet!", "warning");
            }
            document.getElementById("main").innerHTML = `
            ${bookedDatas.map(roomTemplate).join("")}           
`;
        }
        );
}


function roomTemplate(book) {
    // console.log(room.room_url)
    // console.log(room)
    return ` 
    <div class="wrapper">
            <div class="menu-item">
                  <div class="product-img">
                      <img src="${book.room_url}" height="250" width="327">
                  </div>
                <div class="product-info ">
                      <div class="product-text">
                          <h1>${book.room_name}</h1>
                          <h2>by Planzo</h2>
                          <p><b>Name:</b> ${book.name}</p>
                          <p><b>Ph.No:</b> ${book.phone}</p>
                          <p><b>Date:</b> ${book.date}</p>
                          <p><b>Time: </b>${book.time}</p>
                      </div>               
                      <div class="product-price-btn">
                      </div>
                </div>
             </div>
        </div>    
  `;
}
