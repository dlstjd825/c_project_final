//우재연
// 프로필 불러오기
document.addEventListener("DOMContentLoaded", () => {
    fetch('/get-profile-picture-post')
        .then(response => response.json())
        .then(data => {
            console.log(data); // 서버 응답 확인
            if (data.success) {
                const profilePicture = document.getElementById("profile-picture");
                console.log("Setting src to:", data.photo); // photo 경로 디버깅
                profilePicture.src = data.photo; // 프로필 사진 경로 설정
            } else {
                console.error(data.message);
            }
        })
        .catch(error => {
            console.error("Error fetching profile picture:", error);
        });
});




// 게시글 삭제 버튼 이벤트
const deletePostButton = document.getElementById('deletePostButton');
if (deletePostButton) {
    deletePostButton.addEventListener('click', () => {
        fetch(`/delete_post/{{ post.image_path }}`, {
            method: 'POST'
        })
        .then(response => {
            if (response.ok) {
                alert("게시글이 삭제되었습니다.");
                window.location.href = '/main'; // 커뮤니티 메인 페이지로 이동
            } else {
                alert("게시글 삭제에 실패했습니다.");
            }
        });
    });
}


// 댓글 삭제
document.getElementById('comments').addEventListener('click', (event) => {
    if (event.target.classList.contains('delete-comment-button')) {
        const button = event.target;
        const commentId = button.getAttribute('data-comment-id');
        const postId = "{{ post.image_path }}";

        console.log("Deleting comment with ID:", commentId);

        if (confirm("정말로 이 댓글을 삭제하시겠습니까?")) {
            fetch('/delete_comment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({
                    comment_id: commentId,
                    post_id: postId
                })
            })
            .then(response => {
                if (response.ok) {
                    alert("댓글이 삭제되었습니다.");
                    location.reload();
                } else {
                    alert("댓글 삭제에 실패했습니다.");
                }
            });
        }
    }
});

// 좋아요 버튼 이벤트
const likeButton = document.querySelector('.like-button');
const likeIcon = likeButton.querySelector('i');

likeButton.addEventListener('click', () => {
    const userId = "{{ session.get('user_id', '') }}"; // 세션에 저장된 user_id 가져오기
    if (!userId) {
        alert("로그인이 필요합니다. 로그인 후 좋아요를 눌러주세요.");
        return; // user_id가 없으면 좋아요 요청 보내지 않음
    }

    if (likeIcon.classList.contains('far')) {
        likeIcon.classList.remove('far');
        likeIcon.classList.add('fas');
    } else {
        likeIcon.classList.remove('fas');
        likeIcon.classList.add('far');
    }

    // 서버에 좋아요 요청 보내기
    fetch('/like_post', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
            image_path: "{{ post.image_path }}"
        })
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 403) {
                alert("로그인이 필요합니다. 로그인 후 다시 시도해주세요.");
            } else {
                alert("좋아요 요청에 실패했습니다.");
            }
        }
    });
});

// 댓글 작성 이벤트
const postImagePath = "{{ post.image_path }}";  // 템플릿 변수로 값 렌더링
const commentButton = document.getElementById('commentButton');
const commentInput = document.getElementById('commentInput');

commentButton.addEventListener('click', () => {
    const commentText = commentInput.value.trim();
    if (commentText) {
        fetch('/add_comment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({
                user: "{{ session.get('user_id', '익명') }}",
                text: commentText,
                post_id: postImagePath  // 서버에서 렌더링된 image_path 전달
            })
        })
        .then(response => {
            if (response.ok) {
                alert("댓글이 추가되었습니다.");
                location.reload();
            } else {
                alert("댓글 추가에 실패했습니다.");
            }
        });
    }
});

// 팝업 닫기 버튼 이벤트
document.querySelector('.close-button').addEventListener('click', () => {
    window.location.href = '/main';  // 커뮤니티 메인 페이지로 이동
});