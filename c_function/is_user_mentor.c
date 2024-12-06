#include "user.h"

// 사용자가 멘토인지 여부를 확인하는 함수
__declspec(dllexport) bool is_user_mentor(const char* user_id) {
    User users[MAX_USERS];  // 사용자 데이터를 저장할 배열
    int user_count = load_users(users, MAX_USERS);  // 사용자 데이터를 로드

    if (user_count == 0) {
        printf("사용자 데이터를 불러오지 못했습니다.\n");
        return false;  // 데이터가 없으면 false 반환
    }

    // 사용자 배열을 ID 기준으로 정렬
    qsort(users, user_count, sizeof(User), compare_users);

    // 이진 탐색을 통해 user_id를 찾음
    int index = binary_search(users, 0, user_count - 1, user_id);
    if (index != -1 && strcmp(users[index].role, "mentor") == 0) {
        return true;  // 사용자가 mentor 역할인 경우 true 반환
    }

    return false;  // 사용자가 mentor가 아니거나 존재하지 않는 경우 false 반환
}
