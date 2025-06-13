function getFilteredOptions() {
    const stringFilter = document.querySelector('select[name="option_types"]').value;
    location.href=`/manager/cakes-options/${stringFilter}/`;
}