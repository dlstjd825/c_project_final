// 왼쪽 화살표 버튼 클릭 시 메인 페이지로 이동
document.querySelector('.larrow-container').addEventListener('click', function() {
    window.location.href = '/';
});

// 멘티 선택 시 UI 업데이트
document.getElementById('mentee-label').addEventListener('click', function() {
    document.getElementById('mentee-label').classList.add('active');
    document.getElementById('mentor-label').classList.remove('active');
    
    resetFileUpload(); // 파일 업로드 초기화

    document.getElementById('right-section-title').textContent = '학적 확인';
    document.getElementById('right-section-description').innerText = 
        '학적 정보를 인증할 수 있는 파일을 올려주세요!\nex) 학생증, 재학 증명서, 학교 포털사이트 로그인 화면 등\n파일명이 영어인 파일만 업로드해주세요!!!';

});

// 멘토 선택 시 UI 업데이트
document.getElementById('mentor-label').addEventListener('click', function() {
    document.getElementById('mentor-label').classList.add('active');
    document.getElementById('mentee-label').classList.remove('active');
    
    resetFileUpload(); // 파일 업로드 초기화

    document.getElementById('right-section-title').textContent = '멘토 정보';
    document.getElementById('right-section-description').innerText = 
        '멘토로 활동하기 위해 관련 정보를 올려주세요!\nex) 자격증, 포트폴리오 등\n파일명이 영어인 파일만 업로드해주세요!!!';
});

// 성별 버튼 클릭 시 UI 업데이트
document.getElementById('male-button').addEventListener('click', function() {
    document.getElementById('male-button').classList.add('active');
    document.getElementById('female-button').classList.remove('active');
});

document.getElementById('female-button').addEventListener('click', function() {
    document.getElementById('female-button').classList.add('active');
    document.getElementById('male-button').classList.remove('active');
});

// 아이디 입력 시 중복 확인 버튼 초기화
document.getElementById('id-input').addEventListener('input', function() {
    const duplicateButton = document.getElementById('duplicate-check-button');
    duplicateButton.textContent = "중복 확인";
    duplicateButton.style.backgroundColor = "";
    duplicateButton.style.color = "";
    duplicateButton.disabled = false;
});

// 아이디 중복 확인 버튼 클릭 시
document.getElementById('duplicate-check-button').addEventListener('click', function() {
    var idInput = document.getElementById('id-input');
    var userId = idInput.value;

    if (!userId) {
        idInput.style.borderColor = 'red'; // 입력값이 없을 경우 경고 표시
    } else {
        idInput.style.borderColor = '#ddd';

        // 서버에 중복 확인 요청
        fetch('/check_duplicate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: userId })
        })
        .then(response => response.json())
        .then(data => {
            // C함수를 통해서 중복여부 받아옴 (is_duplicate)
            if (data.is_duplicate) {
                alert("아이디가 이미 존재합니다.");
            } else {
                alert("사용 가능한 아이디입니다.");
                const duplicateButton = document.getElementById('duplicate-check-button'    );
                duplicateButton.textContent = "중복 확인 완료";
                duplicateButton.style.backgroundColor = "#ddd";
                duplicateButton.style.color = "#888";
                duplicateButton.disabled = true; // 중복 확인 완료 후 버튼 비활성화
            }
        })
        .catch(error => console.error('Error:', error));
    }
});

// 비밀번호 확인 입력 시 비밀번호 일치 여부 확인
document.getElementById('password-confirm').addEventListener('input', function() {
    var password = document.getElementById('password').value;
    var confirm = document.getElementById('password-confirm').value;
    var warning = document.getElementById('password-warning');

    if (password !== confirm) {
        document.getElementById('password-confirm').style.borderColor = 'red';
        warning.style.display = 'block'; // 비밀번호 불일치 경고 표시
    } else {
        document.getElementById('password-confirm').style.borderColor = '#ddd';
        warning.style.display = 'none';
    }
});

// 생년월일 입력 유효성 검사
document.getElementById('birth-year').addEventListener('input', validateDateInput);
document.getElementById('birth-month').addEventListener('input', validateDateInput);
document.getElementById('birth-day').addEventListener('input', validateDateInput);

function validateDateInput() {
    const year = parseInt(document.getElementById('birth-year').value);
    const month = parseInt(document.getElementById('birth-month').value);
    const day = parseInt(document.getElementById('birth-day').value);

    // 연도 유효성 검사
    if (year < 1900 || year > 2100 || isNaN(year)) {
        document.getElementById('birth-year').style.borderColor = 'red';
    } else {
        document.getElementById('birth-year').style.borderColor = '#ddd';
    }

    // 월 유효성 검사
    if (month < 1 || month > 12 || isNaN(month)) {
        document.getElementById('birth-month').style.borderColor = 'red';
    } else {
        document.getElementById('birth-month').style.borderColor = '#ddd';
    }

    // 일 유효성 검사
    const daysInMonth = new Date(year, month, 0).getDate();
    if (day < 1 || day > daysInMonth || isNaN(day)) {
        document.getElementById('birth-day').style.borderColor = 'red';
    } else {
        document.getElementById('birth-day').style.borderColor = '#ddd';
    }
}

// 업로드된 파일 목록 관리
const uploadedFiles = new Set();

function bindFileUploadEvents() {
    // 파일 업로드 버튼 클릭 시 파일 선택 창 열기
    document.getElementById('upload-button').addEventListener('click', function() {
        document.getElementById('file-upload').click();
    });

    // 파일 선택 시 파일 목록에 추가
    document.getElementById('file-upload').addEventListener('change', function(event) {
        const files = event.target.files;
        const linkContainer = document.getElementById('file-link-container');

        for (let i = 0; i < files.length; i++) {
            const fileName = files[i].name;

            if (uploadedFiles.has(fileName)) {
                alert(`이미 업로드된 파일입니다: ${fileName}`);
                continue;
            }

            uploadedFiles.add(fileName);

            const fileRow = document.createElement('div');
            fileRow.className = 'files';

            const fileLink = document.createElement('a');
            fileLink.href = URL.createObjectURL(files[i]);
            fileLink.download = fileName;
            fileLink.textContent = fileName;

            const cancelButton = document.createElement('button');
            cancelButton.textContent = '업로드 취소';

            // 업로드 취소 버튼 클릭 시 파일 목록에서 제거
            cancelButton.addEventListener('click', function() {
                fileRow.remove(); // UI에서 삭제
                uploadedFiles.delete(fileName); // 업로드된 파일 목록에서 제거
                checkInputs(); // 파일 삭제 후 버튼 상태 업데이트
            });

            fileRow.appendChild(fileLink);
            fileRow.appendChild(cancelButton);
            linkContainer.appendChild(fileRow);
        }

        checkInputs(); // 파일 업로드 시 버튼 상태 업데이트
    });
}

// 파일 업로드 초기화 함수
function resetFileUpload() {
    document.getElementById('file-link-container').innerHTML = '';
    uploadedFiles.clear();
    checkInputs(); // 초기화 후 버튼 상태 업데이트
}

bindFileUploadEvents(); // 파일 업로드 이벤트 바인딩

// 회원가입 버튼 클릭 시 처리
document.getElementById('signup-submit-button').addEventListener('click', function(event) {
    event.preventDefault(); // 폼 기본 제출 방지
    const button = event.target;
    button.disabled = true; // 중복 클릭 방지

    // 회원가입 폼 데이터 수집
    const id = document.getElementById('id-input').value;
    const password = document.getElementById('password').value;
    const name = document.querySelector('input[placeholder="이름"]').value;
    const birthday = `${document.getElementById('birth-year').value}-${document.getElementById('birth-month').value}-${document.getElementById('birth-day').value}`;
    let gender = document.querySelector('.gender-group button.active').textContent;
    gender = (gender === "남자") ? "m" : "w";
    let role = document.querySelector('.radio-group .active').innerText;
    role = (role === "멘토") ? "mentor" : "mentee";
    
    const formData = new FormData();
    formData.append('id', id);
    formData.append('password', password);
    formData.append('role', role);
    formData.append('name', name);
    formData.append('birthday', birthday);
    formData.append('gender', gender);
    
    // 파일 데이터 추가
    const fileInput = document.getElementById('file-upload');
        for (let file of fileInput.files) {
            formData.append('files', file);
        }
    
        // 서버에 회원가입 요청 전송
        fetch('/sign_up.html', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("회원가입 신청이 완료되었습니다! 2~3일 내에 처리가 완료됩니다.");
                window.location.href = '/';
            } else {
                alert("회원가입 신청에 실패했습니다. 잠시 뒤 다시 신청해 주시길 바랍니다.");
                button.disabled = false;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("회원가입 신청에 실패했습니다. 잠시 뒤 다시 신청해 주시길 바랍니다.");
            button.disabled = false;
        });
    });

    // 모든 입력 필드의 값이 입력되었는지 확인하여 회원가입 버튼 활성화
    const inputs = [
    document.getElementById('id-input'),
    document.getElementById('password'),
    document.getElementById('password-confirm'),
    document.querySelector('input[placeholder="이름"]'),
    document.getElementById('birth-year'),
    document.getElementById('birth-month'),
    document.getElementById('birth-day')
];

const signupButton = document.getElementById('signup-submit-button');

function checkInputs() {
    // 모든 필수 입력 필드가 채워졌는지 확인
    const allFilled = inputs.every(input => input.value.trim() !== "");

    // 생년월일 유효성 검사
    const year = parseInt(document.getElementById('birth-year').value);
    const month = parseInt(document.getElementById('birth-month').value);
    const day = parseInt(document.getElementById('birth-day').value);
    const daysInMonth = new Date(year, month, 0).getDate();
    const isDateValid = (
        !isNaN(year) && year >= 1900 && year <= 2100 &&
        !isNaN(month) && month >= 1 && month <= 12 &&
        !isNaN(day) && day >= 1 && day <= daysInMonth
    );

    // 파일 업로드 여부 확인
    const fileUploaded = document.getElementById('file-upload').files.length > 0;

    // 모든 조건 충족 여부 확인
    const canSubmit = allFilled && isDateValid && fileUploaded;

    // 회원가입 버튼 활성화/비활성화 설정
    signupButton.disabled = !canSubmit;
    signupButton.style.backgroundColor = canSubmit ? "#FEE99C" : "#ddd";
}

// 파일 업로드 변경 이벤트 추가
document.getElementById('file-upload').addEventListener('change', checkInputs);

// 파일 삭제 이벤트 추가 (업로드된 파일 목록에서 변경이 있을 때도 확인)
document.getElementById('file-link-container').addEventListener('DOMNodeRemoved', checkInputs);

// 기존 입력 필드 이벤트 추가
inputs.forEach(input => {
    input.addEventListener('input', checkInputs);
});

// 초기 상태에서 버튼 비활성화 설정
checkInputs();

