// ======================== 상품 이미지 필드 컨트롤 ========================
// '파일 선택' 버튼 클릭시
document.getElementById('fileUpload').addEventListener('change', (event) => {
    // 파일명 노출
    const uploadedFile = event.target.files[0];
    if (uploadedFile) {
        const customSpan = document.getElementById('customSpan');
        customSpan.textContent = uploadedFile.name
    }
    // 파일 프리뷰
    const fileReader = new FileReader;
    fileReader.onload = (e) => {
        const imgPreviewDiv = document.getElementById('imgPreviewDiv');
        imgPreviewDiv.classList.remove('display-none');
        imgPreviewDiv.firstElementChild.src = e.target.result;
    }
    fileReader.readAsDataURL(uploadedFile);   // 이걸 호출해야 브라우저가 파일을 읽고, onload 콜백이 실행됨
})

// 수정 페이지에서 불필요한 디폴트 요소 제거
Array.from(document.getElementById('uploadDiv').childNodes).forEach(child => {
    // 차일드노드 타입이 엘리먼트인 경우 
    if (child.nodeType === Node.ELEMENT_NODE) {
        if (child.tagName != 'LABEL' && child.tagName != 'SPAN' && child.tagName != 'INPUT') {
            child.style.display = 'none';   // <a>, <br> 안보이도록 처리
        }
    // 차일드노드 타입이 텍스트노드이면서 텍스트노드가 공백이 아닐 경우 제거
        // trim()은 문자열 처음과 끝의 공백제거 - '    '.trim() --> ''
        // 공백('')은 조건문에서 false로 분류됨
    // 두번째 조건 없을 경우, 줄바꿈('\n'), 들여쓰기('\t') 등 '공백만 있는 노드'들도 제거하는 불필요한 연산이 추가적으로 실행됨
    // 두번째 조건이 있으면 '의미 있는 텍스트'들만 깔끔하게 제거 가능
    // 결론적으로, 그냥 습관적으로 넣는것이 안전함
    } else if (child.nodeType === Node.TEXT_NODE && child.textContent.trim()) {
        child.parentNode.removeChild(child);
    }
})
