class Category {


    setFormData = (form_id, data) => {
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

    viewCategory = (uuid) => {
        let self = this;
        new AjaxService().getRequest(
            category_api_url + uuid + '/',
            function (response) {
                let category = response.data;
                self.setFormData('#categoryBasicInformationForm', category);
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
        let modal = $('#addFolderModal');
        $('#actionButtonAddFolder').off('click').on('click', function () {
            $('#addFolderModalForm')[0].reset();
            modal.find('#addFolderModalFormError').html("");
            modal.modal('show');
        });
        $(category).on('submit', '#addFolderModalForm', function (e) {
            e.preventDefault();
            const form = $('#addFolderModalForm').parsley();
            let payload = {
                name: $(this).find('#name').val(),
                is_active: $(this).find('#is_active').is(':checked'),
            }
            let parent_uuid = self.breadcrumbTrail[self.breadcrumbTrail.length - 1].uuid;

            if (parent_uuid !== "#") {
                payload.parent_uuid = parent_uuid;
            }

            new AjaxService().postRequest(
                category_api_url,
                payload,
                function (response) {
                    if (parent_uuid === "#") {
                        self.list();
                    } else {
                        self.list(parent_uuid);
                    }
                    modal.modal('hide');
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
                        $('#addFolderModalFormError').html(errorHtml);
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
