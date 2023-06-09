$( async () => {
    const results = await $.get("http://shaila.org/wp-content/uploads/2023/06/uStx8CK.jpg")
    console.log(results)
});
$("#YesBtn").on("click", function(event) { 
    console.log("Click!!!!");
    const API_data = document.getElementById("API_input").value;
    console.log("API:",API_data);

    $.ajax({
        type: "POST",
        url: "http:/localhost:5000/SendAPI",
        data: JSON.stringify(API_data),
        contentType: "application/json",
        dataType: 'json', 
        success: function(msg){
            console.log("msg:",msg);
        },
        error: function(){
            console.log("Error");
        }
      });
});
$("#NoBtn").on("click", function(event) { 
    console.log("NOClick!!!!");
    
});