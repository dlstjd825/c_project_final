//정인성
// 멘티/멘토 신청 수락 처리 함수
function acceptSignup(userId) {
    fetch(`/signup_accept/${userId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`${userId}의 신청이 수락되었습니다.`);
            document.getElementById(`row-${userId}`).remove();
        } else {
            alert("신청 수락에 실패했습니다.");
        }
    })
    .catch(error => console.error('Error:', error));
}

// 멘티/멘토 신청 거절 처리 함수
function rejectSignup(userId) {
    fetch(`/signup_reject/${userId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`${userId}의 신청이 거절되었습니다.`);
            document.getElementById(`row-${userId}`).remove();
        } else {
            alert("신청 거절에 실패했습니다.");
        }
    })
    .catch(error => console.error('Error:', error));
}

// 로그아웃 함수
function admin_logout() {
    window.location.href = '/admin_logout';
}


