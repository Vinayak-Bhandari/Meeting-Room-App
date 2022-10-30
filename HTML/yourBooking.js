function yourBooking() {
    var user_id = localStorage.getItem("userId");    
fetch("http://127.0.0.1:5000/yourBookings", {
    // Adding method type
    method: "POST",
    // Adding body or contents to send
    body: JSON.stringify({
        user_id:user_id
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
        console.log(yourBookings)
        // localStorage.setItem("roomURL",perticularroomData[0].room_url)
        // localStorage.setItem("roomName",perticularroomData[0].room_name)
        // console.log(perticularroomData)
        if(yourBookings == undefined){
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
<div class="selection">

    <img src="${room.room_url}" class="responsive">
    
    <div class="text">
        <h2>${room.room_name}</h2>
        <p><b>Name:</b> ${room.name}</p>
        <p><b>Email:</b> ${room.email}</p>
        <p><b>Phone.No:</b> ${room.phone}</p>
        <p><b>Time:</b> ${room.time}</p>
        <p><b>Date:</b> ${room.date}</p>

        <a class="button" style="cursor:pointer;">Cancel your Booking</a>
    </div>
</div> 
`;
}
