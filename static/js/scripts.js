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


var date = new Date();

var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

// var month = dateObj.getUTCMonth() + 1; //months from 1-12
// var weekday = dateObj.toLocaleString("default",{weekday:"long"})
// var day = dateObj.getUTCDate();
// var year = dateObj.getUTCFullYear();

// newdate = weekday + "," + year + "/" + month + "/" + day;
newdate = date.toLocaleDateString("default",options)
document.getElementById('newdate').innerHTML=newdate;