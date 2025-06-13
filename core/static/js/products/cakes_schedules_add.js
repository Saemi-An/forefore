// days 필드 - 커스텀 체크박스 컨트롤
function checkDays(btnDiv) {
    const checkbox = btnDiv.firstElementChild;

    if (checkbox.classList.contains('btn-check_off')) {
    checkbox.classList.replace('btn-check_off', 'btn-check_on');
    } else {
    checkbox.classList.replace('btn-check_on', 'btn-check_off');
    }
}

// 폼 제출
function submitScheduleForm(event) {
    event.preventDefault();

    // 선택된 요일들 비트마스킹 값으로 변환하여 hiddenDaysInput에 value 주기
    const hiddenDaysInput = document.getElementById('hiddenDaysInput');
    let bitmask = 0;
    const checkedBoxes = document.querySelectorAll('.btn-check_on')
    if (checkedBoxes.length > 0) {
        checkedBoxes.forEach(box => {
            bitmask |= (1 << parseInt(box.dataset['selected']))
        })
        hiddenDaysInput.value = bitmask;
    }

    document.getElementById('scheduleForm').submit();
}

// 비트마스킹값 숫자로 변환
function decodeBitmask(bitmask) {
  const decodedDays = [];

  for (let i = 0; i <= 6; i++) {
    if (bitmask & (1 << i)) {
      decodedDays.push(i);
    }
  }

  return decodedDays;
}

// edit 요청시 기존 요일값 체크해두기
function initEditForm() {
  const hiddenDaysInput = document.getElementById('hiddenDaysInput');
  
  // 수정 페이지에서 기존 선택된 요일 체크해두기
  if (hiddenDaysInput.value) {
    const selectedDaysAry = decodeBitmask(hiddenDaysInput.value);
    selectedDaysAry.forEach(intDay =>  {
      document.querySelector(`[data-selected="${intDay}"]`).classList.replace('btn-check_off', 'btn-check_on');
    });
  
  }
}
initEditForm();
