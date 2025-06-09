// 모달 여닫을때 html 스크롤 활성/비활성화
function fixBody() {document.documentElement.style.overflow = 'hidden';} 
function unfixBody() {document.documentElement.style.overflow = '';}

// 노말 모달 컨트롤 =============================================================================================================================
function showNormalModal(){
    document.getElementById('normalModal').style.display = 'block';
    fixBody();
}
function closeNormalModal(){
    document.getElementById('normalModal').style.display = 'none';
    unfixBody();
}

// 픽업 모달 컨트롤 =============================================================================================================================
function showPickupModal(){
    document.getElementById('pickupModal').style.display = 'block'
    fixBody();
};
function closePickupModal(){
    document.getElementById('pickupModal').style.display = 'none'
    document.getElementById('checkSelectedMsg').style.display = 'none'
    unfixBody();
};

// 체크박스 on/off
function selectPickupTimes(event){
    const button = event.currentTarget;
    const toggleDiv = button.querySelector('div[class^="btn-check_"]');

    toggleDiv.classList.toggle('btn-check_on');
    toggleDiv.classList.toggle('btn-check_off');
}

// 유효성 검사
function checkPickupModal() {
    const selectedDivs = document.querySelectorAll('div.btn-check_on');

    let selectedTimeIds = '';
    selectedDivs.forEach(div => {
        selectedTimeIds += ` ${div.dataset.selected}`;
    });
    const hiddenInput = document.querySelector('input[name="selected_times"]');
    hiddenInput.value = selectedTimeIds;
}

// 제출
function submitPickupModal(event){
    event.preventDefault();
    let flag = checkPickupModal();
    pickupModalForm.submit();
}

// 폼 모달 컨트롤 =============================================================================================================================
// 상품 추가 모달 열기
function showFormModal() {
    document.getElementById('formModal').style.display = 'block';
    fixBody();
}
// 닫기
function closeFormModal() {
    fillInEditForm(false, null);
    document.getElementById('formModal').style.display = 'none';
    unfixBody();
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
        document.getElementById('addCookieFormTitle').innerText = '⚡️ 판매 상품 추가 ⚡️';
        addCookieForm.submit();
    }
}

// 수정폼 변경사항
function fillInEditForm(beforeSubmit, data) {
    const selectProduct = document.getElementById('selectProduct');
    const selectStatus = document.getElementById('selectStatus');
    const inputTotal = document.getElementById('inputTotal');
    const inputSafe = document.getElementById('inputSafe');
    const addCookieForm = document.getElementById('addCookieForm');
    const addCookieFormTitle = document.getElementById('addCookieFormTitle');

    if (beforeSubmit) {
        // 폼 action 변경
        addCookieForm.action = `/manager/cookies/add/${data.id}/`;

        // 폼 모달 타이틀 변경
        addCookieFormTitle.innerText = '⚡️ 판매 상품 수정 ⚡️';

        // product 필드
        let newOption = `<option value=${data.product.id} selected>${data.product.name}</option>`
        selectProduct.innerHTML += newOption;
        selectProduct.classList.add('no-select');
        
        // status 필드
        let selectedOption = document.querySelector(`#selectStatus option[value="${String(data.status)}"]`)
        selectedOption.setAttribute('selected', '');
        
        // total & safe 필드
        inputTotal.value = `${data.total}`;
        inputSafe.value = `${data.safe}`;

    } else {
        // action 및 타이틀 초기화
        addCookieForm.action = '/manager/cookies/add/0/';
        addCookieFormTitle.innerText = '⚡️ 판매 상품 추가 ⚡️';
        // product 필드 초기화
        selectProduct.classList.remove('no-select');
        document.querySelector('#selectProduct option[selected=""]')?.removeAttribute('selected');
        // status 필드 초기화
        document.querySelectorAll('#selectStatus option').forEach(opt => opt.removeAttribute('selected'));
        // total & safe 필드 초기화
        inputTotal.value = '';
        inputTotal.classList.remove('no-input');
        inputSafe.value = '';
        inputSafe.classList.remove('no-input');
    }

}

// 상품 수정 모달 열기
// 타겟 구움과자 정보 GET 요청
    // 수정폼 변경사항 적용 + 모달 노출
function showEditFormModal(pk) {
    fetch(`/api/cookie/${pk}`, {   // '/'로 시작하는 절대경로
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(async data => {
        // 수정 요청된 Cookie 정보 채우기
        fillInEditForm(true, data);

        // sales 상태에 따라 total, safe 비활성화
        const SalesStatus = await getCookieSalesStatus();
        
        if (SalesStatus) {
            // 처리
            const inputTotal = document.getElementById('inputTotal');
            const inputSafe = document.getElementById('inputSafe');
            inputTotal.classList.add('no-input');
            inputSafe.classList.add('no-input');
        }

        // 폼 모달 노출
        showFormModal();
    })
}

async function getCookieSalesStatus() {
    const response = await fetch('/api/cookie-sales-status', {   // '/'로 시작하는 절대경로
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    });
    const data = await response.json()
    return data.on_sale;
}

