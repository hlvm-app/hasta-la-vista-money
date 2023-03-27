let productForm = document.querySelectorAll(".form-product")
let container = document.querySelector("#form-create-receipt")
let addButton = document.querySelector("#add-form")
let totalForms = document.querySelector("#id_form-TOTAL_FORMS")

let formNum = productForm.length-1
addButton.addEventListener('click', addForm)

function addForm(e){
    e.preventDefault()

    let newForm = productForm[0].cloneNode(true)
    let formRegex = RegExp(`form-(\\d){1}-`,'g')

    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
    container.insertBefore(newForm, addButton)

    totalForms.setAttribute('value', `${formNum+1}`)
    newForm.querySelector('.price').addEventListener('input', amountUpdate);
    newForm.querySelector('.quantity').addEventListener('input', amountUpdate);
}

function toggleNewSellerField() {

    var existingSeller = document.getElementById('id_existing_seller');
    var newSeller = document.getElementById('form-create-receipt').getElementsByClassName('row')[1]

    if (existingSeller.value === 'other') {
        newSeller.style.display = 'flex';
    } else {
        newSeller.style.display = 'none';
    }
}

$(function () {
    toggleNewSellerField();
    $('select#existingSeller').change(toggleNewSellerField)
})


function amountUpdate() {
    let formInputs = container.querySelectorAll('.form-product');
    formInputs.forEach( formInput => {
        let priceInput = formInput.querySelector('.price');
        let quantityInput = formInput.querySelector('.quantity');
        let amountInput = formInput.querySelector('.amount');
        if (priceInput && quantityInput && amountInput) {
            amountInput.value = priceInput.value * quantityInput.value;
        }
    });
}

// Attach event listeners to existing inputs
productForm.forEach(form => {
    form.querySelector('.price').addEventListener('input', amountUpdate);
    form.querySelector('.quantity').addEventListener('input', amountUpdate);
});
