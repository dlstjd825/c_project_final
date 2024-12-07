//우재연,정인성
#include "user.h"

// 승인된 사용자인지 확인하는 함수
__declspec(dllexport) int is_user_valid(const char* user_id) {
    User users[MAX_USERS];  // 사용자 데이터를 저장할 배열
    int user_count = load_users(users, MAX_USERS);  // 사용자 데이터를 로드

    if (user_count == 0) {
        printf("사용자 데이터를 불러오지 못했습니다.\n");
        return 0;  // 데이터가 없으면 실패
    }

    // 사용자 배열을 ID 기준으로 정렬
    qsort(users, user_count, sizeof(User), compare_users);

    // 이진 탐색을 통해 user_id를 찾음
    int index = binary_search(users, 0, user_count - 1, user_id);
    if (index != -1 && strcmp(users[index].status, "approved") == 0) {
        return 1;  // 승인된 사용자
    }

    return 0;  // 승인되지 않거나 사용자가 존재하지 않음
}
