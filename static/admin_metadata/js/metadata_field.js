/*
* =============================================================================
*                             Metadata
* =============================================================================
**/

class Field {
    /*
    * =========================================================================
    *                       Active sidebar option
    * =========================================================================
    **/
    select_sidebar_option = () => {
        $('#sidebar_option_user_management_a').click();
        $('#sidebar_option_user_management_group').addClass('active');
    };

    /*
    * =========================================================================
    *                       Metadata in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#fieldDataTable').DataTable({
            "fixedHeader": {
                header: true,
                footer: true
            },
            scrollY: '50vh',
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add Field',
                        id: 'addFieldButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = fields_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete F',
                        id: 'deleteFieldButton',
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
                                new AjaxService().deleteRequest(
                                    fieldlist_api_urls + data[0].uuid + '/',
                                    function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Field has been deleted.',
                                            'success'
                                        );
                                        dt.ajax.reload()
                                    },
                                    function (response) {
                                        let response_json = response.responseJSON
                                        if (response_json.code === "USER_DELETION_NOT_ALLOWED") {
                                            notify("You are not allowed to delete an user.", "error");
                                        }
                                        notify(response.responseJSON.message, 'error');
                                    }
                                );
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
                // {
                //     extend: 'print',
                //     title: 'USERS',
                //     messageTop: '<h5 class="text-center">Group List</h5>',
                //     messageBottom: null
                // }
            ],
            "lengthMenu": [10, 25, 50, 75, 100],
            "ajax": function (data, callback, settings) {
                let queryParams = $.param({
                    draw: data.draw,
                    start: data.start,
                    length: data.length,
                    search: data.search.value,
                    order: JSON.stringify(data.order),
                    // Add any additional parameters here
                });
                let url = `${fieldlist_api_urls}?${queryParams}`;
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
                { "title": "Name", "data": "name" },
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
                    targets: 1,
                    render: function (data, type, row, meta) {
                        // let count = row.user.length
                        return `${data}`;
                    }
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
        $('#fieldDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#fieldDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.uuid;
        });
    };

    /*
    * =========================================================================
    *                      Metadata Group edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        // edit group form value setup
        new AjaxService().getRequest(
            fieldlist_api_urls + uuid + '/',
            function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'field_edit') {
                            let uuids = value.map(function (v) { return v.uuid });
                            $('#members_list').multiSelect('select', uuids.map(String))
                        }
                        if (key === 'permissions') {
                            let codenames = value.map(function (v) { return v.codename });
                            $('#permissions_list').multiSelect('select', codenames.map(String))
                        }
                        else $('[name=' + key + ']', form).val(value);
                    });
                }
                setTimeout(function (e) {
                    populate($('#group_edit'), response.data);
                }, 3000)
            },
            function (response) {
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
        );
    };


    /*
   * =========================================================================
   *                            SAVE Metadata GROUP
   * =========================================================================
   **/
    save = () => {
        let self = this;
        $(document).on('click', '.submit_btn', function (e) {
            e.preventDefault();
            if ($('#name').val() == "") {
                notify('Field name required!', 'error', 5000);
                return;
            }
            let data = {
                name: $('#name').val(),
                is_active: $('#is_active').is(':checked'),
                users: $('#members_list').val(),
                permissions: $('#permissions_list').val(),
            }
            let url = fieldlist_api_urls

            if (page === "add") {
                new AjaxService().postRequest(
                    url,
                    data,
                    function (response) {
                        notify('Success', 'success', 3000);
                        if (page === "add") {
                            setTimeout(function (e) {
                                window.location.href = metadata_list_url;
                            }, 4000)
                        }

                    },
                    function (response) {
                        let response_json = response.responseJSON
                        console.log(response_json)
                        if (response_json.code === "NOT_ALLOWED") {
                            notify("You are not allowed to add a new field.", "error");
                        }
                    }
                );
            }

            if (page === "edit") {
                url = fieldlist_api_urls + uuid + "/"
                new AjaxService().patchRequest(
                    url,
                    data,
                    function (response) {
                        notify('Success', 'success', 3000);
                        if (page === "add") {
                            setTimeout(function (e) {
                                window.location.href = metadata_list_url;
                            }, 4000)
                        }

                    },
                    function (response) {
                        let response_json = response.responseJSON
                        console.log(response_json)
                        if (response_json.code === "NOT_ALLOWED") {
                            notify("You are not allowed to add a new field.", "error");
                        }
                    }
                );
            }
        })
    }

    /*
   * =========================================================================
   *                       Main function of this class
   * =========================================================================
   **/

    main = () => {
        // call this function to execute all operations of this class
        this.select_sidebar_option()
        this.list()
        this.members()
        this.permissions()
        if (page === "edit") {
            this.edit_form_value_set();
        }
        this.save()
    }
}


new Field().main();
