$("#YesBtn").on("click", function(event) { 
    console.log("Click!!!!");
    const API_data = document.getElementById("API_input").value;
    const account = document.getElementById("account").value;
    const wp_password = document.getElementById("wp_password").value;
    const wp_url = document.getElementById("wp_url").value;
    console.log("API:",API_data);
    console.log("account:",account);
    console.log("wp_password:",wp_password);
    console.log("wp_url:",wp_url);
    $.ajax({
        type: "POST",
        url: "http:/localhost:5000/SendAPI",
        data: JSON.stringify({
            API_data: API_data,
            account:account,
            wp_password:wp_password,
            wp_url:wp_url,
        }),
        contentType: "application/json",
        dataType: 'json', 
        success: function(msg){
            console.log("msg:",msg);
        },
        error: function(error){
            console.log("Error",error);
        }
      });
});
$("#NoBtn").on("click", function(event) { 
    console.log("NOClick!!!!");
    window.close();
});