$(".mdl-textfield__input").blur(function (){
    if( !this.value ){
        $(this).prop('required', true);
        $(this).parent().addClass('is-invalid');
    }
});
$(".mdl-button[type='submit']").click(function (event){
    $(this).siblings(".mdl-textfield").children(".mdl-textfield__input").prop('required', true);
});

$('form[method="put"], form[method="delete"]').submit(function(e) {
    e.preventDefault();
    
    var method = $(this).attr('method');
    var url = $(this).attr('action');
    var data = $(this).serializeArray();

    // send Ajax request instead!
    $.ajax({
        type: method,
        url: url,
        data: data,
        success: function(result) {
            console.log('Req Done', result);
            window.location.href = "/";
        },
        error: function(jqXHR, status, err) {
            console.log('Error', err);
        }
    });
})

function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();

    if( profile ) {

        var id_token = googleUser.getAuthResponse().id_token;
        // console.log("ID Token: " + id_token);
        var state = $('#state').val();

        $.ajax({
            type: 'POST',
            url: '/gconnect?state=' + state,
            processData: false,
            data: id_token,
            contentType: 'application/octet-stream; charset=utf-8',
            success: function(result) {
                console.log('Auth Done', result);
                window.location.href = "/";
            },
            error: function(jqXHR, status, err) {
                console.log('Error', err);
                alert(err);
            }
        });
    }
}

function signOut() {
    $.ajax({
        type: 'POST',
        url: '/gdisconnect',
        success: function() {
            console.log('Sign Out Done');
            window.location.href = "/";
        },
        error: function(jqXHR, status, err) {
            console.log('Error', err);
        }
    });
}