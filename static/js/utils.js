function setFormErrors(form, errors) {
    for (let key in errors) {
        let input = form.querySelector('*[name=' + key + ']');
        input.errorMessage = errors[key];
        input.invalid = true;
    }
}

// Original JavaScript code by Chirp Internet: www.chirp.com.au
// Please acknowledge use of this code by including this header.

function getCookie(name)
{
    let re = new RegExp(name + "=([^;]+)");
    let value = re.exec(document.cookie);
    return (value != null) ? unescape(value[1]) : null;
}

function getCsrfToken() {
    return getCookie('csrftoken');
}