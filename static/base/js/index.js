class CustomDropzone {
    generate = () => {
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
                    $(mockFile.previewTemplate).find('.dz-remove').attr('data-uuid', document.uuid);
                });
            },
            function (response) {
                console.log('Error fetching documents');
            }
        );
    }

    main = () => {
        if (!hasPermission('document.add_document')) {
            $("#document-upload").hide();
        } else {
            this.generate();
            $("#document-upload").show();
        }
        if (!hasPermission('document.view_document')) {
            $("#recent-uploaded-document").hide();
        } else {
            $("#recent-uploaded-document").show();
        }

    }
}

const customDropzone = new CustomDropzone();
customDropzone.main();