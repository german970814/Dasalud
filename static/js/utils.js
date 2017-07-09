function setFormErrors(form, errors) {
    for (let key in errors) {
        let input = form.querySelector('*[name=' + key + ']');
        input.errorMessage = errors[key];
        input.invalid = true;
    }
}