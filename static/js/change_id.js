//정세은
document.getElementById('idForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const oldId = document.getElementById('oldIdInput').value;
    const newId = document.getElementById('newIdInput').value;

    if (oldId === "" || newId === "") {
        alert("현재 아이디와 새 아이디를 입력해주세요.");
        return;
    }

    // 백엔드에 아이디 변경 요청 보냄
    fetch('/change_id', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ old_id: oldId, new_id: newId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("아이디가 성공적으로 변경되었습니다. 변경된 아이디로 다시 로그인 해주세요.");
            document.getElementById("idModal").style.display = "none";
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

// 모달 닫기
document.querySelector("#idModal .close").onclick = function() {
    document.getElementById("idModal").style.display = "none";
};

// 모달 외부 클릭 시 닫기
window.onclick = function(event) {
    if (event.target == document.getElementById("idModal")) {
        document.getElementById("idModal").style.display = "none";
    }
};
