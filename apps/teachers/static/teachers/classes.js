document.addEventListener('DOMContentLoaded', () => {

    // hides the forms
    document.querySelectorAll('.edit-class-name-div').forEach(content => {
        content.style.display = 'none';
    });

    // for edit button in the teacher my classes page
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            console.log(event.target.id);
            document.querySelector(`#div-for-edit-btn-${event.target.id}`).style.display = 'none';
            document.querySelector(`#div-for-delete-btn-${event.target.id}`).style.display = 'none';
            const class_name = document.querySelector(`#class-name-${event.target.id}`);
            const orig_name = class_name.innerHTML;
            document.querySelector(`#class-name-${event.target.id}`).style.display = 'none';
            edit_class_name(event.target, orig_name);
        });
    });
});

function edit_class_name(target, orig_name) {
    console.log('Edit button clicked');

    // show the form and set the value in text input to the original class name
    const edit_class_div = document.querySelector(`.edit-class-name-${target.id}`);
    edit_class_div.style.display = 'block';
    const classNameInput = document.querySelector(`#class-name-input-${target.id}`);
    classNameInput.value = orig_name.trim();

    const saveBtn = document.querySelector(`.save-btn-${target.id}`);
    saveBtn.addEventListener('click', (e) => {
        e.preventDefault()
        // get the csrftoken
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        console.log('Save button clicked');

        // make sure to include csrf token when fetching
        const request = new Request(
            `/teacher/classes/${target.id}/rename_class/`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        fetch(request, {
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify({
                new_name: classNameInput.value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        });

        edit_class_div.style.display = 'none';
        document.querySelector(`#div-for-edit-btn-${target.id}`).style.display = 'block';
        document.querySelector(`#div-for-delete-btn-${target.id}`).style.display = 'block';
        const class_name = document.querySelector(`#class-name-${target.id}`);
        class_name.style.display = 'block';
        class_name.innerHTML = classNameInput.value;
        return false;
    });
}