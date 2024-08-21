class CategoryPermissionType:
    ADD = "add"
    VIEW = "view"
    CHANGE = "change"
    DELETE = "delete"
    DOWNLOAD = "download"

    CHOICES = (
        (ADD, "Add"),
        (VIEW, "View"),
        (CHANGE, "Change"),
        (DELETE, "Delete"),
        (DOWNLOAD, "Download"),
    )
