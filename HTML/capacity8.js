var roomDatas = []
function gotolargeRooms() {
    var room_category = "Large"
    fetch("http://127.0.0.1:5000/meetingRoom", {
        // Adding method type
        method: "POST",
        // Adding body or contents to send
        body: JSON.stringify({
            room_category: room_category
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
            var roomDatas = json.data;
            console.log(roomDatas)

            document.getElementById("main").innerHTML = `
            ${roomDatas.map(roomTemplate).join("")}            
`;
        }
        );
}

function navigatetolargeRooms() {
    location.href = "capacity8.html";
}

function roomTemplate(room) {
    console.log(room.room_url)
    console.log(room.room_name)
    return ` 
    <div class="wrapper">
            <div class="menu-item">
                  <div class="product-img">
                      <img src="${room.room_url}" height="250" width="327">
                  </div>
                <div class="product-info ">
                      <div class="product-text">
                          <h1>${room.room_name}</h1>
                          <h2>by Planzo</h2>
                          <p>${room.room_description}</p>
                      </div>               
                      <div class="product-price-btn">
                          <button onclick="navigatetoperticularRooms(${room.room_id})">
                              <a type="button">show</a>
                          </button>
                      </div>
                </div>
             </div>
        </div>    
  `;
}

function navigatetoperticularRooms(room_id) {
    localStorage.setItem("roomId", room_id)
    location.href = "room3.html?room_id="+room_id;
}

{/* <a href="room1.html" type="button">show</a> */}

function roomDetails() {
    let params = (new URL(location.href)).searchParams;
    
    fetch("http://127.0.0.1:5000/perticularRoom", {
        // Adding method type
        method: "POST",
        // Adding body or contents to send
        body: JSON.stringify({
            room_id: params.get("room_id")
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
            var perticularroomData = json.roomData;
            localStorage.setItem("roomURL",perticularroomData[0].room_url)
            localStorage.setItem("roomName",perticularroomData[0].room_name)
            console.log(perticularroomData)
            document.getElementById("roomMain").innerHTML = `
            ${perticularroomData.map(perticularroomTemplate).join("")}           
`;
        }
        );
}

function perticularroomTemplate(room) {
    console.log(room.room_url)
    console.log(room.room_name)
    console.log(room.inner_description)
    return ` 
    <div class="section">
        
        <img src="${room.room_url}" class="responsive">
        
        
        <div class="text">
            <h2>${room.room_name}</h2>
            <p>${room.inner_description}</p>
            <h3>Availabilities in Room</h3>
                <ul class="list-group" id="box" >
                    <li class="list-group-item">${room.room_availability}</li>             
                </ul>
                  
            </p>

            <a onclick="checkifBooked()" class="button" style="cursor:pointer;">Book</a>
            <a class="button"  href="order.html" style="cursor:pointer;">Order Refreshment</a>
        </div>
        </div> 
  `;
}


function checkifBooked() {
    var room_id = localStorage.getItem("roomId");
    fetch("http://127.0.0.1:5000/checkifbooked", {
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
            response.json()).then(json => {
              console.log(json)
              if (json.status == true) {
                // alert(json.message)
                // location.href = "book.html"
                swal({
                  title: "Good job!",
                  text: json.message,
                  icon: "success",
                  button: "OK",
                })
                .then((value) => {
                  location.href = "book.html"
                })
    
              } 
              else {
                swal({
                  title: "NOT GOOD job!",
                  text: json.message,
                  icon: "warning",
                  button: "OK",
                });
              }
    
            })
        }
