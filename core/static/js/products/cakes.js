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