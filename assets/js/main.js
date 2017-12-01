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


function signInCallback(authResult) {
    console.log(authResult);
    if( authResult['code']) {

        // Send the one-time-use code to the server, if the server responds,
        // write a 'login successful' message to the web page and then redirect
        // back to the main page.
        var state = $('#state').val();
        console.log('state', state);

        $.ajax({
            type: 'POST',
            url: '/gconnect?state=' + state,
            processData: false,
            data: authResult['code'],
            contentType: 'application/octet-stream; charset=utf-8',
            success: function(result) {
                // Handle or verify the server response if necessary.
                if (result) {
                    console.log('Auth Done', result);
                    window.location.href = "/catalog";
                } else if (authResult['error']) {
                    console.log('There was an error: ' + authResult['error']);
                } else {
                    alert('Failed to make a server-side call. Check your configuration and console.');
                }
            }
        });
    }
}