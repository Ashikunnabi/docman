/*
* =============================================================================
*                                   USER
* =============================================================================
**/

class User {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_user_management_a').click();
        $('#sidebar_option_user_management_user').addClass('active');
    };

    /*
    * =========================================================================
    *                       User in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#userDataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "ordering": false,
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add user',
                        id: 'addUserButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = user_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete user',
                        id: 'deleteUserButton',
                        class: 'btn btn-danger'
                    },
                    action: function (e, dt, node, config) {
                        let data = dt.rows(".selected").data();
                        // no table row selected
                        if (data[0] === undefined) {
                            notify('Please select an item', 'error');
                            return;
                        }
                        // table row selected so do further actions
                        Swal.fire({
                            title: 'Are you sure?',
                            text: "You won't be able to revert this!",
                            icon: 'warning',
                            showCancelButton: true,
                            confirmButtonColor: '#3085d6',
                            cancelButtonColor: '#d33',
                            confirmButtonText: 'Yes, delete it!'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
                                // do ajax request to delete
                                $.ajax({
                                    url: user_api_url + data[0].uuid + '/',
                                    headers: { "X-CSRFToken": csrf_token },
                                    type: "DELETE",
                                    success: function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'User has been deleted.',
                                            'success'
                                        );
                                        dt.ajax.reload()
                                    },
                                    error: function (response) {
                                        notify(response.responseJSON.detail, 'error');
                                    }
                                });
                            }
                        })
                    }
                },
                {
                    extend: 'copy',
                    exportOptions: { orthogonal: 'export' }
                },
                {
                    extend: 'pdf',
                    exportOptions: { orthogonal: 'export' }
                },
                {
                    extend: 'excel',
                    exportOptions: { orthogonal: 'export' }
                },
                {
                    extend: 'csv',
                    exportOptions: { orthogonal: 'export' }
                },
                {
                    extend: 'print',
                    exportOptions: { orthogonal: 'export' }
                },
            ],
            "lengthMenu": [30, 50, 80, 100, 200],
            "ajax": function (data, callback, settings) {
                let queryParams = $.param({
                    draw: data.draw,
                    start: data.start,
                    length: data.length,
                    search: data.search.value,
                    order: JSON.stringify(data.order),
                    // Add any additional parameters here
                });
                let url = `${user_api_url}?${queryParams}`;
                new AjaxService().getRequest(url, function (response) {
                    callback(response);
                }, function (response) {
                    notify(response.responseJSON.detail, 'error');
                })
            },
            "rowCallback": function (row, data, displayNum, displayIndex, dataIndex) {
                $(row).attr('title', 'Double click to edit')
            },
            "columns": [
                { "title": "SL", "data": "" },
                { "title": "Username", "data": "username" },
                { "title": "Email", "data": "email" },
                { "title": "Name", "data": "name" },
                { "title": "Phone", "data": "phone" },
                { "title": "Status", "data": "is_active" },
                { "title": "Action", "data": "" },
            ],
            "columnDefs": [
                {
                    targets: 0,
                    render: function (data, type, row, meta) {
                        return (table.page.info()['start'] + meta['row'] + 1);
                    }
                },
                {
                    "targets": [5],
                    "visible": true,
                    "searchable": true,
                    "render": function (data, type, row, meta) {
                        let active_html = `<i class="fa fa-solid fa-check color_green"></i>`
                        let inactive_html = `<i class="fa fa-times color_red"></i>`
                        if (type === "export") {
                            if (data) return "Active"
                            return "Inactive"
                        }
                        if (data) return active_html
                        return inactive_html
                    },
                },
                {
                    "targets": -1,
                    "data": null,
                    "render": function (data, type, row, meta) {
                        return `<a href="edit/${row.uuid}">
                            <button class="btn btn-outline-primary btn-sm actionButtonEdit" title="Edit">
                            >
                            </button>
                        </a>`
                    }

                }
            ],
        });

        // Single click row select the row and mark a different color
        // $('#userDataTable tbody').on('click', 'tr', function () {
        //     if ($(this).hasClass('selected')) {
        //         $(this).removeClass('selected');
        //     } else {
        //         table.$('tr.selected').removeClass('selected');
        //         $(this).addClass('selected');
        //     }
        // });

        // double click row will redirect to edit selected row
        $('#userDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.uuid;
        });
    };

    /*
    * =========================================================================
    *                       User add
    * =========================================================================
    **/

    add = () => {
        // add user
        $(document).on('submit', '#user_add', function (e) {
            e.preventDefault();
            const user_add_form = $('#user_add').parsley();
            let user_add_form_data = new FormData($('#user_add')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (user_add_form.isValid()) {
                // make form attributes request friendly
                if (user_add_form_data.has('password1')) user_add_form_data.delete('password1');
                if (!user_add_form_data.has('is_staff')) user_add_form_data.append('is_staff', 0);
                if (!user_add_form_data.has('is_active')) user_add_form_data.append('is_active', 0);
                // submit an ajax request to the api endpoint
                $.ajax({
                    url: user_api_url,
                    type: "POST",
                    headers: { "X-CSRFToken": csrf_token },
                    data: user_add_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        // Display a success message
                        notify("User has been created successfully.", "success");

                        // Delay the page refresh for 2 seconds (2000 milliseconds)
                        setTimeout(function () {
                            // Refresh the page
                            // location.reload();
                            window.location.href = user_list_url;
                        }, 2000); // Adjust the delay time as needed
                    },
                    error: function (response) {
                        let response_json = response.responseJSON
                        for (var field in response_json.error) {
                            if (response_json.error.hasOwnProperty(field)) {
                                var errorMessages = response_json.error[field];
                                for (var i = 0; i < errorMessages.length; i++) {
                                    notify(`${field.toUpperCase()}: ${errorMessages[i]}`, 'error');
                                }
                            }
                        }
                    }
                });
            }
        });
    };

    /*
    * =========================================================================
    *                       User edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        // edit user form value setup
        $.ajax({
            type: "get",
            url: `${user_api_url}`,
            success: function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'company_application_document') (value != null) ? $('#editCompanyApplicationDocument').attr('href', `/media/${value}`) : "";
                        else if (key === 'company_store_front') (value != null) ? $('#editCompanyStoreFront').attr('href', `/media/${value}`) : "";
                        else if (key === 'company_commercial_location') (value != null) ? $('#editCompanyCommercialLocation').attr('href', `/media/${value}`) : "";
                        else if (key === 'company_reseller_permit') (value != null) ? $('#editCompanyResellerPermit').attr('href', `/media/${value}`) : "";
                        else if (key === 'company_retail_sales_floor') (value != null) ? $('#editCompanyRetailSalesFloor').attr('href', `/media/${value}`) : "";
                        else if (key === 'is_staff') (value === true) ? $('input[name=is_staff]').click() : "";
                        else if (key === 'is_api_user') (value === true) ? $('input[name=is_api_user]').click() : "";
                        else if (key === 'is_active') (value === true) ? $('input[name=is_active]').click() : "";
                        else $('[name=' + key + ']', form).val(value);
                    });
                }

                populate($('#user_edit'), response.data);
                $('input[name=password]').val('')
            },
            error: function (response) {
                let response_json = response.responseJSON
                for (var field in response_json.error) {
                    if (response_json.error.hasOwnProperty(field)) {
                        var errorMessages = response_json.error[field];
                        for (var i = 0; i < errorMessages.length; i++) {
                            notify(`${field.toUpperCase()}: ${errorMessages[i]}`, 'error');
                        }
                    }
                }
            }
        });
    };

    /*
    * =========================================================================
    *                       User edit
    * =========================================================================
    **/

    edit = () => {
        // edit user
        $(document).on('submit', '#user_edit', function (e) {
            e.preventDefault();
            const user_edit_form = $('#user_edit').parsley();
            let user_edit_form_data = new FormData($('#user_edit')[0]);
            let csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


            if (user_edit_form.isValid()) {
                // make form attributes request friendly
                if (user_edit_form_data.has('password')) ($("input[name='password']").val() === '') ? user_edit_form_data.delete('password') : '';
                if (user_edit_form_data.has('password1')) user_edit_form_data.delete('password1');
                if (user_edit_form_data.has('company_application_document')) ($("input[name='company_application_document']").val() === '') ? user_edit_form_data.delete('company_application_document') : '';
                if (user_edit_form_data.has('company_store_front')) ($("input[name='company_store_front']").val() === '') ? user_edit_form_data.delete('company_store_front') : '';
                if (user_edit_form_data.has('company_commercial_location')) ($("input[name='company_commercial_location']").val() === '') ? user_edit_form_data.delete('company_commercial_location') : '';
                if (user_edit_form_data.has('company_reseller_permit')) ($("input[name='company_reseller_permit']").val() === '') ? user_edit_form_data.delete('company_reseller_permit') : '';
                if (user_edit_form_data.has('company_retail_sales_floor')) ($("input[name='company_retail_sales_floor']").val() === '') ? user_edit_form_data.delete('company_retail_sales_floor') : '';
                if (!user_edit_form_data.has('is_staff')) user_edit_form_data.append('is_staff', 0);
                if (!user_edit_form_data.has('is_api_user')) user_edit_form_data.append('is_api_user', 0);
                if (!user_edit_form_data.has('is_active')) user_edit_form_data.append('is_active', 0);

                // submit an ajax request to the api endpoint
                $.ajax({
                    url: user_api_url,
                    headers: { "X-CSRFToken": csrf_token },
                    type: "PATCH",
                    data: user_edit_form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (resp) {
                        // Display a success message
                        notify("User has been updated successfully.", "success");
                    },
                    error: function (response) {
                        let response_json = response.responseJSON
                        for (var field in response_json.error) {
                            if (response_json.error.hasOwnProperty(field)) {
                                var errorMessages = response_json.error[field];
                                for (var i = 0; i < errorMessages.length; i++) {
                                    notify(`${field.toUpperCase()}: ${errorMessages[i]}`, 'error');
                                }
                            }
                        }
                    }
                });
            }
        });
    };

    /*
    * =========================================================================
    *                    User account activation email
    * =========================================================================
    **/

    send_account_activation_email = () => {
        // edit user
        $(document).on('click', '#send_account_activation_email', function (e) {
            e.preventDefault();
            // submit an ajax request to the api endpoint
            Swal.fire({
                title: 'Are you sure?',
                text: "You are going to send an activation email!",
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, send it!'
            }).then((result) => {
                if (result.isConfirmed) {
                    $.ajax({
                        url: account_activation_email_send_api_url,
                        type: "POST",
                        data: { id: uuid },
                        success: function (resp) {
                            window.location.reload();
                        },
                        error: function (response) {
                            Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                text: response.responseJSON.data
                            })
                        }
                    });
                }
            });
        });
    };

    /*
    * =========================================================================
    *                User account activation email last sent at
    * =========================================================================
    **/

    last_account_activation_sent_at = () => {
        // show last account activation email sent at
        // submit an ajax request to the api endpoint
        $.ajax({
            url: last_account_activation_sent_at_api_url,
            type: "GET",
            data: { id: uuid },
            success: function (response) {
                if (response.data !== "") {
                    let text = `Last sent at: ${response.data}`;
                    $('#last_email_sent_at').html(text)
                }
            },
            error: function (response) {
                let response_json = response.responseJSON
                for (var field in response_json.error) {
                    if (response_json.error.hasOwnProperty(field)) {
                        var errorMessages = response_json.error[field];
                        for (var i = 0; i < errorMessages.length; i++) {
                            notify(`${field.toUpperCase()}: ${errorMessages[i]}`, 'error');
                        }
                    }
                }
            }
        });
    };

    sales_reps = () => {
        // set sales reps at user edit dropdown
        $.ajax({
            url: sales_reps_api_url + `?user=${uuid}`,
            type: "get",
            success: function (response) {
                $(document).ready(function () {
                    $('#sales_reps').select2({ data: response.detail });
                });
            },
            error: function (response) { }
        });

        $('#sales_reps_save_btn').on('click', function (e) {
            $.ajax({
                url: sales_reps_add_update_api_url + `?user=${uuid}`,
                data: JSON.stringify({ sales_reps: $('#sales_reps').val() }),
                dataType: 'json',
                contentType: "application/json",
                type: "post",
                success: function (response) {
                    window.location.reload();
                },
                error: function (response) {
                    console.log(response)
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
        this.select_sidebar_option();
        if (page === 'list') {
            this.list();
        }
        if (page === 'add') {
            this.add();
        }
        if (page === 'edit') {
            this.edit_form_value_set();
            this.edit();
        }
        // this.send_account_activation_email();
        // this.last_account_activation_sent_at();
        // this.sales_reps();
    }
}


new User().main();
