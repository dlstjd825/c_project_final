document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_user_info')
    .then(response => response.json())
    .then(data => {
        document.getElementById('loggedInUser').textContent = 'ID' + data.id;
        
        document.getElementById('userPageTitle').textContent = data.id + '님의 페이지';

        //document.getElementById('userSubTitle').textContent = data.subtitle || '수식어';
    })
    .catch(error => {
        console.error('Error:', error);
        alert("서버 요청 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.");
    })
});