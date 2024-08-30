class Category {


    setFormData = (form_id, data) => {
        let self = this;
        let form = $(form_id);
        $.each(data, function (key, value) {
            let element = form.find(`#${key}`);
            if (element.is(':checkbox')) {
                element.prop('checked', value);
            } else {
                element.val(value);
            }
        });
    }

    pathGenerator = (category, ignore_current = true) => {
        let paths = [];
        let path = '';

        while (category) {
            paths.push({
                name: category.name,
                uuid: category.uuid
            });
            category = category.parent;
        }
        paths = paths.reverse();

        if (paths.length !== 0 && ignore_current) {
            paths.pop();
        }

        if (paths.length === 0) {
            path = `<span class="separator">/</span>`;
        }

        $.each(paths, function (key, value) {
            path += `<span class="separator">/</span> <a href="/category/edit/${value.uuid}/" class="breadcrumbItem">${value.name}</a> `;
        });
        return path;
    }

    viewCategory = (uuid) => {
        let self = this;
        new AjaxService().getRequest(
            category_api_url + uuid + '/',
            function (response) {
                let category = response.data;
                self.setFormData('#categoryBasicInformationForm', category);
                $('#categoryBasicInformationForm').find('#path').html(self.pathGenerator(category));
            },
            function (response) {
                let response_json = response.responseJSON;
                if (response_json.code === "NOT_FOUND") {
                    form.find('#categoryBasicInformationFormError').html(
                        `<div class="alert alert-danger">
                            <strong>Error:</strong> ${response_json.message}
                        </div>`
                    );
                }
            }
        );
    }

    editCategory = () => {
        let self = this;
        $(document).on('submit', '#categoryBasicInformationForm', function (e) {
            e.preventDefault();
            const form = $('#categoryBasicInformationForm').parsley();
            let payload = {
                name: $(this).find('#name').val(),
                is_active: $(this).find('#is_active').is(':checked'),
            }

            new AjaxService().patchRequest(
                category_api_url + uuid + '/',
                payload,
                function (response) {
                    notify('Success', 'success');
                },
                function (response) {
                    let response_json = response.responseJSON
                    if (response_json.code === "BAD_REQUEST") {
                        let errorHtml = `
                            <div class="alert alert-danger">
                                <strong>Error:</strong> ${response_json.message}
                            </div>`;
                        $.each(response_json.error, function (key, value) {
                            if (Array.isArray(value)) {
                                $.each(value, function (k, v) {
                                    errorHtml += `${key.toUpperCase().replace(/_/g, ' ')}: ${v}<br>`;
                                })
                            }
                        })
                        $('#editCategoryBasicInformationFormError').html(errorHtml);
                    }
                }
            );
        });
    }

    groupPermissions = () => {
        let self = this;
        new AjaxService().getRequest(
            category_group_permission_api_url,
            function (response) {
                let group_permissions = response.data;
                let groupPermissionTable = $('#groupPermissionTable');
                let table_head = groupPermissionTable.find('thead');
                let table_body = groupPermissionTable.find('tbody');
                table_body.html('');

                let table_headers = ["Group"]
                $.each(group_permissions[0].permission_names, function (key, value) {
                    table_headers.push(value[1]);
                });
                $.each(table_headers, function (key, value) {
                    table_head.append(`<th>${value}</th>`);
                });



                function permissionColumns(data) {
                    let permissions = data.permissions
                    let columns = '';
                    $.each(permissions, function (key, value) {
                        columns += `<td>
                            <input type="checkbox" 
                            class="actionButtonAddDeleteGroupPermission"
                            data-group-id="${value.group_id}" 
                            data-category-permission-id="${value.category_permission_id}" 
                            data-category-group-permission-uuid="${value.category_group_permission_uuid}"
                             ${value.has_permission ? 'checked' : ''}
                             >
                        </td>`;
                    });
                    return columns;
                }


                $.each(group_permissions, function (key, value) {
                    let tr = `<tr>
                        <td>${value.name}</td>
                        ${permissionColumns(value)}
                        </tr>`;
                    table_body.append(tr);
                });
            },
            function (response) {
                let response_json = response.responseJSON;
                if (response_json.code === "NOT_FOUND") {
                    $('#editCategoryBasicInformationFormError').html(
                        `<div class="alert alert-danger">
                            <strong>Error:</strong> ${response_json.message}
                        </div>`
                    );
                }
            }
        );
    }

    addDeleteGroupPermission = () => {
        let self = this;
        $(document).on('change', '.actionButtonAddDeleteGroupPermission', function (e) {
            let current_checkbox = $(this);
            current_checkbox.attr('disabled','disabled');
            let category_group_permission_uuid = current_checkbox.data('category-group-permission-uuid');
            let category_permission_id = current_checkbox.data('category-permission-id');
            let group_id = current_checkbox.data('group-id');
            let has_permission = current_checkbox.is(':checked');
            let payload = {
                permission_id: category_permission_id,
                group_id: group_id
            }
            console
            if (has_permission) {
                new AjaxService().postRequest(
                    category_group_permission_api_url,
                    payload,
                    function (response) {
                        notify('Success', 'success');
                        current_checkbox.data('category-group-permission-uuid', response.data.uuid);
                        current_checkbox.removeAttr('disabled');
                    },
                    function (response) {
                        current_checkbox.removeAttr('disabled');
                        let response_json = response.responseJSON;
                        if (response_json.code === "BAD_REQUEST") {
                            $('#editCategoryBasicInformationFormError').html(
                                `<div class="alert alert-danger">
                                <strong>Error:</strong> ${response_json.message}
                            </div>`
                            );
                        }
                    }
                );
            } else {
                new AjaxService().deleteRequest(
                    category_group_permission_api_url + group_id + '/' + 'category-group-permission' + '/' + category_group_permission_uuid + '/',
                    function (response) {
                        notify('Success', 'success');
                        current_checkbox.removeAttr('disabled');
                    },
                    function (response) {
                        current_checkbox.removeAttr('disabled');
                        let response_json = response.responseJSON;
                        if (response_json.code === "BAD_REQUEST") {
                            $('#editCategoryBasicInformationFormError').html(
                                `<div class="alert alert-danger">
                                <strong>Error:</strong> ${response_json.message}
                            </div>`
                            );
                        }
                    }
                );
            }
        });
    }


    main = () => {
        if (page === 'edit') {
            if (!hasPermission('category.view_category')) {
                $('.actionButtonViewFolder').hide();
            } else {
                this.viewCategory(uuid);
            }
            if (!hasPermission('category.change_category')) {
                $('.actionButtonViewFolder').hide();
            } else {
                this.editCategory();
            }
            if (!hasPermission('category.view_categorygrouppermission')) {
                $('#groupPermissionTable').parent().parent().parent().parent().hide();
            } else {
                this.groupPermissions();
            }
            if (!hasPermission('category.add_categorygrouppermission')) {
                $('.actionButtonAddDeleteGroupPermission').hide();
            } else {
                this.addDeleteGroupPermission();
            }
        }
    }
}


new Category().main();
