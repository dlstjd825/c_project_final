//정인성
// 회원가입 요청
#include "user.h"

__declspec(dllexport) bool signup_request(const char* ID, const char* PW, const char* status, const char* role, const char* name, const char* birthday, const char* gender) {
    char txt_filename[256];
    snprintf(txt_filename, sizeof(txt_filename), "static/users/%s_info.txt", ID);

    // txt파일 작성 : 관리자가 사용자 정보 확인용도
    FILE* txt_file = fopen(txt_filename, "w");
    if (txt_file == NULL) {
        printf("Failed to create user info file\n");
        return false;
    }

    // 사용자 정보를 텍스트 파일에 작성
    fprintf(txt_file, "ID: %s\nPW: %s\nStatus: %s\nRole: %s\nName: %s\nBirthday: %s\nGender: %s\n",
        ID, PW, status, role, name, birthday, gender);
    fclose(txt_file);

    // user.csv 파일에 사용자 정보 추가
    FILE* csv_file = fopen("static/user.csv", "a+");
    if (csv_file == NULL) {
        perror("Failed to open CSV file");
        return false;
    }

    // user.csv에서 새로운 정보가 맨 마지막에 추가될 수 있도록 함
    fseek(csv_file, 0, SEEK_END);

    // CSV 형식으로 사용자 정보를 추가
    fprintf(csv_file, "%s,%s,%s,%s,%s,%s,%s\n", ID, PW, status, role, name, birthday, gender);
    fclose(csv_file);

    return true;
}


