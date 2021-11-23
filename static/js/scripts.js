$("form[name=signup_form").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/dashboard/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault();
});

$("form[name=login_form").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/dashboard/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault();
});


function deposit(){
    $("form[name=deposit_withdraw_form").submit(function(e){
        var $form = $(this);
        var $error = $form.find(".error");
        var data = $form.serialize();
        $.ajax({
            url: "/user/deposit",
            type: "POST",
            data: data,
            dataType: "json",
            success: function(resp) {
                
                document.getElementById("form_id").reset();
                location.reload();
                
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })
    e.preventDefault();
    })
};

function withdraw(){
    $("form[name=deposit_withdraw_form").submit(function(e){
        var $form = $(this);
        var $error = $form.find(".error");
        var data = $form.serialize();
        $.ajax({
            url: "/user/withdraw",
            type: "POST",
            data: data,
            dataType: "json",
            success: function(resp) {
                
                document.getElementById("form_id").reset();
                location.reload();
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })
    e.preventDefault();
    })
};


var date = new Date();

var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

newdate = date.toLocaleDateString("default",options)
document.getElementById('newdate').innerHTML=newdate;