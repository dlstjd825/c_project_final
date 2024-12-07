//임수빈
#define _CRT_SECURE_NO_WARNINGS
#include "user.h"
#include "class_management.h" // 클래스 관리와 관련된 함수, 상수를 포함한 헤더 파일 따로 정리.

// 특정 클래스를 신청하고 신청 인원을 업데이트하는 함수
__declspec(dllexport) bool apply_class_in_c(const char* class_title) {
    // csv 파일을 읽기 및 쓰기 모드로 열기
    FILE* file = fopen("static/classes.csv", "r+");
    if (file == NULL) { // 파일이 열리지 않으면 오류 메시지 출력 후 함수 종료
        printf("클래스 정보를 저장한 파일을 열 수 없습니다.\n");
        return false;
    }

    char line[MAX_LINE_LENGTH];
    char updated_content[10000] = ""; // 수정된 파일 내용을 저장할 문자열
    bool found_class = false; // 클래스가 발견되었는지 여부를 나타냄

    // 파일에서 한 줄씩 읽기
    while (fgets(line, sizeof(line), file)) {
        // 각 클래스 정보를 저장할 변수들 선언
        char current_title[100], mentor_name[100], location[100], description[500];
        char price[20], mode[20], capacity[10], current_applicants[10], image_path[200];

        // 쉼표로 구분된 각 정보를 읽어와 변수에 저장
        if (sscanf(line, "%99[^,],%99[^,],%99[^,],%499[^,],%19[^,],%19[^,],%9[^,],%9[^,],%199[^\n]",
            current_title, mentor_name, location, description, price, mode, capacity, current_applicants, image_path) == 9) {

            // 찾고 있는 클래스 제목과 일치하는지 확인
            if (strcmp(class_title, current_title) == 0) {
                int current_applicants_num = atoi(current_applicants); // 현재 신청 인원을 정수로 변환
                int capacity_num = atoi(capacity); // 최대 수강 인원을 정수로 변환

                // 신청 인원이 최대 수강 인원을 초과하는지 확인
                if (current_applicants_num >= capacity_num) {
                    fclose(file);
                    return false;
                }

                // 신청 인원 +1
                current_applicants_num++;
                snprintf(current_applicants, sizeof(current_applicants), "%d", current_applicants_num); // 증가된 인원 저장
                found_class = true; // 클래스가 발견되었음을 표시
            }

            // 현재 줄을 수정된 형태로 저장
            char updated_line[MAX_LINE_LENGTH];
            snprintf(updated_line, sizeof(updated_line), "%s,%s,%s,%s,%s,%s,%s,%s,%s\n",
                current_title, mentor_name, location, description, price, mode, capacity, current_applicants, image_path);
            strcat(updated_content, updated_line); // 수정된 줄을 전체 업데이트된 내용에 추가
        }
    }

    fclose(file);

    // 업데이트된 내용을 파일에 다시 작성
    if (found_class) {
        file = fopen("static/classes.csv", "w"); // 파일을 쓰기 모드로 다시 열기
        if (file == NULL) { // 파일이 열리지 않으면 오류 메시지 출력 후 함수 종료
            printf("클래스 정보를 저장한 파일을 열 수 없습니다.\n");
            return false;
        }
        fputs(updated_content, file); // 수정된 내용 파일에 작성
        fclose(file);
    }

    return found_class; // 클래스를 찾았으면 true, 찾지 못했으면 false 반환
}
