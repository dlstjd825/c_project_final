//정세은
#define _CRT_SECURE_NO_WARNINGS
#include "user.h"

__declspec(dllexport) bool change_id(const char* old_id, const char* new_id) {
    // 힙 메모리에 User 배열 할당
    User* users = (User*)malloc(MAX_USERS * sizeof(User));
    if (users == NULL) {
        printf("Memory allocation failed.\n");
        return false;
    }

    int num_users = load_users(users, MAX_USERS);

    if (num_users == 0) {
        printf("No users loaded.\n");
        free(users); // 메모리 해제
        return false;
    }

    // User 배열을 ID 기준으로 정렬
    qsort(users, num_users, sizeof(User), compare_users);

    // 기존 아이디가 있는지 확인
    int index = binary_search(users, 0, num_users - 1, old_id);
    if (index == -1) {
        printf("User not found.\n");
        free(users); // 메모리 해제
        return false;
    }

    // 새 아이디가 중복되는지 확인
    if (binary_search(users, 0, num_users - 1, new_id) != -1) {
        printf("New ID already exists.\n");
        free(users); // 메모리 해제
        return false;
    }

    // 아이디 변경
    strcpy(users[index].id, new_id);

    // 변경된 사용자 정보를 CSV 파일에 다시 저장
    FILE* csv_file = fopen("static/user.csv", "w");
    if (!csv_file) {
        perror("Failed to open CSV file for writing");
        free(users); // 메모리 해제
        return false;
    }

    for (int i = 0; i < num_users; i++) {
        fprintf(csv_file, "%s,%s,%s,%s,%s,%s,%s\n",
            users[i].id, users[i].pw, users[i].status,
            users[i].role, users[i].name, users[i].birthday, users[i].gender);
    }

    fclose(csv_file);
    free(users); // 메모리 해제

    return true;
}
