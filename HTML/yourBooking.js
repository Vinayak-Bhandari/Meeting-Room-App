function yourBooking() {
    var user_id = localStorage.getItem("userId");
    fetch("http://127.0.0.1:5000/yourBookings", {
        // Adding method type
        method: "POST",
        // Adding body or contents to send
        body: JSON.stringify({
            user_id: user_id
        }),
        // Adding headers to the request
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })

        // Converting to JSON
        .then(response =>
            response.json())
        .then(json => {
            var yourBookings = json.yourData;
            console.log(yourBookings.length)
            // localStorage.setItem("roomURL",perticularroomData[0].room_url)
            // localStorage.setItem("roomName",perticularroomData[0].room_name)
            // console.log(perticularroomData)
            if (yourBookings.length <= 0) {
                swal("Not-Found!", json.message, "warning");
            }
            document.getElementById("main").innerHTML = `
        ${yourBookings.map(yourbookingroomTemplate).join("")} 
    
`;
        }
        );

}


// function gotoyourBookings(){

//      location.href="yourBooking.html";
// }

function yourbookingroomTemplate(room) {
    console.log(room.room_url)
    console.log(room.room_name)

    return ` 

<div class="wrapper">
            <div class="menu-item">
                  <div class="product-img">
                      <img src="${room.room_url}" height="278" width="327">
                  </div>
                <div class="product-info ">
                      <div class="product-text">
                          <h1>${room.room_name}</h1>
                          <p><b>Name:</b> ${room.name}</p>
                          <p><b>Ph.No:</b> ${room.phone}</p>
                          <p><b>Time: </b>${room.time}</p>
                          <p><b>Date:</b> ${room.date}</p>
                      </div>               
                      <div class="product-price-btn">
                          <button onclick="cancelBooking(${room.room_id})">
                              <a  type="button">Cancel Booking</a>
                          </button>
                      </div>
                </div>
             </div>
        </div>    
`;
}

function cancelBooking(roomid) {
    var room_id = roomid
    fetch("http://127.0.0.1:5000/cancelBooking", {
        // Adding method type
        method: "POST",
        // Adding body or contents to send
        body: JSON.stringify({
            room_id: room_id
        }),
        // Adding headers to the request
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })

        // Converting to JSON
        .then(response =>
            response.json())
        .then(json => {
            if (json.status == true) {
                swal({
                    title: "Are you sure?",
                    text: "Are you sure you want to cancel your Booking!",
                    icon: "warning",
                    buttons: true,
                    dangerMode: true,
                })
                    .then((willDelete) => {
                        if (willDelete) {
                            swal(json.message, {
                                icon: "success",
                            }).then(value=>{
                                yourBooking();
                            })
                        } else {
                            swal("Cancelled");
                        }

                    })
            }
            else {
                swal({
                    title: "NOT GOOD job!",
                    text: json.message,
                    icon: "warning",
                    button: "OK",
                }).then(value=>{
                    yourBooking();
                });
            }
        },
        );



}