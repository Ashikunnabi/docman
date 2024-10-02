class Document {
    breadcrumbTrail = [{
        name: 'Home',
        uuid: "#"
    }];

    getIcon = (extension) => {
        switch (extension) {
            // add colors too
            case 'folder': return '<i class="far fa-folder" style="color:#0157b3"></i>';
            case 'jpg': return '<i class="far fa-image" style="color:#26b99a"></i>';
            case 'jpeg': return '<i class="fas fa-image" style="color:#26b99a"></i>';
            case 'png': return '<i class="far fa-image" style="color:#26b99a"></i>';
            case 'pdf': return '<i class="far fa-file-pdf" style="color:#09c55d"></i>';
            case 'doc': return '<i class="far fa-file-word" style="color:#222222"></i>';
            case 'docx': return '<i class="far fa-file-word" style="color:#222222"></i>';
            case 'xls': return '<i class="far fa-file-excel" style="color:#09c55d"></i>';
            case 'xlsx': return '<i class="far fa-file-excel" style="color:#09c55d"></i>';
            case 'ppt': return '<i class="far fa-file-powerpoint" style="color:#f6712e"></i>';
            case 'pptx': return '<i class="far fa-file-powerpoint" style="color:#f6712e"></i>';
            case 'txt': return '<i class="far fa-file-alt" style="color:#0096e6"></i>';
            default: return '<i class="far fa-question-circle" style="color:#c509bf"></i>';
        }
    }

    /*
    * =========================================================================
    *                       Document in Datatable
    * =========================================================================
    **/
    list = (category_uuid) => {
        let self = this;

        // Destroy the existing DataTable if it exists
        if ($.fn.DataTable.isDataTable('#documentDataTable')) {
            $('#documentDataTable').DataTable().clear().destroy();
        }

        let table = $('#documentDataTable').DataTable({
            "fixedHeader": {
                header: true,
                footer: true
            },
            scrollY: '55vh',
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": 'frtip',
            "ordering": false,
            "buttons": [
                {
                    text: 'Add',
                    attr: {
                        title: 'Add document',
                        id: 'addDocumentButton',
                        class: 'btn btn-success'
                    },
                    action: function (e, dt, node, config) {
                        window.location = document_add_url;
                    }
                },
                {
                    text: 'Delete',
                    attr: {
                        title: 'Delete document',
                        id: 'deleteDocumentButton',
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
                                    document_search_api_url + data[0].uuid + '/',
                                    function (resp) {
                                        Swal.fire(
                                            'Deleted!',
                                            'Document has been deleted.',
                                            'success'
                                        );
                                        dt.ajax.reload()
                                    },
                                    function (response) {
                                        let response_json = response.responseJSON
                                        if (response_json.code === "USER_DELETION_NOT_ALLOWED") {
                                            notify("You are not allowed to delete an document.", "error");
                                        }
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
            ],
            "lengthMenu": [50, 80, 100, 200],
            "ajax": function (data, callback, settings) {
                let urlParams = new URLSearchParams(window.location.search);
                let queryParamSearchKeyword = urlParams.get('search');
                data.search.value = data.search.value || queryParamSearchKeyword;
                $('#documentDataTable_filter input').val(data.search.value);
                // update browser url also
                let _url = new URL(window.location.href);
                _url.searchParams.set('search', data.search.value);
                window.history.replaceState({}, '', _url);

                let queryParams = $.param({
                    draw: data.draw,
                    start: data.start,
                    length: data.length,
                    search: data.search.value,
                    order: JSON.stringify(data.order),
                    category_uuid: category_uuid,
                });
                if (data.search.value) {
                    queryParams += '&file_only=true';
                }
                let url = `${document_search_api_url}?${queryParams}`;
                new AjaxService().getRequest(url, function (response) {
                    callback(response);
                }, function (response) {
                    notify(response.responseJSON.detail, 'error');
                })
            },
            // "rowCallback": function (row, data, displayNum, displayIndex, dataIndex) {
            //     $(row).attr('title', 'Double click to edit')
            // },
            "columns": [
                { "title": "Name", "data": "" },
                { "title": "Size", "data": "" },
                { "title": "Modified", "data": "" },
                // { "title": "Path", "data": "category_wise_file_path" },
                { "title": "Action", "data": "" },
            ],
            "columnDefs": [
                {
                    "targets": 0,
                    "data": "name",
                    "width": "50%",
                    "render": function (data, type, row, meta) {
                        let html = `<div class="file-icon">${self.getIcon(row.extension)} &nbsp;${row.name}`;
                        if (hasPermission('category.add_category') && row.extension === 'folder') {
                            if (row.is_active) {
                                html += ` &nbsp;<span class="badge badge-success">Active</span>`;
                            } else {
                                html += ` &nbsp;<span class="badge badge-danger">Inactive</span>`;
                            }
                        }
                        html += `</div>`;

                        return html;
                    }

                },
                {
                    "targets": 1,
                    "data": "size",
                    "render": function (data, type, row, meta) {
                        // row.size is in byte
                        let size = row.size + ' Byte';
                        // if more than 1 TB then convert to TB
                        if (row.size >= 1024 * 1024 * 1024 * 1024) {
                            size = (row.size / (1024 * 1024 * 1024 * 1024)).toFixed(2) + ' TB';
                        }
                        // if more than 1 GB then convert to GB
                        else if (row.size >= 1024 * 1024 * 1024) {
                            size = (row.size / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
                        }
                        // if more than 1 MB then convert to MB
                        else if (row.size >= 1024 * 1024) {
                            size = (row.size / (1024 * 1024)).toFixed(2) + ' MB';
                        }
                        // if more than 1 KB then convert to KB
                        else if (row.size >= 1024) {
                            size = (row.size / 1024).toFixed(2) + ' KB';
                        }

                        if (row.extension === 'folder') {
                            size = 'Folder';
                        }
                        return size;
                    }

                },
                {
                    "targets": 2,
                    "data": "modified",
                    "render": function (data, type, row, meta) {
                        return moment(row.updated_at).format('YYYY-MM-DD hh:mm A');
                    }

                },
                {
                    "targets": -1,
                    "data": null,
                    "render": function (data, type, row, meta) {
                        let html = '';
                        // if (row.extension !== 'folder') {
                        //     html = `<a href="edit/${row.uuid}">
                        //     <button class="btn btn-outline-primary btn-sm actionButtonEdit" title="Edit">
                        //     >
                        //     </button>
                        // </a>`;
                        // }
                        if (row.extension === 'folder') {
                            if (hasPermission('category.delete_category')) {
                                html += `<i class="far fa-trash-alt btn btn-outline-primary btn-sm actionButton actionButtonDeleteFolder" title="View Folder"></i>`;
                            }
                            if (hasPermission('category.view_category')) {
                                html += `<button class="btn btn-outline-primary btn-sm actionButton actionButtonViewFolder" title="View Folder">></button>`;
                            }
                        } else {
                            let hasDeletePermission = hasPermission('document.delete_document') && hasCategoryPermission(row.category, 'delete_document');
                            if (hasDeletePermission) {
                                html += `<i class="far fa-trash-alt btn btn-outline-primary btn-sm actionButton actionButton actionButtonDeleteFile" title="Delete File"></i>`;
                            }
                            if (hasPermission('document.view_document')) {
                                html += `<button class="btn btn-outline-primary btn-sm actionButton actionButtonViewFile" title="View File">></button>`;
                            }
                        }
                        return html;
                    }
                }
            ],
        });

        // double click row will redirect to edit selected row
        $('#documentDataTable tbody').off('dblclick').on('dblclick', 'tr', function () {
            let data = $('#documentDataTable').DataTable().row(this).data();
            if (data.extension === 'folder') {
                self.handleRowDoubleClick(data);
            } else {
                window.open(`${document_view_url}${data.uuid}/`, '_blank');
            }
        });
        self.renderBreadcrumb();
        self.breadcrumbClick();
    };

    // Function to handle row double-click and reinitialize DataTable with new data
    handleRowDoubleClick = (rowData) => {
        let self = this;
        self.updateBreadcrumb(rowData);
        self.list(rowData.uuid);
    }

    updateBreadcrumb = (rowData) => {
        let self = this;
        self.breadcrumbTrail.push({
            name: rowData.name,
            uuid: rowData.uuid
        });
        self.renderBreadcrumb();
    }

    renderBreadcrumb = () => {
        let self = this;
        let breadcrumbHtml = ``;

        self.breadcrumbTrail.forEach((item, index) => {
            if (index === 0) {
                breadcrumbHtml += `<a href="#" class="breadcrumbItem" title="Go to home"><i class="fas fa-home"></i></a>`;
                return;
            }
            if (index === self.breadcrumbTrail.length - 1) {
                breadcrumbHtml += ` <span class="separator">/</span> ${item.name}`;
                return;
            }
            breadcrumbHtml += ` <span class="separator">/</span> <a href="${item.uuid}" class="breadcrumbItem">${item.name}</a>`;
        });

        $('#breadcrumb').html(breadcrumbHtml);
    }

    breadcrumbClick = () => {
        let self = this;
        $('#breadcrumb').off('click').on('click', '.breadcrumbItem', function (e) {
            e.preventDefault();
            let uuid = $(this).attr('href');
            let index = self.breadcrumbTrail.findIndex((item) => item.uuid === uuid);
            self.breadcrumbTrail = self.breadcrumbTrail.slice(0, index + 1);
            self.renderBreadcrumb();
            if (uuid === "#") {
                self.list();
            } else {
                self.list(uuid);
            }
        });
    }

    addFolder = () => {
        let self = this;
        let modal = $('#addFolderModal');
        $('#actionButtonAddFolder').off('click').on('click', function () {
            $('#addFolderModalForm')[0].reset();
            modal.find('#addFolderModalFormError').html("");
            modal.modal('show');
        });
        $(document).on('submit', '#addFolderModalForm', function (e) {
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
                        $('#addFolderModalFormError').html(errorHtml);
                    }
                }
            );
        });
    }

    deleteFolder = () => {
        let self = this;
        let datatable_row = null;
        let modal = $('#deleteFolderModal');

        $(document).on('click', '.actionButtonDeleteFolder', function () {
            let row = $(this).parent().parent()
            datatable_row = $('#documentDataTable').DataTable().row(row).data();
            modal.find('#deleteFolderModalFolderName').text(datatable_row.name);
            modal.find('#deleteFolderModalFormError').html("");
            modal.modal('show');
        });

        $(document).on('submit', '#deleteFolderModalForm', function (e) {
            e.preventDefault();
            let parent_uuid = self.breadcrumbTrail[self.breadcrumbTrail.length - 1].uuid;
            new AjaxService().deleteRequest(
                category_api_url + datatable_row.uuid + '/',
                function (response) {
                    if (parent_uuid === "#") {
                        self.list();
                    } else {
                        self.list(self.breadcrumbTrail[self.breadcrumbTrail.length - 1].uuid);
                    }
                    modal.modal('hide');
                    notify('Success', 'success');
                },
                function (response) {
                    let response_json = response.responseJSON
                    if (response_json.code === "CATEGORY_DELETE_EXCEPTION") {
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
                        $('#deleteFolderModalFormError').html(errorHtml);
                    }
                }
            );
        });
    }

    deleteFile = () => {
        let self = this;
        let datatable_row = null;
        let modal = $('#deleteFileModal');

        $(document).on('click', '.actionButtonDeleteFile', function () {
            let row = $(this).parent().parent()
            datatable_row = $('#documentDataTable').DataTable().row(row).data();
            modal.find('#deleteFileModalFolderName').text(datatable_row.name);
            modal.find('#deleteFileModalFormError').html("");
            modal.modal('show');
        });

        $(document).on('submit', '#deleteFileModalForm', function (e) {
            e.preventDefault();
            let parent_uuid = self.breadcrumbTrail[self.breadcrumbTrail.length - 1].uuid;
            new AjaxService().deleteRequest(
                document_api_url + datatable_row.uuid + '/',
                function (response) {
                    if (parent_uuid === "#") {
                        self.list();
                    } else {
                        self.list(self.breadcrumbTrail[self.breadcrumbTrail.length - 1].uuid);
                    }
                    modal.modal('hide');
                    notify("Success", "success");
                },
                function (response) {
                    let response_json = response.responseJSON
                    if (response_json.code === "DOCUMENT_DELETE_EXCEPTION") {
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
                        $('#deleteFileModalFormError').html(errorHtml);
                    }
                }
            );
        });
    }


    viewFolder = () => {
        let self = this;
        let datatable_row = null;

        $(document).on('click', '.actionButtonViewFolder', function () {
            let row = $(this).parent().parent()
            datatable_row = $('#documentDataTable').DataTable().row(row).data();
            let url = `/category/edit/${datatable_row.uuid}/`;
            window.location.href = url;
        });
    }

    viewFile = () => {
        let self = this;
        let datatable_row = null;

        $(document).on('click', '.actionButtonViewFile', function () {
            let row = $(this).parent().parent()
            datatable_row = $('#documentDataTable').DataTable().row(row).data();
            let url = `${document_view_url}${datatable_row.uuid}/`;
            window.open(url, '_blank');
        });
    }

    main = () => {
        if (page === 'list') {
            // get category_uuid from url
            let url = new URL(window.location.href);
            let category_uuid = url.searchParams.get("category_uuid");
            if (category_uuid) {
                this.list(category_uuid);
            } else {
                this.list();
            }
            if (!hasPermission('category.add_category')) {
                $('#actionButtonAddFolder').hide();
            } else {
                this.addFolder();
            }
            if (!hasPermission('category.view_category')) {
                $('.actionButtonViewFolder').hide();
            } else {
                this.viewFolder();
            }
            if (!hasPermission('document.view_document')) {
                $('.actionButtonViewFile').hide();
            } else {
                this.viewFile();
            }
            if (!hasPermission('document.delete_document')) {
                $('.actionButtonDeleteFolder').hide();
            } else {
                this.deleteFolder();
            }
            if (!hasPermission('document.delete_document')) {
                $('.actionButtonDeleteFile').hide();
            } else {
                this.deleteFile();
            }
        }
    }
}


new Document().main();
