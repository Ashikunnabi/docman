class Edit {
    document_view_card = $("#document-view-card");
    document_viewer = $("#document-viewer");
    pdfDocumentViewer = $(this.document_viewer).find("#pdfDocumentViewer");
    imageDocumentViewer = $(this.document_viewer).find("#imageDocumentViewer");
    otherDocumentViewer = $(this.document_viewer).find("#otherDocumentViewer");
    metadataForm = $("#documentEditMetadataForm");
    document = null;

    textField = (field) => {
        return `<div class="form-group">
            <label for="${field.uuid}">${field.name}${field.is_required ? '<span class="text-danger">*</span>' : ''}</label>
            <input type="text" class="form-control" id="${field.uuid}" name="${field.uuid}" data-field-type=${field.field_type} placeholder="${field.placeholder}" ${field.is_required ? 'required' : ''}>
        </div>`;
    }

    integerField = (field) => {
        return `<div class="form-group">
            <label for="${field.uuid}">${field.name}${field.is_required ? '<span class="text-danger">*</span>' : ''}</label>
            <input type="number" class="form-control" id="${field.uuid}" name="${field.uuid}" data-field-type=${field.field_type} placeholder="${field.placeholder}" ${field.is_required ? 'required' : ''}>
        </div>`;
    }

    emailField = (field) => {
        return `<div class="form-group">
            <label for="${field.uuid}">${field.name}${field.is_required ? '<span class="text-danger">*</span>' : ''}</label>
            <input type="email" class="form-control" id="${field.uuid}" name="${field.uuid}" data-field-type=${field.field_type} placeholder="${field.placeholder}" ${field.is_required ? 'required' : ''}>
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

    setFormFieldValues = (document) => {
        let documentEditform = $("#documentEditMetadataForm");
        let category_dropdown = documentEditform.find("#__category_uuid");
        let options = new Option(document.category.path, document.category.uuid, true, true);
        category_dropdown.append(options).trigger('change');
        category_dropdown.attr('disabled', 'disabled');

        let metadata = document.metadata_values;
        metadata.forEach((value) => {
            let fieldElement = documentEditform.find(`#${value.field.uuid}`);
            if (fieldElement.length) {
                let value_type = `value_${value.field.field_type}`;
                fieldElement.val(value[value_type]);
            }
        });
    }

    fetchAndRenderMetadata = (category_uuid) => {
        let self = this;
        let documentEditform = $("#documentEditMetadataForm")
        let metadata_section = documentEditform.find("#metadata-section");
        metadata_section.empty();
        let metadata_html = '';
        if (!category_uuid) {
            return;
        }
        let url = `${category_api_url}${category_uuid}/`;
        new AjaxService().getRequest(
            url,
            function (response) {
                let metadata = response.data.metadata;
                $.each(metadata, function (index, fields) {
                    metadata_html += self.dynamicFormFields(fields);
                });
                metadata_section.html(metadata_html);

                // restart parsley validation
                documentEditform.parsley().reset();

            },
            function (response) {
                console.log('Error fetching metadata');
            }
        );
    }

    getAvailableCategories = () => {
        let self = this;
        let documentEditform = $("#documentEditMetadataForm")
        let category_dropdown = documentEditform.find("#__category_uuid");

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

    renderPDF = (_document) => {
        let pdf_url = _document.file;
        PDFViewerApplication.open({ url: pdf_url });
        PDFViewerApplication.eventBus.on('documentloaded', () => {
            PDFViewerApplication.setTitle(_document.name);
        })
    }

    renderImage = (_document) => {
        let self = this;
        let image_url = _document.file;
        let image = new Image();
        image.src = image_url;
        image.style.width = '100%';
        image.style.height = 'auto';
        image.onload = function () {
            self.imageDocumentViewer.append(image);
        }
    }

    renderOtherDocument = (_document) => {
        // gdrive iframe
        let iframe = document.createElement('iframe');
        // iframe.src = `https://docs.google.com/gview?url=https://www.cmu.edu/blackboard/files/evaluate/tests-example.xls&embedded=true`;
        iframe.src = `https://docs.google.com/gview?url=${window.location.origin}${_document.file}&embedded=true`;
        iframe.style.width = '100%';
        iframe.style.height = '100%';
        iframe.style.border = 'none';
        this.otherDocumentViewer.append(iframe);
    }

    viewDocument = () => {
        let self = this;
        let url = `${document_api_url}${uuid}/`;
        new AjaxService().getRequest(
            url,
            function (response) {
                self.document = response.data;
                self.document_view_card.find("#document-name").text(self.document.name);
                self.fetchAndRenderMetadata(self.document.category.uuid);
                setTimeout(function () {
                    self.setFormFieldValues(response.data);
                }, 2000);

                if (self.document.extension !== 'pdf') {
                    PDFViewerApplication.close();
                }
                if (self.document.extension === 'pdf') {
                    self.pdfDocumentViewer.show();
                    self.renderPDF(self.document);
                } else if (self.document.extension === 'png') {
                    self.imageDocumentViewer.show();
                    self.renderImage(self.document);
                } else {
                    self.otherDocumentViewer.show();
                    self.renderOtherDocument(self.document);
                }

                // set title of the page
                document.title = "Docman | " + self.document.name;
                if (hasCategroryPermission(self.document.category.code, 'download_document')) {
                    $("#download-document").show();
                    self.downloadDocument();
                }

            },
            function (response) {
                console.log('Error fetching document');
            }
        );
    }

    downloadDocument = () => {
        let self = this;
        $("#download-document").on('click', function () {
            let url = `${self.document.file}`;
            window.open(url, 'download');
        })
    }

    metadataValueUpdate = () => {
        let self = this;
        self.metadataForm.on('submit', function (e) {
            e.preventDefault();
            self.metadataForm.parsley().validate();
            if (!self.metadataForm.parsley().isValid()) {
                return;
            }
            let url = `${document_api_url}${uuid}/metadata/`;
            let data = $(this).serializeArray();
            let metadata = [];
            data.forEach((item) => {
                if (item.name === '__category_uuid') {
                    return;
                }
                let field_type = "value_" + $(`#${item.name}`).data('field-type');
                metadata.push({
                    field_uuid: item.name,
                    [field_type]: item.value
                });
            });
            new AjaxService().patchRequest(
                url,
                metadata,
                function (response) {
                    notify('success', 'success');
                },
                function (response) {
                    notify(response.responseJSON.message, 'error');
                    console.log(response);
                }
            );

        })
    }

    main = () => {
        if (!hasPermission('document.view_document')) {
            $("#document-view").hide();
        } else {
            $("#document-view").show();
            this.viewDocument();
        }
        if (hasPermission('category.view_category')) {
            this.getAvailableCategories();
        } else {
            $("#documentEditMetadataForm").find("#category").hide();
        }
        this.metadataValueUpdate();
    }
}


new Edit().main();
