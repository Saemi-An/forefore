// 노말 모달 컨트롤 =============================================================================================================================
function showNormalModal() {document.getElementById('normalModal').style.display = 'block';}
function closeNormalModal(){document.getElementById('normalModal').style.display = 'none';}

// 픽업 모달 컨트롤 =============================================================================================================================
function showPickupModal(){document.getElementById('pickupModal').style.display = 'block'};
function closePickupModal(){
    document.getElementById('pickupModal').style.display = 'none'
    document.getElementById('checkSelectedMsg').style.display = 'none'
};

// 체크박스
function selectPickupTimes(event){
    const button = event.currentTarget;
    const toggleDiv = button.querySelector('div[class^="btn-check_"]');

    toggleDiv.classList.toggle('btn-check_on');
    toggleDiv.classList.toggle('btn-check_off');
}

// 유효성 검사
function checkPickupModal() {
    const selectedDivs = document.querySelectorAll('div.btn-check_on');
    const checkSelectedMsg = document.getElementById('checkSelectedMsg');

    let selectedTimeIds = '';
    selectedDivs.forEach(div => {
        selectedTimeIds += ` ${div.dataset.selected}`;
    });
    const hiddenInput = document.querySelector('input[name="selected_times"]');
    hiddenInput.value = selectedTimeIds;

    // if (selectedDivs.length) {
    //     let selectedTimeIds = '';
    //     selectedDivs.forEach(div => {
    //         selectedTimeIds += ` ${div.dataset.selected}`;
    //     });
    //     const hiddenInput = document.querySelector('input[name="selected_times"]');
    //     hiddenInput.value = selectedTimeIds;
    //     return true
    // } else {
    //     checkSelectedMsg.style.display = 'block';
    //     return false
    // }
}

// 제출
function submitPickupModal(event){
    event.preventDefault();
    let flag = checkPickupModal();
    pickupModalForm.submit();
}

// 폼 모달 컨트롤 =============================================================================================================================
// 열기 + action 변경
function showFormModal() {
    // 폼 action 변경: 새로운 구움과자 추가
    const addCookieForm = document.getElementById('addCookieForm');
    const actionUrl = 'add/0';
    addCookieForm.action = actionUrl;

    document.getElementById('formModal').style.display = 'block';
}
// 닫기 + action 리셋
function closeFormModal() {
    // 폼 action 변경: 초기화
    const addCookieForm = document.getElementById('addCookieForm');
    addCookieForm.action = '';

    document.getElementById('formModal').style.display = 'none';
}

// 유효성 검사
function checkSelectProduct() {
    const selectProductMsg = document.getElementById('selectProductMsg');
    if (document.getElementById('selectProduct').value === ''){
        selectProductMsg.innerText = '필수 입력값 입니다.';
        selectProductMsg.classList.remove('display-none');
        return false
    }
    else {
        selectProductMsg.classList.add('display-none');
        return true
    }
}
function checkSelectStatus() {
    const selectStatusMsg = document.getElementById('selectStatusMsg');
    if (document.getElementById('selectStatus').value === '') {
        selectStatusMsg.innerText = '필수 입력값 입니다.';
        selectStatusMsg.classList.remove('display-none');
        return false
    } else {
        selectStatusMsg.classList.add('display-none');
        return true
    }
}
function checkInputTotal() {
    const inputTotal = document.getElementById('inputTotal');
    const inputTotalMsg = document.getElementById('inputTotalMsg');
    if (inputTotal.value === '') {
        inputTotalMsg.innerText = '필수 입력값 입니다.';
        inputTotalMsg.classList.remove('display-none');
        return false
    } else {
        inputTotalMsg.classList.add('display-none');
        return true
    }
}
function checkInputSafe() {
    const inputSafe = document.getElementById('inputSafe');
    const inputSafeMsg = document.getElementById('inputSafeMsg');
    if (inputSafe.value === '') {
        inputSafeMsg.innerText = '필수 입력값 입니다.';
        inputSafeMsg.classList.remove('display-none');
        return false
    } else {
        inputSafeMsg.classList.add('display-none');
        return true
    }
}
function compareTotalAndSafe() {
    const inputTotal = document.getElementById('inputTotal');
    const inputSafe = document.getElementById('inputSafe');
    const inputSafeMsg = document.getElementById('inputSafeMsg');
    
    if (inputTotal.value !== '' && inputSafe !== '') {
        if (parseInt(inputTotal.value) <= parseInt(inputSafe.value)) {
            inputSafeMsg.innerText = '안전 재고 수량은 전체 재고 수량보다 작아야 합니다.';
            inputSafeMsg.classList.remove('display-none');
            return false
        } else {
            inputSafeMsg.classList.add('display-none');
            return true
        }
    }
}

// 제출
function submitCookieAdd(event) {
    event.preventDefault();
    
    let check1 = checkSelectProduct();
    let check2 = checkSelectStatus();
    let check3 = checkInputTotal();
    let check4 = checkInputSafe();
    let check5 = compareTotalAndSafe();

    if (check1 && check2 && check3 && check4 && check5) {
        addCookieForm.submit();
    }
}

// 판매 구움과자 수정시 GET 요청 + 폼 모달 열기
function getEditCookieModal(pk) {
    fetch(`/api/cookie/${pk}`, {   // '/'로 시작하는 절대경로
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(data => {
        // product 필드
        const selectProduct = document.getElementById('selectProduct');
        let newOption = `<option value=${data.product.id} selected>${data.product.name}</option>`
        selectProduct.innerHTML += newOption;
        selectProduct.classList.add('no-select');
        
        // status 필드
        const selectStatus = document.getElementById('selectStatus');
        let selectedOption = document.querySelector(`#selectStatus option[value="${String(data.status)}"]`)
        selectedOption.setAttribute('selected', '');
        
        // total 필드
        const inputTotal = document.getElementById('inputTotal');
        inputTotal.value = `${data.total}`;
        
        // safe 필드
        const inputSafe = document.getElementById('inputSafe');
        inputSafe.value = `${data.safe}`;

        // 폼 action 변경
        const addCookieForm = document.getElementById('addCookieForm');
        const actionUrl = `add/${data.id}`;
        addCookieForm.action = actionUrl;

        // 폼 모달 노출
        const formModal = document.getElementById('formModal');
        formModal.style.display = 'block';
    })
}

