const form = document.getElementById('addIncomeForm')
const name = document.getElementById('input-category')
const $incomesUl =  $("#incomes-categorys-list li:nth-last-child(2)") //pic last income category before form


const updateUl = (category) => {
    $incomesUl.after(`<li class="list-group-item d-flex">
                 <span class="mr-auto">${category}</span>
                 <div><a class='btn btn-secondary btn-sm' href="/budget/e_inc_category/${category}">Edytuj</a></div>
            </li>`);
}

const csrf = document.getElementsByName('csrfmiddlewaretoken')
form.addEventListener('submit', e=>{
    e.preventDefault()

    const fd = new FormData()

    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('name', name.value)

    $.ajax({
        type : 'POST',
        url : '/budget/settings/',
        data: fd,
        success: function(response){
            updateUl(response.name) //update unordered list
        },
        error: function(error){
            console.log(error)
        },
        caches: false,
        contentType: false,
        processData: false
    })

})