//임수빈
#define _CRT_SECURE_NO_WARNINGS
#include "user.h"
#include "class_management.h" // 클래스 관리와 관련된 함수, 상수를 포함한 헤더 파일 따로 정리.

// 특정 클래스 제목을 기반으로 csv 파일에서 해당 클래스의 세부 정보를 찾는 함수
bool load_class_details(const char* class_title, char* class_details) {
    // CSV 파일을 읽기 모드로 열기
    FILE* file = fopen("static/classes.csv", "r");
    if (file == NULL) { // 파일이 열리지 않으면 오류 메시지 출력 후 함수 종료
        printf("클래스 정보를 불러올 수 없습니다.\n");
        return false;
    }

    char line[1024];
    while (fgets(line, sizeof(line), file)) { // 파일에서 한 줄씩 읽기
        // 읽은 줄에 특정 클래스 제목이 포함되어 있는지 확인
        if (strstr(line, class_title) != NULL) {
            // class_details(연결된 파이썬 함수!)에 클래스 정보가 담긴 해당 줄 저장
            strcpy(class_details, line);
            fclose(file); // 파일 닫기
            return true;
        }
    }

    fclose(file); // 파일을 다 읽은 후 닫기
    return false;
}
