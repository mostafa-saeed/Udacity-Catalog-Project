$(".mdl-textfield__input").blur(function (){
    if( !this.value ){
        $(this).prop('required', true);
        $(this).parent().addClass('is-invalid');
    }
});
$(".mdl-button[type='submit']").click(function (event){
    $(this).siblings(".mdl-textfield").addClass('is-invalid');
    $(this).siblings(".mdl-textfield").children(".mdl-textfield__input").prop('required', true);
});


function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    // var email = profile.getEmail();

    // console.log('profile', profile);

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
                // Handle or verify the server response if necessary.
                if (result) {
                    console.log('Auth Done', result);
                    window.location.href = "/catalog";
                }
                else {
                    alert('Failed to make a server-side call. Check your configuration and console.');
                }
            }
        });
    }
}