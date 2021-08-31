$(document).ready( () =>{

    const $deleteCategoryForm = $('#deleteCategoryForm')
    const $editCategoryForm = $('#editCategoryForm')
    const $alert = $('#alert-ribbon');
    const csrf = document.getElementsByName('csrfmiddlewaretoken');
    const $deleteModal = $('#deleteConfModal')
    const $editModal = $('#editModal');

    //animation for buttons
    $('button.js_button').click(function(){
        $(this).parent().next('div.js_toggle_group').slideToggle(150);
      })

    $editModal.on('show.bs.modal', function (e) {
        var button = $(e.relatedTarget); // Button that triggered the modal
        var url = button.data('url'); // Extract info from data-* attributes
        var id = button.data('id');
        var type = button.data('type');
        
        var modal = $(this);
        modal.find('#editCategoryForm').attr('action',url);
        modal.find('#editCategoryForm').attr('name',type); 
        modal.find('#editCategoryButton').attr('name',id);
        
        $.get(url, function(response){
            modal.find('#editCategoryFormInput').attr('placeholder',response.name)
        })
    })


    $deleteModal.on('show.bs.modal', function (e) {
        var button = $(e.relatedTarget) // Button that triggered the modal
        var urlDelete = button.data('urldelete') // Extract info from data-* attributes
        var urlEdit = button.data('urledit')
        var id = button.data('id')
        var type = button.data('type')
        
        var modal = $(this)
        modal.find('#deleteCategoryForm').attr('action',urlDelete)
        modal.find('#deleteCategoryForm').attr('name',type)
        modal.find("#deleteCategoryButton").attr('name',id)
        
        $.get(urlEdit, function(response){
            modal.find('p').text(`Czy jesteś pewien że chcesz usunąć ${response.name}? Spowoduje to usunięcie wszystkich wpisów związanych z tą kategorią`)
        })
    })


    const clearUl = (id, type)=> {
        var $elementUl = $(`#${type}-categories-list`);
        element = $elementUl.find(`#line${id}`)
        element.remove()
    }

    const updateUl = (id, type, response) =>{
        var $elementUl = $(`#${type}-categories-list`);
        element = $elementUl.find(`#line${id} span:first-child`);
        element.text(response.name);
    }


    const messageHandler = (message, type)=> {
        $alert.append(`<div class="alert alert-${type} text-center" role="alert">${message}</div>`)

    }

    //EDIT CATEGORY
    $editCategoryForm.on('submit', e=>{
        e.preventDefault();
        var url = $editCategoryForm.attr('action');
        var type = $editCategoryForm.attr('name');
        var name = $('#editCategoryFormInput').val();
        var id = $('#editCategoryButton').attr('name')

        const fd = new FormData ()
        fd.append('csrfmiddlewaretoken', csrf[0].value);
        fd.append('name',name);

        $.ajax({
            type: 'POST',
            url: url,
            data: fd,
            success: function(response){
                $editModal.modal('hide');
                $editCategoryForm.trigger('reset');
                updateUl(id, type, response);
            },

            error: function(error){
                messageHandler(error.responseJSON.errorText, 'danger');
                (error.responseJSON.errorText, 'danger');
                $editCategoryForm.trigger('reset');
                $editModal.modal('hide');
                setTimeout(()=>{
                    $alert.empty();
                },3000);
            },
            cache : false,
            contentType: false,
            processData: false,
        })
    })

    //DELETE CATEGORY
    $deleteCategoryForm.on('submit', e=>{
        e.preventDefault();
        
        var url = $('#deleteCategoryForm').attr('action')
        var type = $('#deleteCategoryForm').attr('name')
        var id = $('#deleteCategoryButton').attr('name')
        
        const fd = new FormData()
        fd.append('csrfmiddlewaretoken', csrf[0].value)

        $.ajax({
            type: 'POST',
            url: url,
            data: fd,
            success: function(){
                clearUl(id, type);
                $deleteModal.modal('hide')
            },

            error: function(){
                alert('error')
            },
            cache : false,
            contentType: false,
            processData: false,
        })

    })
})