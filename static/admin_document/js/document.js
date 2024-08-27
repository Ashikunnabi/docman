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
            "processing": true,
            "serverSide": true,
            "bDestroy": true,
            "bJQueryUI": true,
            "dom": 'rtp',
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
                                    document_api_url + data[0].uuid + '/',
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
                let queryParams = $.param({
                    draw: data.draw,
                    start: data.start,
                    length: data.length,
                    search: data.search.value,
                    order: JSON.stringify(data.order),
                    category_uuid: category_uuid
                });
                let url = `${document_api_url}?${queryParams}`;
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
                        return `<div class="file-icon">${self.getIcon(row.extension)} &nbsp;${row.name}</div>`;
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
                        return moment(row.modified).format('YYYY-MM-DD hh:mm A');
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
                        const has_delete_permission = hasPermission('document.delete_document');
                        if (has_delete_permission) {
                            html += `<i class="far fa-trash-alt actionButton actionButtonDelete"></i>`;
                        }
                        if (row.extension === 'folder') {
                            html += `<i class="far fa-sun actionButton actionButtonManage"></i>`;
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
                window.location.href = "edit/" + data.uuid;
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
                breadcrumbHtml += `<a href="#" class="breadcrumbItem">${item.name}</a>`;
            } else {
                breadcrumbHtml += ` <span class="separator">/</span> <a href="${item.uuid}" class="breadcrumbItem">${item.name}</a>`;
            }
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
        }
    }
}


new Document().main();
