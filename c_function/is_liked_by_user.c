//우재연,정인성
#define _CRT_SECURE_NO_WARNINGS
#include "user.h"

// 특정 사용자가 특정 이미지를 좋아요 했는지 확인하는 함수
__declspec(dllexport) bool is_liked_by_user(const char* user_id, const char* image_path) {
    // 사용자 데이터 로드
    User users[MAX_USERS];
    int user_count = load_users(users, MAX_USERS);

    if (user_count == 0) {
        printf("사용자 데이터를 불러오지 못했습니다.\n");
        return false;  // 데이터를 로드하지 못하면 false 반환
    }

    // 사용자 배열 정렬
    qsort(users, user_count, sizeof(User), compare_users);

    // user_id를 이진 탐색으로 찾음
    int user_index = binary_search(users, 0, user_count - 1, user_id);

    if (user_index == -1) {
        printf("사용자를 찾을 수 없습니다: %s\n", user_id);
        return false;  // 사용자 ID가 존재하지 않으면 false 반환
    }

    // likes.csv 파일 열기
    FILE* file = fopen("static/likes.csv", "r");
    if (file == NULL) {
        perror("Failed to open likes.csv");
        return false;  // 파일 열기 실패 시 false 반환
    }

    char line[MAX_LINE_LENGTH];
    char csv_user_id[50];
    char csv_image_path[255];

    // likes.csv에서 한 줄씩 읽어와 user_id와 image_path 확인
    while (fgets(line, sizeof(line), file)) {
        if (sscanf(line, "%49[^,],%254[^,],%*s", csv_user_id, csv_image_path) == 2) {
            trim_newline(csv_user_id);
            trim_newline(csv_image_path);

            if (strcmp(csv_user_id, users[user_index].id) == 0 && strcmp(csv_image_path, image_path) == 0) {
                fclose(file);
                return true;  // 좋아요 데이터가 발견되면 true 반환
            }
        }
    }

    fclose(file);  // 파일 닫기
    return false;  // 좋아요 데이터가 없으면 false 반환
}
