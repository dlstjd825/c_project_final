// 비밀번호 변경 모달 열기
document.getElementById("change-password").onclick = function() {
    document.getElementById("passwordModal").style.display = "block";
}

// 비밀번호 변경 처리
document.getElementById('passwordForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const id = document.getElementById('idInput').value;
    const oldPassword = document.getElementById('oldPasswordInput').value;
    const newPassword = document.getElementById('newPasswordInput').value;
    const confirmNewPassword = document.getElementById('confirmNewPasswordInput').value;

    if (newPassword !== confirmNewPassword) {
        alert("새 비밀번호가 일치하지 않습니다.");
        return;
    }

    fetch('/change_password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id, oldPassword: oldPassword, newPassword: newPassword })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("비밀번호가 성공적으로 변경되었습니다. 변경된 비밀번호로 다시 로그인 해주세요.");
            document.getElementById('passwordModal').style.display = 'none';
            window.location.replace('/');
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("서버 요청 중 문제가 발생했습니다. 잠시 후 다시 시도해주세요.");
    })
});
