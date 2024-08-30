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

        while (category.parent) {
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
        }
    }
}


new Category().main();
