$(function() {
    $('#upload-btn').click(function() {
        var form_data = new FormData($('#upload-form')[0]);
        console.log(form_data)
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
            },
        });
    });
});