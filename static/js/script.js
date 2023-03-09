let birdForm = document.querySelectorAll(".form-product")
let container = document.querySelector("#form-create-receipt")
let addButton = document.querySelector("#add-form")
let totalForms = document.querySelector("#id_form-TOTAL_FORMS")

let formNum = birdForm.length-1
addButton.addEventListener('click', addForm)

function addForm(e){
    e.preventDefault()

    let newForm = birdForm[0].cloneNode(true)
    let formRegex = RegExp(`form-(\\d){1}-`,'g')

    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
    container.insertBefore(newForm, addButton)

    totalForms.setAttribute('value', `${formNum+1}`)
}

function toggleNewSellerField() {
    
    var existingSeller = document.getElementById('id_existing_seller');
    var newSeller = document.getElementById('form-create-receipt').getElementsByClassName('row')[1];
    
    if (existingSeller.value === 'other') {
        newSeller.style.display = 'block';
    } else {
        newSeller.style.display = 'none';
        newSeller.value = '';
    }
}
