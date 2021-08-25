const form = document.getElementById('addIncomeForm')
const name = document.getElementById('input-category')

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
            console.log(response)
        },
        error: function(error){
            console.log(error)
        },
        caches: false,
        contentType: false,
        processData: false
    })

})