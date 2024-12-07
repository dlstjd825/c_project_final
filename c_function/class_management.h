//임수빈
#ifndef CLASS_MANAGEMENT_H
#define CLASS_MANAGEMENT_H

#define MAX_LINE_LENGTH 1024

// 함수 선언에 __declspec(dllexport) 추가
__declspec(dllexport) bool save_class_info(const char* class_title, const char* mentor_name, const char* location, const char* class_description, const char* price, const char* mode, const char* capacity, const char* image_path);
__declspec(dllexport) bool load_classes(const char* filename, char classes[][MAX_LINE_LENGTH], int* count);
__declspec(dllexport) bool is_user_mentor(const char* user_id);
__declspec(dllexport) bool load_class_details(const char* class_title, char* class_details);
__declspec(dllexport) bool apply_class_in_c(const char* class_title);

#endif
