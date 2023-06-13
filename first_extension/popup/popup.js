$("#YesBtn").on("click", function(event) { 
    $("#unfinish").attr('hidden', true);
    $("#finish").attr('hidden', true);
    console.log("Click!!!!");
    const API_data = document.getElementById("API_input").value;
    const account = document.getElementById("account").value;
    const wp_password = document.getElementById("wp_password").value;
    const wp_url = document.getElementById("wp_url").value;
    console.log("API:",API_data);
    console.log("account:",account);
    console.log("wp_password:",wp_password);
    console.log("wp_url:",wp_url);
    // Click Button : Loading
    $('#YesBtn').prop('disabled', true)
    $('#Yes').text('Loading..')
    $("#spinner").removeAttr("style");
    $("#spinner").attr('hidden', false);
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
            console.log("msg:");
            // 收到成功的話
            $('#YesBtn').prop('disabled', false)
            $("#spinner").attr('hidden', true);
            $("#finish").attr('hidden', false);
            $('#Yes').text('確定')
        },
        error: function(error){
            console.log("Error",error);
            // 收到成功的話
            $('#YesBtn').prop('disabled', false)
            $("#spinner").attr('hidden', true);
            $("#unfinish").attr('hidden', false);
            $('#Yes').text('確定')
        }
      });
});
$("#NoBtn").on("click", function(event) { 
    console.log("NOClick!!!!");
    window.close();
});
