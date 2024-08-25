/*
* =============================================================================
*                             GROUP
* =============================================================================
**/

class GroupActivityLog {
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
    *                       Group in Datatable
    * =========================================================================
    **/
    list = () => {
        let self = this;

        let table = $('#groupDataTable').DataTable({
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": '<"mb-3"B>flrtip',
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add group',
                        id: 'addGroupButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = group_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete group',
                        id: 'deleteGroupButton',
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
                                    api_urls["group_list"] + data[0].id + '/',
                                    function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Group has been deleted.',
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
                let url = `${api_urls["group_list"]}?${queryParams}`;
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
                        return `<a href="edit/${row.id}">
                            <button class="btn btn-outline-primary btn-sm actionButtonEdit" title="Edit">
                            >
                            </button>
                        </a>`
                    }

                }
            ],
        });

        // Single click row select the row and mark a different color
        $('#groupDataTable tbody').on('click', 'tr', function () {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

        // double click row will redirect to edit selected row
        $('#groupDataTable tbody').on('dblclick', 'tr', function () {
            let data = table.row(this).data();
            window.location = 'edit/' + data.id;
        });
    };

    /*
   * =========================================================================
   *                       Members (Staff Users)
   * =========================================================================
   **/
    members = () => {
        let self = this;
        new AjaxService().getRequest(
            api_urls["user_list"],
            function (response) {
                let html = "";
                $.each(response.data, function (i, v) {
                    html += `
                        <option value="${v.uuid}">${v.email}</option>
                    `
                })
                $('#members_list').append(html)
                $('#members_list').multiSelect({
                    selectableHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='Search for selection'>",
                    selectionHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='Search selected'>",
                    afterInit: function (ms) {
                        var that = this,
                            $selectableSearch = that.$selectableUl.prev(),
                            $selectionSearch = that.$selectionUl.prev(),
                            selectableSearchString = '#' + that.$container.attr('uuid') + ' .ms-elem-selectable:not(.ms-selected)',
                            selectionSearchString = '#' + that.$container.attr('uuid') + ' .ms-elem-selection.ms-selected';

                        that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
                            .on('keydown', function (e) {
                                if (e.which === 40) {
                                    that.$selectableUl.focus();
                                    return false;
                                }
                            });

                        that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
                            .on('keydown', function (e) {
                                if (e.which == 40) {
                                    that.$selectionUl.focus();
                                    return false;
                                }
                            });
                    },
                    afterSelect: function () {
                        this.qs1.cache();
                        this.qs2.cache();
                    },
                    afterDeselect: function () {
                        this.qs1.cache();
                        this.qs2.cache();
                    }
                });
            },
            function (response) {
                $('#nav-members').hide()
                notify('Something went wrong in members tab', 'error', 5000);
                console.log(response)
            }
        );

    }

    /*
   * =========================================================================
   *                       Permissions
   * =========================================================================
   **/
    permissions = () => {
        let self = this;
        new AjaxService().getRequest(
            api_urls["permission_list"],
            function (response) {
                let html = "";
                $.each(response.data, function (i, v) {
                    html += `
                        <option value="${v.codename}">${v.name}</option>
                    `
                })
                $('#permissions_list').append(html)
                $('#permissions_list').multiSelect({
                    selectableHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='Search for selection'>",
                    selectionHeader: "<input type='text' class='search-input' autocomplete='off' placeholder='Search selected'>",
                    afterInit: function (ms) {
                        var that = this,
                            $selectableSearch = that.$selectableUl.prev(),
                            $selectionSearch = that.$selectionUl.prev(),
                            selectableSearchString = '#' + that.$container.attr('codename') + ' .ms-elem-selectable:not(.ms-selected)',
                            selectionSearchString = '#' + that.$container.attr('codename') + ' .ms-elem-selection.ms-selected';

                        that.qs1 = $selectableSearch.quicksearch(selectableSearchString)
                            .on('keydown', function (e) {
                                if (e.which === 40) {
                                    that.$selectableUl.focus();
                                    return false;
                                }
                            });

                        that.qs2 = $selectionSearch.quicksearch(selectionSearchString)
                            .on('keydown', function (e) {
                                if (e.which == 40) {
                                    that.$selectionUl.focus();
                                    return false;
                                }
                            });
                    },
                    afterSelect: function () {
                        this.qs1.cache();
                        this.qs2.cache();
                    },
                    afterDeselect: function () {
                        this.qs1.cache();
                        this.qs2.cache();
                    }
                });
            },
            function (response) {
                $('#nav-permissions').hide()
                notify('Something went wrong in permissions tab', 'error', 5000);
                console.log(response)
            }
        );

    }

    /*
    * =========================================================================
    *                       Group edit form setup
    * =========================================================================
    **/

    edit_form_value_set = () => {
        // edit group form value setup
        new AjaxService().getRequest(
            api_urls["group_list"] + uuid + '/',
            function (response) {
                function populate(form, data) {
                    $.each(data, function (key, value) {
                        if (key === 'users') {
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
   *                            SAVE GROUP
   * =========================================================================
   **/
    save = () => {
        let self = this;
        $(document).on('click', '.submit_btn', function (e) {
            e.preventDefault();
            if ($('#name').val() == "") {
                notify('Group name required!', 'error', 5000);
                return;
            }
            let data = {
                name: $('#name').val(),
                is_active: $('#is_active').is(':checked'),
                users: $('#members_list').val(),
                permissions: $('#permissions_list').val(),
            }
            let url = api_urls["group_list"]

            if (page === "add") {
                new AjaxService().postRequest(
                    url,
                    data,
                    function (response) {
                        notify('Success', 'success', 3000);
                        if (page === "add") {
                            setTimeout(function (e) {
                                window.location.href = group_list_url;
                            }, 4000)
                        }

                    },
                    function (response) {
                        let response_json = response.responseJSON
                        console.log(response_json)
                        if (response_json.code === "NOT_ALLOWED") {
                            notify("You are not allowed to add a new group.", "error");
                        }
                    }
                );
            }

            if (page === "edit") {
                url = api_urls["group_list"] + uuid + "/"
                new AjaxService().patchRequest(
                    url,
                    data,
                    function (response) {
                        notify('Success', 'success', 3000);
                        if (page === "add") {
                            setTimeout(function (e) {
                                window.location.href = group_list_url;
                            }, 4000)
                        }

                    },
                    function (response) {
                        let response_json = response.responseJSON
                        console.log(response_json)
                        if (response_json.code === "NOT_ALLOWED") {
                            notify("You are not allowed to add a new group.", "error");
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


new GroupActivityLog().main();
