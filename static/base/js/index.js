class CustomDropzone{
    generate = () => {
        new AjaxService().getRequest(
    new Dropzone(".dropzone", { url: "/api/v1/documents/" });}
}