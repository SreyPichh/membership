$(document).ready(function () {
    $("#img-submit").hide();
    var user_id = $('#user_id').val();
    var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();

    console.log(user_id, csrfmiddlewaretoken);

    $('#save_contact_info').on('submit', function (e) {
        e.preventDefault();
        // noinspection JSAnnotator
        var user_info = {
            name: $('#name').val(),
            surname: $('#surname').val(),
            email: $('#email').val(),
            phone: $('#phone').val()
        };
        console.log(user_info);
        $.ajax({
            type: 'POST',
            url: '/edit_user_info_profile/',
            data: {
                name: user_info.name,
                surname: user_info.surname,
                email: user_info.email,
                phone: user_info.phone,
                csrfmiddlewaretoken: csrfmiddlewaretoken
            },
            success: function (e) {
                toastr.success(e, {timeOut: 5000});
            }
        });
    });

    $('#save_address_info').on('submit', function (e) {
        e.preventDefault();

        var user_address = {
            state: $('#state').val(),
            city: $('#city').val(),
            street: $('#street').val(),
            house_number: $('#house_number').val(),
            zip: $('#zip').val()
        };
        console.log(user_address);
        $.ajax({
            type: 'POST',
            url: '/edit_address_profile/',
            data: {
                state: user_address.state,
                city: user_address.city,
                street: user_address.street,
                house_number: user_address.house_number,
                zip: user_address.zip,
                csrfmiddlewaretoken: csrfmiddlewaretoken
            },
            success: function (e) {
                toastr.success(e, {timeOut: 5000});
            }
        });

    });

    /*$('#img_profile').on('change', function () {
        console.log(new FormData(this));
        console.log($('#img_profile').attr("enctype"));
        console.log($('#reg-form-img').attr("value"));
        $.ajax({
            type: 'POST',
            enctype: $('#img_profile').attr("enctype"),
            url: '/edit_profile_picture/',
            async: false,
            cache: false,
            processData: false,
            contentType: false,
            data: {
                image: new FormData(this),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (e) {
                // Rollback Success
                $('#profile_pic').attr("src", e);
            },
            error: function () {
                // Handle Error
            }
        });
    });*/

    $(function () {
        $("#reg-form-img").change(function () {
            $("#img-submit").show();
            var file = this.files[0];
            var imagefile = file.type;
            var match = ["image/jpeg", "image/png", "image/jpg"];
            if (!((imagefile === match[0]) || (imagefile === match[1]) || (imagefile === match[2]))) {
                return false;
            }
            else {
                var reader = new FileReader();
                reader.onload = imageIsLoaded;
                reader.readAsDataURL(this.files[0]);
                /*console.log(typeof(formData));
                jQuery.ajax({
                    type: 'POST',
                    enctype: 'multipart/form-data',
                    url: '/edit_profile_picture/',
                    async: false,
                    cache: false,
                    processData: false,
                    data: file,
                    contentType: 'application/json',
                    headers: { "X-CSRFToken": csrfmiddlewaretoken },
                    success: function (e) {
                        // Rollback Success
                        console.log(e);
                        $('#profile_pic').attr("src", e);
                    },
                    error: function () {
                        // Handle Error
                    }
                });*/
            }
        });
    });

    function imageIsLoaded(e) {
        $("#profile_pic").attr('src', e.target.result);
    }

});

// *******************************************
