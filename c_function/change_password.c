//Á¤¼¼Àº
#define _CRT_SECURE_NO_WARNINGS
#include "user.h"

__declspec(dllexport) bool change_password(const char* id, const char* old_password, const char* new_password) {
    User* users = (User*)malloc(MAX_USERS * sizeof(User));
    if (users == NULL) {
        printf("Memory allocation failed.\n");
        return false;
    }

    int num_users = load_users(users, MAX_USERS);

    if (num_users == 0) {
        printf("No users loaded.\n");
        free(users);
        return false;
    }

    qsort(users, num_users, sizeof(User), compare_users);

    int index = binary_search(users, 0, num_users - 1, id);
    if (index == -1) {
        printf("User not found.\n");
        free(users);
        return false;
    }

    if (strcmp(users[index].pw, old_password) != 0) {
        printf("Old password does not match.\n");
        free(users);
        return false;
    }

    strcpy(users[index].pw, new_password);

    FILE* csv_file = fopen("static/user.csv", "w");
    if (!csv_file) {
        perror("Failed to open CSV file for writing");
        free(users);
        return false;
    }

    for (int i = 0; i < num_users; i++) {
        fprintf(csv_file, "%s,%s,%s,%s,%s,%s,%s\n",
            users[i].id, users[i].pw, users[i].status,
            users[i].role, users[i].name, users[i].birthday, users[i].gender);
    }

    fclose(csv_file);
    free(users);
    return true;
}
