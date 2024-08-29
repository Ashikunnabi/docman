/*=============================================================================
                    LOCAL STORAGE DATA STORE
=============================================================================*/
// Function to set an item in LocalStorage with an expiration time
function setLocalWithExpiry(key, value, minutes = 60) {
    const now = new Date();
    const item = {
        value: value,
        expiry: now.getTime() + minutes * 60000, // Convert minutes to milliseconds
    };
    localStorage.setItem(key, JSON.stringify(item));
}

// Function to get an item from LocalStorage and check its expiration
function getLocalWithExpiry(key) {
    const itemStr = localStorage.getItem(key);
    if (!itemStr) {
        return null; // Item doesn't exist in LocalStorage
    }
    const item = JSON.parse(itemStr);
    const now = new Date();
    if (now.getTime() > item.expiry) {
        localStorage.removeItem(key); // Remove the item if it has expired
        return null;
    }
    return item.value;
}


// Function to remove an item from LocalStorage
function removeLocalWithExpiry(key) {
    const itemStr = localStorage.getItem(key);
    if (!itemStr) {
        return null; // Item doesn't exist in LocalStorage
    }
    localStorage.removeItem(key); // Remove the item if it has expired
}

function hasPermission(codename) {
    const permissions = getLocalWithExpiry('permissions');
    if (permissions) {
        return permissions.some(permission => permission.codename === codename);
    }
    return false;
}


/*=============================================================================
                        notify js customize
=============================================================================*/
notify = (message, message_type, duration, global_position = 'top right', element_position = 'bottom left') => {
    $.notify(
        message,
        {
            // whether to hide the notification on click
            clickToHide: true,
            // whether to auto-hide the notification
            autoHide: true,
            // if autoHide, hide after milliseconds
            autoHideDelay: duration,
            // show the arrow pointing at the element
            arrowShow: true,
            // arrow size in pixels
            arrowSize: 5,
            // position defines the notification position though uses the defaults below
            // position: '...',
            // default positions
            elementPosition: element_position,
            globalPosition: global_position,
            // default style
            style: 'bootstrap',
            // default class (string or [string])
            className: message_type,
            // show animation
            showAnimation: 'slideDown',
            // show animation duration
            showDuration: 400,
            // hide animation
            hideAnimation: 'slideUp',
            // hide animation duration
            hideDuration: 200,
            // padding between element and notification
            gap: 2
        }
    );
};


/*=============================================================================
                        Search product
=============================================================================*/

class Search {

    basic_search = () => {
        let self = this;
        let search_input = $('#searchbar-input-box');
        let searchbar_submit_button = $('#searchbar-submit-button');
        let search_result_div = $('#search_result');

        // hide search result if click outside of the div
        $(document).click(function (e) {
            if ($(e.target).parent().parent().attr('id') !== "search_result") {
                if ($(e.target).siblings("div").attr('id') !== "search_result") {
                    if ($(e.target).parent().siblings("div").attr('id') !== "search_result") {
                        search_result_div.fadeOut(300);
                    }
                }
            }
        });


        search_input.on('keyup', function (e) {
            if (search_input.val() !== '') {
                if (e.keyCode == 13) {
                    self.quick_search()
                } else {
                    self.do_search()
                }
            } else {
                search_result_div.fadeOut(1000);
            }
        });

        searchbar_submit_button.on('click', function (e) {
            if (search_input.val() !== '') {
                self.quick_search()
            } else {
                search_result_div.fadeOut(1000);
            }
        });
    };

    do_search = () => {
        let timeout = null;
        let search_input = $('#searchbar-input-box');
        let searchbar_submit_button = $('#searchbar-submit-button');
        let search_result_div = $('#search_result');

        if (search_result_div.css('display') === 'none') {
            search_result_div.children('ul').empty().append('<li>Searching...</li>');
            search_result_div.css('display', 'block');
        }

        // ajax search
        if (timeout) {
            clearTimeout(timeout);
        }
        timeout = setTimeout(function (e) {
            $.ajax({
                url: product_search_api_url + `?q=${search_input.val()}`,
                type: "GET",
                success: function (resp) {
                    search_result_div.children('ul').empty();
                    if (resp.data.length === 0) {
                        search_result_div.children('ul').append(`<li>No result found</li>`);
                    } else {
                        $.map(resp.data, function (value, index) {
                            let image_url = value.image_url ? value.image_url : '/static/base/img/no_image.png';
                            search_result_div.children('ul').append(
                                `<li>
                                    <a href="/product-details/${value.uuid}/" style="display: grid; grid-template-columns: 20% 70%; grid-column-gap: 20px;">
                                        <img width="100%" src="${image_url}">
                                        ${value.description}
                                    </a>
                                </li>`
                            );
                        });
                    }

                },
                error: function (response) {
                    console.log(response)
                }
            });
        }, 1000);
    };

    quick_search = () => {
        let self = this;
        let search_input = $('#searchbar-input-box');

        if (search_input.val() !== '') {
            window.location.href = `/product-list/?q=${search_input.val()}`
        }
    };

    advanced_search = () => {
        var container = $("#advanced_search");
        // show div if click
        $('#searchbar-advanced-search-button').on('click', function (e) {
            container.toggle()
        })
        // hide div if click outside
        $(document).mouseup(function (e) {
            // if the target of the click isn't the container nor a descendant of the container
            if (!container.is(e.target) && container.has(e.target).length === 0) {
                container.fadeOut(300);
            }
        });
        let self = this;
        let year = $('#adv_year');
        let brand = $('#adv_brand');
        let model = $('#adv_model');
        let search = $('#search');
        let reset = $('#reset');
        $.ajax({
            url: '/api/v1/get-advanced-search-data/',
            type: "GET",
            success: function (resp) {
                $.each(resp.data.years, function (i, v) {
                    $('#adv_year').append(`<option value="${v}">${v}</option>`);
                });
                $('#adv_year').selectpicker()

                $.each(resp.data.brands, function (i, v) {
                    $('#adv_brand').append(`<option value="${v.uuid}">${v.name}</option>`);
                });
                $('#adv_brand').selectpicker()

                $.each(resp.data.models, function (i, v) {
                    $('#adv_model').append(`<option value="${v}">${v}</option>`);
                });
                $('#adv_model').selectpicker()
            },
            error: function (response) {
                let response_json = response.responseJSON
                for (var field in response_json.error) {
                    if (response_json.error.hasOwnProperty(field)) {
                        var errorMessages = response_json.error[field];
                        for (var i = 0; i < errorMessages.length; i++) {
                            notify(`${field.toUpperCase()}: ${errorMessages[i]}`, 'error');
                        }
                    }
                }
                notify(response.responseJSON.detail, 'error');
            }
        });

        search.on('click', function (e) {
            window.location.href = `/product-list/?type=2&year=${year.val()}&adv_brand=${brand.val()}&model=${model.val()}`
        })
    };

    main = () => {
        this.basic_search();
        if (
            !window.location.pathname.startsWith("/admin/") &&
            !window.location.pathname.startsWith("/login/") &&
            !window.location.pathname.startsWith("/registration/")
        ) {
            this.advanced_search();
        }

    }
}

// new Search().main();


/*=============================================================================
                        AJAX SERVICE
=============================================================================*/
class AjaxService {
    constructor() {
        this.accessToken = this.getAccessToken();
    }

    // Utility function to get access token from local storage with expiry check
    getAccessToken() {
        return getLocalWithExpiry('access');
    }

    onLogoutAction() {
        // clear local storage except few keys
        let doNotRemoveKeys = ['rememberMe', 'username', 'password'];
        let allLoccalStorateKeys = Object.keys(localStorage);
        allLoccalStorateKeys.forEach(key => {
            if (!doNotRemoveKeys.includes(key)) {
                localStorage.removeItem(key);
            }
        });
    }

    // General method to perform AJAX requests
    ajaxRequest(method, url, data = null, isFileUpload = false) {
        const options = {
            url: url,
            type: method,
            headers: {
                'Authorization': `JWT ${this.accessToken}`
            },
            success: function (response) {
                if (typeof this.successCallback === 'function') {
                    this.successCallback(response);
                }
            }.bind(this),
            error: function (response) {
                if (response.status === 401) {
                    // Unauthorized error
                    this.onLogoutAction()
                    // notify user
                    notify('Session expired. Please login again.', 'error');
                    // Redirect to login page
                    setTimeout(() => {
                        window.location.href = '/logout/';
                    }, 2000);
                }
                if (typeof this.errorCallback === 'function') {
                    this.errorCallback(response);
                }
            }.bind(this)
        };

        if (['POST', 'PATCH'].includes(method) && isFileUpload) {
            options.data = data;
            options.processData = false;
            options.contentType = false;
        } else if (data) {
            options.data = JSON.stringify(data);
            options.headers['Content-Type'] = 'application/json';
        }

        return $.ajax(options);
    }

    getRequest(url, successCallback, errorCallback) {
        this.successCallback = successCallback;
        this.errorCallback = errorCallback;
        return this.ajaxRequest('GET', url);
    }

    postRequest(url, data, successCallback, errorCallback) {
        this.successCallback = successCallback;
        this.errorCallback = errorCallback;
        return this.ajaxRequest('POST', url, data);
    }

    patchRequest(url, data, successCallback, errorCallback) {
        this.successCallback = successCallback;
        this.errorCallback = errorCallback;
        return this.ajaxRequest('PATCH', url, data);
    }

    deleteRequest(url, successCallback, errorCallback) {
        this.successCallback = successCallback;
        this.errorCallback = errorCallback;
        return this.ajaxRequest('DELETE', url);
    }

    postRequestWithFile(url, data, successCallback, errorCallback) {
        this.successCallback = successCallback;
        this.errorCallback = errorCallback;
        return this.ajaxRequest('POST', url, data, true);
    }

    patchRequestWithFile(url, data, successCallback, errorCallback) {
        this.successCallback = successCallback;
        this.errorCallback = errorCallback;
        return this.ajaxRequest('PATCH', url, data, true);
    }
}


/*=============================================================================
                        SIDEBAR
=============================================================================*/
class Sidebar {
    constructor() {
        this.moduleWiseSidebarItems = [
            {
                code: 'user_management',
                name: 'Users',
                icon: 'fas fa-fw fa-user',
                submodules: [
                    {
                        name: 'User',
                        code: 'view_user',
                        requiredPermissions: ['rbac.view_user'],
                        url: '/rbac/user/'
                    },
                    {
                        name: 'Group',
                        code: 'view_group',
                        requiredPermissions: ['auth.view_group'],
                        url: '/rbac/group/'
                    },
                ]
            },
            {
                code: 'document_management',
                name: 'Documents',
                icon: 'fas fa-folder-open',
                submodules: [
                    {
                        name: 'Document',
                        code: 'view_document',
                        requiredPermissions: ['document.view_document'],
                        url: '/document/'
                    },
                ]
            }
        ];
    }

    getPermissions() {
        return getLocalWithExpiry('permissions');
    }

    readPermissionsAndSetSidebar() {
        const permissions = this.getPermissions();
        if (permissions) {
            this.setSidebar(permissions);
            this.highlightActiveSidebarItem();
        }
    }

    hasRequiredPermissions(submodule, permissions) {
        // Check if all required permissions are present
        return submodule.requiredPermissions.every(requiredPermission =>
            permissions.some(permission => permission.codename === requiredPermission)
        );
    }

    sidebarSubmodulesHtml(module, permissions) {
        return module.submodules
            .filter(submodule => this.hasRequiredPermissions(submodule, permissions))
            .map(submodule => `
                <a class="collapse-item" href="${submodule.url}" id="sidebar__${module.code}__${submodule.code}">
                    ${submodule.name}
                </a>
            `).join('');
    }

    sidebarModuleHtml(module, permissions) {
        return `
            <li class="nav-item">
                <a class="nav-link collapsed" href="#" data-toggle="collapse" 
                    id="sidebar__${module.code}"
                    data-target="#sidebar__${module.code}_options" 
                    aria-expanded="false" aria-controls="collapseTwo">
                    <i class="${module.icon}"></i>
                    <span>${module.name}</span>
                </a>
                <div id="sidebar__${module.code}_options" class="collapse" aria-labelledby="headingTwo"
                    data-parent="#accordionSidebar">
                    <div class="bg-white py-2 collapse-inner rounded">
                        <h6 class="collapse-header">SUB MODULE:</h6>
                        ${this.sidebarSubmodulesHtml(module, permissions)}
                    </div>
                </div>
            </li>`;
    }

    setSidebar(permissions) {
        const sidebar = $('#sidebar-modules');
        sidebar.empty();

        this.moduleWiseSidebarItems
            .filter(module =>
                module.submodules.some(submodule =>
                    this.hasRequiredPermissions(submodule, permissions))
            )
            .forEach(module => {
                sidebar.append(this.sidebarModuleHtml(module, permissions));
            });

        // Attach click event listeners
        $('.collapse-item').on('click', (event) => {
            event.preventDefault();
            const target = $(event.currentTarget);
            this.storeSelectedSidebarItem(target);
            // go to link
            window.location.href = target.attr('href');
        });
    }

    storeSelectedSidebarItem(item) {
        console.log(item);
        let id = item[0].id;
        if (id === '') {
            delete localStorage.selectedSidebarItem;
            return;
        }

        const sidebarItem = {
            module: id.split('__')[1],
            submodule: id.split('__')[2],
        };
        localStorage.setItem('selectedSidebarItem', JSON.stringify(sidebarItem));
    }

    highlightActiveSidebarItem() {
        const selectedItem = JSON.parse(localStorage.getItem('selectedSidebarItem'));
        if (selectedItem) {
            let module = $(`#sidebar__${selectedItem.module}`)
            let submodule = $(`#sidebar__${selectedItem.module}__${selectedItem.submodule}`)
            module.parent().addClass('active');
            submodule.parent().parent().addClass('show');
            submodule.addClass('active');
        }
    }
}

new Sidebar().readPermissionsAndSetSidebar();