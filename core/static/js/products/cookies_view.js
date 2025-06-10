// 모달 여닫을때 html 스크롤 활성/비활성화
function fixBody() {document.documentElement.style.overflow = 'hidden';} 
function unfixBody() {document.documentElement.style.overflow = '';}

// 구움과자 판매 상태 GET 요청
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

// 필드 기본값 채우기
function fillInEditForm(data) {
    const selectProduct = document.getElementById('selectProduct');
    const inputTotal = document.getElementById('inputTotal');
    const inputSafe = document.getElementById('inputSafe');
    
    // product 필드
    let newOption = `<option value=${data.product.id} selected>${data.product.name}</option>`
    selectProduct.innerHTML += newOption;

    // status 필드
    let selectedOption = document.querySelector(`#selectStatus option[value="${String(data.status)}"]`)
    selectedOption.setAttribute('selected', '');
    
    // total & safe 필드
    inputTotal.value = `${data.total}`;
    inputSafe.value = `${data.safe}`;
}

// 폼 모달 노출 + 기본값 채우기 + 특정 필드 활성/비활성
function showFormModal(pk) {
    fetch(`/api/cookie/${pk}`, {   // '/'로 시작하는 절대경로
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(async data => {
        // status, total, safe 기본값 주기
        fillInEditForm(data);

        // sales 상태에 따라 total, safe 필드 비활성화
        const SalesStatus = await getCookieSalesStatus();
        
        if (SalesStatus) {
            const inputTotal = document.getElementById('inputTotal');
            const inputSafe = document.getElementById('inputSafe');
            inputTotal.classList.add('no-input');
            inputSafe.classList.add('no-input');
        }

        // 폼 모달 노출
        document.getElementById('formModal').style.display = 'block';
        fixBody();
    })
}
// 폼 모달 닫기
function closeFormModal() {
    document.getElementById('formModal').style.display = 'none';
    unfixBody();
}
// 유효성 검사
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
// 폼 제출 + 유효성 검사
function submitCookieAdd(event) {
    event.preventDefault();
    
    let check1 = checkSelectStatus();
    let check2 = checkInputTotal();
    let check3 = checkInputSafe();
    let check4 = compareTotalAndSafe();

    if (check1 && check2 && check3 && check4) {
        addCookieForm.submit();
    }
}
