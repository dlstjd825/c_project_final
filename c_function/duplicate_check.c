//정인성
//아이디 중복 체크
#include "user.h"

// 중복 확인 함수
__declspec(dllexport) bool duplicate_check(const char* id) {
    User* users = (User*)malloc(MAX_USERS * sizeof(User));
    if (users == NULL) {
        // 메모리 할당 실패 처리
        return false;
    }

    int num_users = load_users(users, MAX_USERS);

    // 정렬 (필요할 경우)
    qsort(users, num_users, sizeof(User), compare_users);

    // 이진 탐색으로 중복 여부 확인
    bool result = binary_search(users, 0, num_users - 1, id) == -1 ? false : true;

    // 메모리 해제
    free(users);

    return result;
}

