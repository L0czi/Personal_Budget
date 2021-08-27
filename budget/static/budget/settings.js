const addIncomeForm = document.getElementById('addIncomeForm');
const deleteCategoryForm = document.getElementById('deleteCategoryForm')
const name = document.getElementById('input-category');
const $alert = $('#alert-ribbon');
const csrf = document.getElementsByName('csrfmiddlewaretoken');
const $deleteModal = $('#deleteConfModal')


$deleteModal.on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var url = button.data('url') // Extract info from data-* attributes
    var name = button.data('name')
    var id = button.data('id')
    var type = button.data('type')
    
    var modal = $(this)
    modal.find('.modaltitle')
    modal.find('p').text(`Czy jesteś pewien że chcesz usunąć ${name}? Spowoduje to usunięcie wszystkich wpisów związanych z tą kategorią`)
    modal.find('#deleteCategoryForm').attr('action',url)
    modal.find('#deleteCategoryForm').attr('name',type)
    modal.find("#deleteCategoryButton").attr('name',id)
    
  })


const updateUl = (response) => {
    var $incomesUl = $("#incomes-categorys-list li:nth-last-child(2)"); //pic last income category before form
    $incomesUl.after(`<li id=line${response.id} class="list-group-item d-flex">
                    <span class="mr-auto">${response.name}</span>
                    <button type="button" class="mr-2 btn btn-danger btn-sm fas fa-trash" data-toggle="modal" data-target=".bd-delete-modal-sm" data-id=${response.id} data-name=${response.name} data-url=/budget/budget/${response.id}/delete></button>
                    <div><a class='btn btn-secondary btn-sm far fa-edit' href="/budget/e_inc_category/${response.name}"></a></div>
                </li>`);
}

const clearUl = (buttonId, type)=> {
    var $incomesUl = $(`#${type}-categorys-list`);
    element = $incomesUl.find(`#line${buttonId}`)
    element.remove()
}

const errorHandler = (errorText)=> {
    $alert.append(`<div class="alert alert-danger text-center" role="alert">${errorText}</div>`)

}


//DELETE CATEGORY
deleteCategoryForm.addEventListener('submit', e=>{
    e.preventDefault();
    
    var url = $('#deleteCategoryForm').attr('action')
    var type = $('#deleteCategoryForm').attr('name')

    var buttonId = $('#deleteCategoryButton').attr('name')
    
    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)

    $.ajax({
        type: 'POST',
        url: url,
        data: fd,
        success: function(){
            clearUl(buttonId, type);
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


//ADD NEW CATEGORY
addIncomeForm.addEventListener('submit', e=>{
    e.preventDefault()

    const fd = new FormData()

    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('name', name.value)

    $.ajax({
        type : 'POST',
        url : '/budget/settings/',
        data: fd,
        success: function(response){
            updateUl(response); //update unordered list
            addIncomeForm.reset();
            
        },
        error: function(error){
            errorHandler(error.responseJSON.errorText);
            setTimeout(()=>{
                $alert.empty();
            },3000);
            addIncomeForm.reset();
        },
        caches: false,
        contentType: false,
        processData: false
    })

})