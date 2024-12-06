#define _CRT_SECURE_NO_WARNINGS 
#include "user.h"
#include "class_management.h" // 클래스 관리와 관련된 함수, 상수를 포함한 헤더 파일 따로 정리.

// 클래스 정보를 CSV 파일에 저장하는 함수
bool save_class_info(const char* class_title, const char* mentor_name, const char* location, const char* class_description, const char* price, const char* mode, const char* capacity, const char* image_path) {
    // 파일을 추가 모드로 열기
    FILE* file = fopen("static/classes.csv", "a");
    if (file == NULL) { // 파일이 열리지 않으면 오류 메시지 출력 후 함수 종료
        printf("클래스 정보를 저장할 수 없습니다.\n");
        return false;
    }

    // image_path에서 경로를 '/'로 구분하도록하여, 웹에서 인식 가능한 경로로 변경
    char formatted_image_path[200];
    snprintf(formatted_image_path, sizeof(formatted_image_path), "%s", image_path);
    for (int i = 0; formatted_image_path[i] != '\0'; i++) {
        if (formatted_image_path[i] == '\\') { // '\' -> '/'로 변경
            formatted_image_path[i] = '/';
        }
    }

    // CSV 파일에 클래스 정보 작성(초기 인원 0으로 설정)
    fprintf(file, "%s,%s,%s,%s,%s,%s,%s,0,%s\n", class_title, mentor_name, location, class_description, price, mode, capacity, formatted_image_path);
    fclose(file);
    return true;
}
