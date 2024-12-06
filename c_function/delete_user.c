// 회원 정보 삭제
#define _CRT_SECURE_NO_WARNINGS
#include "user.h"

// delete_user 함수를 DLL로 내보내기
__declspec(dllexport) bool delete_user(const char* ID) {
    // 힙 메모리에 User 배열 할당
    User* users = (User*)malloc(MAX_USERS * sizeof(User));
    if (users == NULL) {
        // 메모리 할당 실패 처리
        printf("Memory allocation failed.\n");
        return false;
    }

    int num_users = load_users(users, MAX_USERS);

    if (num_users == 0) {
        printf("No users loaded.\n");
        free(users); // 메모리 해제
        return false;
    }

    // 사용자 배열을 ID를 기준으로 정렬
    qsort(users, num_users, sizeof(User), compare_users);

    // 이진 탐색으로 삭제할 사용자 찾기
    int index = binary_search(users, 0, num_users - 1, ID);
    if (index == -1) {
        printf("User not found.\n");
        free(users); // 메모리 해제
        return false;
    }

    // CSV 파일을 열어 삭제할 사용자를 제외한 모든 사용자 다시 기록
    FILE* temp_file = fopen("static/temp_user.csv", "w");
    if (!temp_file) {
        perror("Failed to open temp CSV file");
        free(users); // 메모리 해제
        return false;
    }

    for (int i = 0; i < num_users; i++) {
        if (i != index) {  // 삭제할 ID가 아닌 사용자만 기록
            fprintf(temp_file, "%s,%s,%s,%s,%s,%s,%s\n", users[i].id, users[i].pw, users[i].status,
                users[i].role, users[i].name, users[i].birthday, users[i].gender);
        }
    }

    fclose(temp_file);

    // 기존 user.csv를 temp_user.csv로 대체
    remove("static/user.csv");
    rename("static/temp_user.csv", "static/user.csv");

    // 메모리 해제
    free(users);

    return true;
}


