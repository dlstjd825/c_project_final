// "로그인"버튼 클릭했을 때 로그인 처리
document.getElementById('login-button').addEventListener('click', function() {
    const id = document.getElementById('login-id').value;
    const password = document.getElementById('login-password').value;

    if (id === "" || password === "") {
        alert("아이디와 비밀번호를 입력해주세요.");
        return;
    }
    
    // 백엔드에 로그인 요청 보냄
    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id, password: password }) // 변수 이름 수정
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect;
        } else if (data.message === "회원가입이 거절되었습니다.") {
            // 거절된 사용자에 대한 알림 (확인 버튼만 표시)
            alert(data.message);
            
            // 회원 정보 삭제 요청
            fetch('/delete_rejected_user', { method: 'POST' })
                .then(response => response.json())
                .then(result => {
                    if (result.success) {
                        alert("회원 정보가 삭제되었습니다.");
                        window.location.href = '/';
                    } else {
                        alert("회원 정보 삭제에 실패했습니다.");
                    }
                })
                .catch(error => console.error('Error:', error));
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});    

