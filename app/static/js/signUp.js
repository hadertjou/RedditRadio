$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                var rec = JSON.parse(response);
                stat = rec.message;
                document.getElementById("signUpStatus").innerHTML = stat;
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});