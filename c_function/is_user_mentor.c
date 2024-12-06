#include "user.h"

// ����ڰ� �������� ���θ� Ȯ���ϴ� �Լ�
__declspec(dllexport) bool is_user_mentor(const char* user_id) {
    User users[MAX_USERS];  // ����� �����͸� ������ �迭
    int user_count = load_users(users, MAX_USERS);  // ����� �����͸� �ε�

    if (user_count == 0) {
        printf("����� �����͸� �ҷ����� ���߽��ϴ�.\n");
        return false;  // �����Ͱ� ������ false ��ȯ
    }

    // ����� �迭�� ID �������� ����
    qsort(users, user_count, sizeof(User), compare_users);

    // ���� Ž���� ���� user_id�� ã��
    int index = binary_search(users, 0, user_count - 1, user_id);
    if (index != -1 && strcmp(users[index].role, "mentor") == 0) {
        return true;  // ����ڰ� mentor ������ ��� true ��ȯ
    }

    return false;  // ����ڰ� mentor�� �ƴϰų� �������� �ʴ� ��� false ��ȯ
}
