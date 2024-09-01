class CustomDropzone {
    generate = () => {
        const dropzone = new Dropzone(".dropzone", {
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