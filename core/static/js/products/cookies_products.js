function getFilteredProducts() {
    const stringFilter = document.querySelector('select[name="product_category"]').value;
    location.href=`/manager/cookies-products/${stringFilter}/`;
}