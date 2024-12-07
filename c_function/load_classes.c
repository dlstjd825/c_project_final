//임수빈
#define _CRT_SECURE_NO_WARNINGS
#include "user.h"
#include "class_management.h" // 클래스 관리와 관련된 함수, 상수를 포함한 헤더 파일 따로 정리.

// CSV 파일에서 클래스 목록을 불러오는 함수
bool load_classes(const char* filename, char classes[][1024], int* count) {
    FILE* file = fopen(filename, "r"); // 파일을 읽기 모드로 열기
    if (file == NULL) { // 파일이 열리지 않으면 오류 메시지 출력 후 함수 종료
        printf("클래스 정보를 불러올 수 없습니다.\n");
        return false;
    }

    char line[MAX_LINE_LENGTH]; // 파일에서 한 줄씩 읽어올 배열 정의
    *count = 0; // 클래스 개수를 0으로 초기화
    while (fgets(line, sizeof(line), file)) { // 파일에서 한 줄씩 읽기
        // 각 정보를 저장할 변수 선언
        char class_title[100], mentor_name[100], location[100], class_description[500];
        char price[20], mode[20], capacity[10], current_applicants[10], image_path[200];

        // 정보들을 쉼표로 구분하여 각각의 변수에 저장
        if (sscanf(line, "%99[^,],%99[^,],%99[^,],%499[^,],%19[^,],%19[^,],%9[^,],%9[^,],%199[^\n]",
            class_title, mentor_name, location, class_description, price, mode, capacity, current_applicants, image_path) == 9) {
            // 각 필드를 문자열 형식으로 배열에 저장
            snprintf(classes[*count], sizeof(line), "%s,%s,%s,%s,%s,%s,%s,%s,%s",
                class_title, mentor_name, location, class_description, price, mode, capacity, current_applicants, image_path);
            (*count)++; // 클래스 개수 증가
        }
    }

    fclose(file); // 파일 닫기
    return true; // 성공적으로 읽었음을 반환
}
