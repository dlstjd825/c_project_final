#define _CRT_SECURE_NO_WARNINGS
#include "user.h"
#include <locale.h>




// ��� ���� �Լ� ����
__declspec(dllexport) bool delete_comment(const char* user_id, const char* comment_id, const char* post_id) {
    setlocale(LC_ALL, "en_US.UTF-8");

    FILE* file = fopen("static/comments.csv", "r");
    if (file == NULL) {
        perror("Failed to open comments.csv");
        return false;
    }

    // �ӽ� ���� ����
    FILE* temp_file = fopen("static/comments_temp.csv", "w");
    if (temp_file == NULL) {
        perror("Failed to create temp file");
        fclose(file);
        return false;
    }

    char line[MAX_LINE_LENGTH];
    bool deleted = false;

    // CSV ���� �б� �� �ӽ� ���Ͽ� ����
    while (fgets(line, sizeof(line), file)) {
        char current_user_id[20], comment_text[1024], current_post_id[1024], timestamp[20];
        char current_comment_id[MAX_LINE_LENGTH];

        if (sscanf(line, "%19[^,],%1023[^,],%1023[^,],%19s",
            current_user_id, comment_text, current_post_id, timestamp) == 4) {
            snprintf(current_comment_id, sizeof(current_comment_id), "%s-%s", comment_text, timestamp);

            // ���� �� ���� ����
            trim_newline(current_user_id);
            trim_newline(current_comment_id);
            trim_newline(current_post_id);

            // �� ���� �α� �߰�
            if (strcmp(user_id, current_user_id) != 0) {
                printf("User ID mismatch: input=%s, csv=%s\n", user_id, current_user_id);
            }
            if (strcmp(comment_id, current_comment_id) != 0) {
                printf("Comment ID mismatch: input=%s, csv=%s\n", comment_id, current_comment_id);
            }
            if (strcmp(post_id, current_post_id) != 0) {
                printf("Post ID mismatch: input=%s, csv=%s\n", post_id, current_post_id);
            }

            // ��
            if (strcmp(user_id, current_user_id) == 0 &&
                strcmp(comment_id, current_comment_id) == 0 &&
                strcmp(post_id, current_post_id) == 0) {
                deleted = true;
                continue; // ���� ����� ���͸�
            }

            // ���� ����� �ƴ� �����͸� �ӽ� ���Ͽ� ���
            fprintf(temp_file, "%s,%s,%s,%s\n", current_user_id, comment_text, current_post_id, timestamp);
        }
    }

    fclose(file);
    fclose(temp_file);

    // ������ ������ ������ �ӽ� ���� ����
    if (!deleted) {
        printf("Comment not found or user mismatch.\n");
        remove("static/comments_temp.csv");
        return false;
    }

    // �۾� ���� �� ���� ������ �ӽ� ���Ϸ� ��ü
    if (remove("static/comments.csv") != 0) {
        perror("Failed to delete original comments.csv");
        return false;
    }

    if (rename("static/comments_temp.csv", "static/comments.csv") != 0) {
        perror("Failed to rename temp file to comments.csv");
        return false;
    }

    printf("Successfully deleted comment.\n");
    return true;
}
