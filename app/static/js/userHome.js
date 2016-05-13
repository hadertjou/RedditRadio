$(function() {
    $('#btnSubmit').click(function() {
 
        document.getElementById("statusDisplay").innerHTML = "Beginning Fetch";//"Fetching...";
        $.ajax({
            url: '/radio',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                var rec = JSON.parse(response);
                stat = rec.message;
                document.getElementById("statusDisplay").innerHTML = stat;
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
        document.getElementById("inputSub").value = "";
        $('#btnSubmit').attr('disabled', true);
    });
});

$(function() {
    $('#inputSub').keyup(function() {
        if($('#inputSub').val() != "")
        {
            $('#btnSubmit').removeAttr('disabled');
        }
        else
        {
            $('#btnSubmit').attr('disabled', true);   
        }
        
    });
});


$(function() {
    $('#btnPlay').click(function() {
        play(); 
       
    });
});

$(function() {
    $('#btnSkip').click(function() {
        voiceEndCallback(); 
       
    });
});

$(function() {
    $('#btnPause').click(function() {
        pause(); 
       
    });
});

$(function() {
    $('#btnResume').click(function() {
        resume(); 
       
    });
});

$(function() {
    $('#btnFlush').click(function() {
 
        document.getElementById("statusDisplay").innerHTML = "Flushing...";
        $.ajax({
            url: '/flush',
            type: 'GET',
            success: function(response) {
                var rec = JSON.parse(response);
                stat = rec.message;
                document.getElementById("statusDisplay").innerHTML = stat;
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});