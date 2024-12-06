// user.h 헤더파일 함수 구현
#define _CRT_SECURE_NO_WARNINGS
#include "user.h"

// 사용자를 id순으로 정렬할 함수
int compare_users(const void* a, const void* b) {
    return strcmp(((User*)a)->id, ((User*)b)->id);
}

// 이진 탐색 함수: 정렬된 users 배열에서 id를 찾음
int binary_search(User* users, int left, int right, const char* id) {
    while (left <= right) {
        int mid = left + (right - left) / 2;
        int cmp = strcmp(id, users[mid].id);

        if (cmp == 0) { // ID가 일치하는 경우
            return mid;  // 일치하는 인덱스 반환
        }
        else if (cmp < 0) {
            right = mid - 1;
        }
        else {
            left = mid + 1;
        }
    }   
    return -1;  // ID가 없는 경우
}

// 사용자를 user.csv에서 불러옴
int load_users(User* users, int max_users) {
    FILE* file = fopen("static/user.csv", "r");
    if (file == NULL) {
        perror("Failed to open CSV file");
        return 0;
    }

    int count = 0;
    char line[MAX_LINE_LENGTH];

    while (fgets(line, sizeof(line), file) && count < max_users) {
        // 각 줄에서 모든 필드를 추출하여 User 배열에 저장
        if (sscanf(line, "%49[^,],%49[^,],%9[^,],%9[^,],%49[^,],%49[^,],%1s",
            users[count].id, users[count].pw, users[count].status,
            users[count].role, users[count].name, users[count].birthday, users[count].gender) == 7) {
            // 각 필드에 대해 개행 문자 제거
            trim_newline(users[count].id);
            trim_newline(users[count].pw);
            trim_newline(users[count].status);
            trim_newline(users[count].role);
            trim_newline(users[count].name);
            trim_newline(users[count].birthday);
            trim_newline(users[count].gender);

            count++;
        }
    }

    fclose(file);
    return count;  // 로드된 사용자 수 반환
}

// 문자열에서 개행함수 제거
void trim_newline(char* str) {
    str[strcspn(str, "\n")] = '\0';
    str[strcspn(str, "\r")] = '\0'; // 캐리지 리턴 제거
}

