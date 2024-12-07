//���翬,���μ�
#include "user.h"

// ���ε� ��������� Ȯ���ϴ� �Լ�
__declspec(dllexport) int is_user_valid(const char* user_id) {
    User users[MAX_USERS];  // ����� �����͸� ������ �迭
    int user_count = load_users(users, MAX_USERS);  // ����� �����͸� �ε�

    if (user_count == 0) {
        printf("����� �����͸� �ҷ����� ���߽��ϴ�.\n");
        return 0;  // �����Ͱ� ������ ����
    }

    // ����� �迭�� ID �������� ����
    qsort(users, user_count, sizeof(User), compare_users);

    // ���� Ž���� ���� user_id�� ã��
    int index = binary_search(users, 0, user_count - 1, user_id);
    if (index != -1 && strcmp(users[index].status, "approved") == 0) {
        return 1;  // ���ε� �����
    }

    return 0;  // ���ε��� �ʰų� ����ڰ� �������� ����
}
