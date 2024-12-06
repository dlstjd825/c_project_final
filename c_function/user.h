#ifndef USER_H
#define USER_H

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_LINE_LENGTH 1024 // 파일 읽을 때 최대 글자 수
#define MAX_USERS 2048 // 최대 사용자 수. 임의로 설정함
#define MAX_COMMENT_COUNT 2048

// 사용자 정보 담은 구조체 선언
typedef struct {
    char id[20];
    char pw[10];
    char status[10];
    char role[10];
    char name[30];
    char birthday[10];
    char gender[2];
} User;

int binary_search(User* users, int left, int right, const char* id); // 정보를 빠르게 찾을 수 있도록 이진탐색 사용
int load_users(User* users, int max_users); // user.csv에서 사용자 정보 읽음
void trim_newline(char* str); // 개행문자 제거
int compare_users(const void* a, const void* b); // 사용자 정렬에 사용할 qsort를 위한 함수

#endif

