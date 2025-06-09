function submitForm(event) {
    event.preventDefault();
    
    const productFilterForm = document.getElementById('productFilterForm');
    const stringFilter = document.querySelector('select[name="product_category"]').value;
    productFilterForm.action = `/manager/cookies-products/${stringFilter}/`;
    productFilterForm.submit();
}