const addIncomeForm = document.getElementById('addIncomeForm');
const name = document.getElementById('input-category');
const $alert = $('#alert-ribbon');

const csrf = document.getElementsByName('csrfmiddlewaretoken');



const updateUl = (response) => {
    var $incomesUl = $("#incomes-categorys-list li:nth-last-child(2)"); //pic last income category before form
    $incomesUl.after(`<li class="list-group-item d-flex">
                 <span class="mr-auto">${response.name}</span>
                 <form class="mr-2" method="POST" action="/budget/budget/${response.id}/delete">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrf[0].value}">
                    <button id="incomeCategoryDeletebutton${response.id}" name="delete_income_category" type="submit" class="btn btn-danger btn-sm fas fa-trash"></button>
                </form>
                    <div><a class='btn btn-secondary btn-sm far fa-edit' href="/budget/e_inc_category/${response.name}"></a></div>
                </li>`);
}

const errorHandler = (errorText)=> {
    $alert.append(`<div class="alert alert-danger text-center" role="alert">${errorText}</div>`)

}

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