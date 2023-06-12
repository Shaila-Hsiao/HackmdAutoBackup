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
    // // 點選載入時的畫面
    // chrome.storage.sync.set({ "status": 1 });
    // // 點選時
    // chrome.storage.sync.get("status").then((result)=>{
    //     console.log("Value currently is " + result.status);
    //     if (result.status == 0) {
    //         console.log("null",result.status);
    //       } else {
    //         console.log("loading",result.status);
    //     }
    // });
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
            console.log("msg:",msg[1]);
            // 收到成功的話
            chrome.storage.sync.set({ "status": 2 });
            $('#YesBtn').prop('disabled', false)
            $("#spinner").attr('hidden', true);
            $("#finish").attr('hidden', false);

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
