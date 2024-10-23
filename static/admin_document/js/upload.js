class Upload {
    generate = () => {
        let self = this;
        const dropzone = new Dropzone(".dropzone", {
            maxFiles: 1,
            url: document_api_url,
            headers: {
                "Authorization": `JWT ${getLocalWithExpiry("access")}`
            },
            previewTemplate: document.querySelector("#dropzone-template").innerHTML,
        });

        dropzone.on("success", function (file, response) {
            $(file.previewTemplate).find('.dz-remove').attr('data-uuid', response.data.uuid);
        });

        dropzone.on("error", function (file, response) {
            if (response.message) {
                $(file.previewTemplate).find('.dz-error-message').text(response.message);
                notify(response.message, 'error');
            }
        });

        dropzone.on("removedfile", function (file) {
            let uuid = $(file.previewTemplate).find('.dz-remove').attr('data-uuid');
            if (!uuid) {
                console.log('No uuid found');
                return;
            }
            let url = `${document_api_url}${uuid}/`;
            new AjaxService().deleteRequest(
                url,
                function (response) {
                    console.log('Document deleted successfully');
                },
                function (response) {
                    console.log('Error deleting document');
                }
            );
        });

        // mock push existing files from server
        new AjaxService().getRequest(
            document_api_url,
            function (response) {
                response.data.forEach((document) => {
                    let mockFile = {
                        name: document.name,
                        size: document.size,
                        dataURL: document.file,
                        accepted: true,
                        status: Dropzone.ADDED,
                        uuid: document.uuid
                    };
                    dropzone.emit("addedfile", mockFile);
                    dropzone.emit("thumbnail", mockFile, document.file);
                    dropzone.emit("complete", mockFile);
                    dropzone.files.push(mockFile);
                    $(mockFile.previewTemplate).find('.dz-remove').attr('data-uuid', document.uuid);
                });
            },
            function (response) {
                console.log('Error fetching documents');
            }
        );
    }

    textField = (field) => {
        return `<div class="form-group">
            <label for="${field.uuid}">${field.name}${field.is_required ? '<span class="text-danger">*</span>' : ''}</label>
            <input type="text" class="form-control" id="${field.uuid}" name="${field.uuid}" placeholder="${field.placeholder}" ${field.is_required ? 'required' : ''}>
        </div>`;
    }

    integerField = (field) => {
        return `<div class="form-group">
            <label for="${field.uuid}">${field.name}${field.is_required ? '<span class="text-danger">*</span>' : ''}</label>
            <input type="number" class="form-control" id="${field.uuid}" name="${field.uuid}" placeholder="${field.placeholder}" ${field.is_required ? 'required' : ''}>
        </div>`;
    }

    emailField = (field) => {
        return `<div class="form-group">
            <label for="${field.uuid}">${field.name}${field.is_required ? '<span class="text-danger">*</span>' : ''}</label>
            <input type="email" class="form-control" id="${field.uuid}" name="${field.uuid}" placeholder="${field.placeholder}" ${field.is_required ? 'required' : ''}>
        </div>`;
    }

    dynamicFormFields = (metadata) => {
        let formFields = `<fieldset class="border p-2">
            <legend class="w-auto" data-uuid=${metadata.uuid}>${metadata.name}</legend>`;

        let fields = metadata.fields;
        fields.forEach((field) => {
            if (field.field_type === 'integer') {
                formFields += this.integerField(field);
            } else if (field.field_type === 'email') {
                formFields += this.emailField(field);
            } else {
                formFields += this.textField(field);
            }
        });
        formFields += `</fieldset>`;
        return formFields;
    }

    addButtonToReadDocumentName = () => {
        let documentUploadform = $("#documentUploadMetadataForm")
        let document_name = documentUploadform.find("#__document_name");
        let button = `<button type="button" class="btn btn-primary btn-sm float-right mt-2" id="read-document-name">Read from document</button>`;
        document_name.after(button);
        documentUploadform.on('click', '#read-document-name', function () {
            let files = Dropzone.forElement(".dropzone").files;
            if (files.length < 1) {
                notify('Please upload a document', 'error');
                return;
            }
            let file = files[0];
            let document_name = file.name.split('.').slice(0, -1).join('.');
            documentUploadform.find("#__document_name").val(document_name);
        });
    }


    fetchAndRenderMetadata = (category_uuid) => {
        let self = this;
        let documentUploadform = $("#documentUploadMetadataForm")
        let metadata_section = documentUploadform.find("#metadata-section");
        metadata_section.empty();
        let metadata_html = '';
        if (!category_uuid) {
            return;
        }
        let url = `${category_api_url}${category_uuid}/`;
        new AjaxService().getRequest(
            url,
            function (response) {
                let static_metadata = {
                    "uuid": null,
                    "name": "Document Information",
                    "is_active": true,
                    "fields": [
                        {
                            "uuid": "__document_name",
                            "name": "Document Name",
                            "placeholder": "Document Name",
                            "field_type": "text",
                            "is_required": true,
                            "is_unique": false,
                            "is_active": true
                        }
                    ]
                }
                metadata_html += self.dynamicFormFields(static_metadata);

                let metadatas = response.data.metadata;
                $.each(metadatas, function (index, metadata) {
                    metadata_html += self.dynamicFormFields(metadata);
                });
                metadata_section.html(metadata_html);

                // restart parsley validation
                documentUploadform.parsley().reset();

                // add button to read document name
                self.addButtonToReadDocumentName();

            },
            function (response) {
                console.log('Error fetching metadata');
            }
        );
    }

    getAvailableCategories = () => {
        let self = this;
        let documentUploadform = $("#documentUploadMetadataForm")
        let category_dropdown = documentUploadform.find("#__category_uuid");

        category_dropdown.select2({
            ajax: {
                url: category_api_url,
                dataType: 'json',
                delay: 250, // Delay in ms before the request is sent
                headers: {
                    "Authorization": `JWT ${getLocalWithExpiry("access")}`
                },
                data: function (params) {
                    return {
                        search: params.term // Search query term
                    };
                },
                processResults: function (response) {
                    // Transform the response into the format expected by Select2
                    return {
                        results: response.data.map(item => ({
                            id: item.uuid,
                            text: item.path
                        }))
                    };
                },
                cache: true // Cache results to reduce API calls
            },
            minimumInputLength: 1, // Minimum input length to trigger search
            placeholder: 'Search...',
            allowClear: true
        });

        category_dropdown.on('select2:select', function (e) {
            let data = e.params.data;
            self.fetchAndRenderMetadata(data.id);
        });
    }

    submitDocument = () => {
        let self = this;
        let documentUploadform = $("#documentUploadMetadataForm")
        documentUploadform.on('submit', function (e) {
            e.preventDefault();
            documentUploadform.parsley().validate();
            if (!documentUploadform.parsley().isValid()) {
                return false;
            }
            let metadata = {};
            let url = document_api_url + 'upload/';
            let data = documentUploadform.serializeArray();
            let document_uuids = $('.dz-remove').map(function () {
                return $(this).attr('data-uuid');
            });

            data.forEach((field) => {
                if (field.name.startsWith('__')) {
                    return;
                }
                metadata[field.name] = field.value;
            });

            let upload_data = {
                metadata: metadata,
                document_uuids: Array.from(document_uuids),
                category_uuid: documentUploadform.find("#__category_uuid").val()
            };

            data.forEach((field) => {
                if (field.name.startsWith('__')) {
                    let field_name = field.name.replace("__", "");
                    upload_data[field_name] = $(`#${field.name}`).val();
                }
            });

            if (document_uuids.length < 1) {
                notify('Please upload a document', 'error');
                return
            }

            new AjaxService().postRequest(
                url,
                upload_data,
                function (response) {
                    notify('Document uploaded successfully', 'success');
                    // documentUploadform.trigger("reset");
                    documentUploadform.parsley().reset();
                    // documentUploadform.find("#metadata-section").empty();
                    let dropzone = Dropzone.forElement(".dropzone");
                    // remove uuids from dropzone files
                    dropzone.files.forEach((file) => {
                        $(file.previewTemplate).find('.dz-remove').attr('data-uuid', '');
                    });
                    // remove all files
                    dropzone.removeAllFiles(true);
                },
                function (response) {
                    console.log('Error uploading document');
                    if (document_uuids.length < 1) {
                        notify('Please upload a document', 'error');
                    } else {
                        notify('Error uploading document', 'error');
                    }
                }
            );
            return false;
        });
    }

    main = () => {
        if (!hasPermission('document.add_document')) {
            $("#document-upload").hide();
        } else {
            this.generate();
            $("#document-upload").show();
            this.submitDocument();
        }
        if (hasPermission('category.view_category')) {
            this.getAvailableCategories();
        } else {
            $("#documentUploadMetadataForm").find("#category").hide();
        }
    }
}


new Upload().main();
