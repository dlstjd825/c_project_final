document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_user_info_simple')
    .then(response => response.json())
    .then(data => {
        document.getElementById('loggedInUser_simple').textContent = 'ID' + data.id;
        
    })
    .catch(error => {
        console.error('Error:', error);
        alert("서버 요청 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.");
    })
});