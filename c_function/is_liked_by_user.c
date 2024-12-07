//���翬,���μ�
#define _CRT_SECURE_NO_WARNINGS
#include "user.h"

// Ư�� ����ڰ� Ư�� �̹����� ���ƿ� �ߴ��� Ȯ���ϴ� �Լ�
__declspec(dllexport) bool is_liked_by_user(const char* user_id, const char* image_path) {
    // ����� ������ �ε�
    User users[MAX_USERS];
    int user_count = load_users(users, MAX_USERS);

    if (user_count == 0) {
        printf("����� �����͸� �ҷ����� ���߽��ϴ�.\n");
        return false;  // �����͸� �ε����� ���ϸ� false ��ȯ
    }

    // ����� �迭 ����
    qsort(users, user_count, sizeof(User), compare_users);

    // user_id�� ���� Ž������ ã��
    int user_index = binary_search(users, 0, user_count - 1, user_id);

    if (user_index == -1) {
        printf("����ڸ� ã�� �� �����ϴ�: %s\n", user_id);
        return false;  // ����� ID�� �������� ������ false ��ȯ
    }

    // likes.csv ���� ����
    FILE* file = fopen("static/likes.csv", "r");
    if (file == NULL) {
        perror("Failed to open likes.csv");
        return false;  // ���� ���� ���� �� false ��ȯ
    }

    char line[MAX_LINE_LENGTH];
    char csv_user_id[50];
    char csv_image_path[255];

    // likes.csv���� �� �پ� �о�� user_id�� image_path Ȯ��
    while (fgets(line, sizeof(line), file)) {
        if (sscanf(line, "%49[^,],%254[^,],%*s", csv_user_id, csv_image_path) == 2) {
            trim_newline(csv_user_id);
            trim_newline(csv_image_path);

            if (strcmp(csv_user_id, users[user_index].id) == 0 && strcmp(csv_image_path, image_path) == 0) {
                fclose(file);
                return true;  // ���ƿ� �����Ͱ� �߰ߵǸ� true ��ȯ
            }
        }
    }

    fclose(file);  // ���� �ݱ�
    return false;  // ���ƿ� �����Ͱ� ������ false ��ȯ
}
