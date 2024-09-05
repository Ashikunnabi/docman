/*
* =============================================================================
*                                   LOGIN
* =============================================================================
**/

class Login {

    /*
    * =========================================================================
    *                       Log into the system
    * =========================================================================
    **/

    remember_me = () => {

        // Check for saved credentials in localStorage
        if (localStorage.getItem('rememberMe') === 'true') {
            $('input[type="text"]').val(localStorage.getItem('username'));
            $('input[type="password"]').val(localStorage.getItem('password'));
            $('#rememberMe').prop('checked', true);
        }
    }

    login = () => {
        let self = this;
        $(document).on('submit', '#login-form', function (e) {
            e.preventDefault();
            const login_form = $('#login-form').parsley();
            let login_form_data = new FormData($('#login-form')[0]);
            let rememberMe = $('#rememberMe').is(':checked');

            let data = {
                username: login_form_data.get('username'),
                password: login_form_data.get('password')
            };

            if (login_form.isValid()) {
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: login_api_url,
                    type: "POST",
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: function (resp) {
                        // Save credentials if 'Remember Me' is checked
                        if (rememberMe) {
                            localStorage.setItem('rememberMe', 'true');
                            localStorage.setItem('username', data.username);
                            localStorage.setItem('password', data.password);
                        } else {
                            localStorage.removeItem('rememberMe');
                            localStorage.removeItem('username');
                            localStorage.removeItem('password');
                        }
                        setLocalWithExpiry('access', resp.data.access, 86400000);
                        setLocalWithExpiry('refresh', resp.data.refresh, 86400000);
                        setLocalWithExpiry('user', resp.data.user, 86400000);
                        self.permissions();
                    },
                    error: function (response) {
                        notify(response.responseJSON.message, 'error');
                    }
                });
            }
        });
    };


    permissions = () => {
        let self = this;
        const ajaxService = new AjaxService();

        ajaxService.getRequest(permission_api_url,
            function success(response) {
                setLocalWithExpiry('permissions', response.data, 86400000);
                window.location.reload();
            },
            function error(response) {
                console.log('Error:', response);
            }
        );

    };


    banner = () => {
        let self = this;
        $.ajax({
            url: login_page_banner_api_url,
            type: "GET",
            success: function (resp) {
                if (resp.data.length < 1) {
                    $('.promotional-section').hide();
                    $('#login-page').css('width', '30%');
                    $('#login_page_body').css('width', '100%');
                    return;
                }
                $.map(resp.data, function (value, index) {
                    if (value.human_readable_page === 'Login page') {
                        $(".promotional-section").append(`                        
                            <a href="${value.redirect_url}">
                                <img src="data:image/png;base64, ${value.image}" alt="${value.title}">
                            </a>
                        `);
                    }
                })
            },
            error: function (response) {
                console.log(response)
            }
        });
    };

    /*
    * =========================================================================
    *                       Main function of this class
    * =========================================================================
    **/

    main = () => {
        // call this function to execute all operations of this class
        this.remember_me();
        this.login();
        // this.banner();
    }
}


/*
* =============================================================================
*                                   registration
* =============================================================================
**/

class registration {

    /*
    * =========================================================================
    *                     Register a new user to the system
    * =========================================================================
    **/

    registration = () => {
        $(document).on('submit', '#registration-form', function (e) {
            e.preventDefault();
            const registration_form = $('#registration-form').parsley();
            let registration_form_data = new FormData($('#registration-form')[0]);

            if (registration_form.isValid()) {
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: registration_api_url,
                    type: "POST",
                    data: registration_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        window.location.href = '/login/?next=/&r=1';
                    },
                    error: function (response) {
                        if (response.status === 422) {
                            let errors = '';
                            $.map(response.responseJSON.details, function (v, i) {
                                $.each(v, function (j, k) {
                                    errors += `<li>${i}: ${k}</l1>`;
                                })
                            });
                            let final_error = `<ul>${errors}</ul>`;

                            $('.registration-failed')
                                .html(final_error)
                                .css('display', 'block')
                        }
                    }
                });
            }
        });
    };

    /*
    * =========================================================================
    *                       Main function of this class
    * =========================================================================
    **/

    main = () => {
        // call this function to execute all operations of this class
        this.registration();
    }
}


/*
* =============================================================================
*                                   ACCOUNT ACTIVATION
* =============================================================================
**/

class AccountActivation {

    /*
    * =========================================================================
    *                     Active a new user's account
    * =========================================================================
    **/

    activation = () => {
        $(document).ready(function (e) {
            $('#account_activation_loading').css('display', 'block');
            $('#account_activation_success').css('display', 'none');
            $('#account_activation_failed').css('display', 'none');
            // submit an ajax request to the api endpoint
            $.ajax({
                url: `${account_activation_api_url}?rt=${rt}&au=${au}`,
                type: "GET",
                success: function (resp) {
                    $('#account_activation_loading').css('display', 'none');
                    $('#account_activation_success').css('display', 'block');
                    $('#account_activation_failed').css('display', 'none');
                },
                error: function (response) {
                    $('#account_activation_loading').css('display', 'none');
                    $('#account_activation_success').css('display', 'none');
                    $('#account_activation_failed').css('display', 'block');
                }
            });
        });
    };

    /*
    * =========================================================================
    *                       Main function of this class
    * =========================================================================
    **/

    main = () => {
        // call this function to execute all operations of this class
        this.activation();
    }
}


/*
* =============================================================================
*                               RECOVER PASSWORD
* =============================================================================
**/

class RecoverPassword {
    send_email = () => {
        $(document).on('submit', '#recover-form-1', function (e) {
            e.preventDefault();
            const form = $('#recover-form-1').parsley();
            let form_data = new FormData($('#recover-form-1')[0]);

            if (form.isValid()) {
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: recover_api_url,
                    type: "POST",
                    data: form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        $('#message').show()
                    },
                    error: function (response) {
                        if (response.status === 422) {
                            let errors = '';
                            $.map(response.responseJSON.details, function (v, i) {
                                $.each(v, function (j, k) {
                                    errors += `<li>${i}: ${k}</l1>`;
                                })
                            });
                            let final_error = `<ul>${errors}</ul>`;

                            $('.registration-failed')
                                .html(final_error)
                                .css('display', 'block')
                        }
                    }
                });
            }
        });
    };

    recover = () => {
        $(document).on('submit', '#recover-form', function (e) {
            e.preventDefault();
            const form = $('#recover-form').parsley();
            let form_data = new FormData($('#recover-form')[0]);

            if (form.isValid()) {
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: recover_password_now_api_url,
                    type: "POST",
                    data: form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        $('#recover_submit').attr('disabled', 'disabled');
                        $('#message').show()
                        setTimeout(function (e) {
                            window.location.href = '/login/';
                        }, 5000)
                    },
                    error: function (response) {
                        if (response.status === 422) {
                            let errors = '';
                            $.map(response.responseJSON.details, function (v, i) {
                                $.each(v, function (j, k) {
                                    errors += `<li>${i}: ${k}</l1>`;
                                })
                            });
                            let final_error = `<ul>${errors}</ul>`;

                            $('.registration-failed')
                                .html(final_error)
                                .css('display', 'block')
                        }
                    }
                });
            }
        });
    };

    /*
    * =========================================================================
    *                       Main function of this class
    * =========================================================================
    **/

    main = () => {
        // call this function to execute all operations of this class
        this.registration();
    }
}


new Login().main();
new registration().main();
if (account_activation_page) {
    new AccountActivation().main();
}
if (recover_password_page) {
    new RecoverPassword().send_email();
    new RecoverPassword().recover();
}
