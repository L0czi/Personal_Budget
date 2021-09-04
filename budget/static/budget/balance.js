$(document).ready( ()=>{

    const csrf = document.getElementsByName('csrfmiddlewaretoken');
    const $deleteButton = $('button')

    const clearUl = (id, category_id,type)=> {
        var $elementUl = $(`#list-${type}${category_id}`);
        element = $elementUl.find(`#line${id}`)
        element.remove()
    }

    const udateNumbers = (category_id,type) => {
        var url_balance = '/budget/balance';

        $.get(url_balance,{AJAX: 'True', category: category_id, type:type}, function(response){
            console.log(response)
            $('#balanceHeader').text(`Bilans: ${response.balance}`)
            $('#expenceHeader').text(`Wydatki Łącznie: ${response.aggr_all_expences}`)
            $('#incomeHeader').text(`Przychody Łącznie: ${response.aggr_all_incomes}`)
            
            
        
            if (response.updated_category_value === null){
                $(`#${type}Banner${category_id}`).remove()
                $(`#${type}Modal${category_id}`).modal('hide')
            }else{
                $(`#${type}Ammount${category_id}`).text(`${response.updated_category_value}`);
            }


            if (type === 'expence' && response.aggr_all_expences === 0){
                $('#expenceHeader').after('<span>Nie dodano wydatku! Dodaj swój pierwszy wydatek w zakładce "WYDATEK"</span>')
            }else if (type === 'income' && response.aggr_all_incomes === 0){
                $('#incomeHeader').after('<span>Nie dodano przychodu! Dodaj swój pierwszy przychód w zakładce "PRZYCHÓD"</span>')
            }
        })
        
    }

    $deleteButton.on('click', e=>{
        e.preventDefault()
        var $button = $(e.target)  

        if ($button.attr('id') === 'deleteButton'){
            var url = $button.attr('data-url');
            var id = $button.attr('name');
            var type = $button.attr('data-type');
            var category_id = $button.attr('date-name');
            const fd = new FormData ()
            fd.append('csrfmiddlewaretoken', csrf[0].value);

            $.ajax({
                type: 'POST',
                url: url,
                data: fd,
                success: function(){
                    clearUl(id,category_id,type);
                    udateNumbers(category_id, type);
                },
                error: function(){
                    alert('error')
                },
                cache : false,
                contentType: false,
                processData: false,
            })
        }
    })


    $(function () {
        $('[data-toggle="popover"]').popover()
    })


})