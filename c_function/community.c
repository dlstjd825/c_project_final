//우재연
#include "user.h"

__declspec(dllexport) void save_community_post(const char* title, const char* content, const char* image_path) {
    if (title == NULL || content == NULL || image_path == NULL) {
        fprintf(stderr, "Error: Invalid input data.\n");
        return;
    }

    const char* filepath = "static/community_posts.csv";  // 파일 경로
    FILE* file = fopen(filepath, "a");
    if (file == NULL) {
        fprintf(stderr, "Error: Unable to open file %s for writing.\n", filepath);
        return;
    }

    fprintf(file, "%s,%s,%s\n", title, content, image_path);
    fclose(file);
}