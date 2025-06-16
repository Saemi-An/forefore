// ===================================== 햄버거 메뉴 컨트롤 =====================================
// 페이지 오픈시 로컬 스토리지에 따라 nav 접힌/펼쳐진 상태로 렌더링
const isHamburgerClosed = localStorage.getItem('isHamburgerClosed') === 'true';
if (isHamburgerClosed) {
    document.getElementById('navPanel').classList.add('display-none')
} else {
    document.getElementById('navPanel').classList.remove('display-none')
}
// 햄버거 아이콘 클릭시 접기/펼치기 + 로컬 스토리지 저장
document.getElementById('hamburgerIcon').addEventListener('click', () => {
    const hamburgerStatus = document.getElementById('navPanel').classList.toggle('display-none');

    localStorage.setItem('isHamburgerClosed', hamburgerStatus);   // true 또는 false 저장
})

// ===================================== nav 컨트롤 =====================================
function showCookieSection() {
    const cookieDiv = document.getElementById('cookieDiv');
    const cookieSubMenu = document.getElementById('cookieSubMenu');
    const cookieDivIcon = document.getElementById('cookieDivIcon');
    
    if (cookieSubMenu.classList.contains('display-none')) {   // 펼치기
        cookieDiv.classList.add('active');
        cookieSubMenu.classList.remove('display-none');
        cookieDivIcon.innerText = '📖';
    } else {   // 접기
        cookieDiv.classList.remove('active');
        cookieSubMenu.classList.add('display-none');
        cookieDivIcon.innerText = '📘';
    }
}
function showCakeSection() {
    const cakeDiv = document.getElementById('cakeDiv');
    const cakeSubMenu = document.getElementById('cakeSubMenu');
    const cakeDivIcon = document.getElementById('cakeDivIcon');
    
    if (cakeSubMenu.classList.contains('display-none')) {   // 펼치기
        cakeDiv.classList.add('active');
        cakeSubMenu.classList.remove('display-none');
        cakeDivIcon.innerText = '📖';
    } else {   // 접기
        cakeDiv.classList.remove('active');
        cakeSubMenu.classList.add('display-none');
        cakeDivIcon.innerText = '📘';
    }
}
// ===================================== 공통 =====================================
// 뒤로가기 버튼
function goBack() {history.back();}

// 토스트 메세지
window.addEventListener('DOMContentLoaded', () => {
    const toastUl = document.getElementById('toastUl');
    if (toastUl){
        setTimeout(() => {toastUl.classList.add('show')}, 100);   // 최초 로딩시 100ms 지연
        setTimeout(() => {toastUl.classList.remove("show")}, 3100);   // 3초 뒤 숨기기
    }
})