$(document).ready( () =>{

    const addIncomeCategoryForm = document.getElementById('addIncomeCategoryForm'); //
    const name = document.getElementById('addIncomeCategoryInput'); //new input category pass by user in <input> field
    const csrf = document.getElementsByName('csrfmiddlewaretoken');
    const $alert = $('#alert-ribbon');

    const appendUl = (response) => {
        var $incomesUl = $("#incomes-categorys-list li:nth-last-child(2)"); //pic last income category before form
        $incomesUl.after(`<li id=line${response.id} class="list-group-item d-flex">
                        <span class="mr-auto">${response.name}</span>
                        <button id="deleteCategoryButton${response.id}" type="button" class="mr-2 btn btn-danger btn-sm fas fa-trash" data-toggle="modal" data-target=".bd-delete-modal-sm" data-id=${response.id} data-type='incomes' data-urledit=/budget/income_category/${response.id}/update data-urldelete=/budget/income_category/${response.id}/delete></button>
                        <button id="editCategoryButton${response.id}" type="button" class="btn btn-secondary btn-sm far fa-edit" data-toggle="modal" data-target=".bd-edit-modal-sm" data-id=${response.id} data-type='incomes' data-url=/budget/income_category/${response.id}/update></button>
                    </li>`);
    }
    const messageHandler = (message, type)=> {
        $alert.append(`<div class="alert alert-${type} text-center" role="alert">${message}</div>`)

    }

    //ADD NEW CATEGORY
    addIncomeCategoryForm.addEventListener('submit', e=>{
        e.preventDefault()

        const fd = new FormData()

        fd.append('csrfmiddlewaretoken', csrf[0].value)
        fd.append('name', name.value)

        $.ajax({
            type : 'POST',
            url : '/budget/settings/',
            data: fd,
            success: function(response){
                messageHandler(response.succesText,'success');
                setTimeout(()=>{
                    $alert.empty();
                },3000);
                appendUl(response); //append new line to unordered list
                addIncomeCategoryForm.reset();
                
            },
            error: function(error){
                messageHandler(error.responseJSON.errorText, 'danger');
                setTimeout(()=>{
                    $alert.empty();
                },3000);
                addIncomeCategoryForm.reset();
            },
            caches: false,
            contentType: false,
            processData: false
        })

    })
})