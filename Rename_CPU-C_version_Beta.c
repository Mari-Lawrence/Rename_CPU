#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

// 注册表路径
#define CPU_REGISTRY_PATH "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0"
#define VALUE_NAME "ProcessorNameString"

// 语言支持
int isEnglish = 0;  // 0 = 中文, 1 = English

void printMenu() {
    if (isEnglish) {
        printf("\n===== Modify CPU Name Tool =====\n");
        printf("1. Modify CPU Name\n");
        printf("2. Restore Original Name\n");
        printf("3. Switch Language (切换语言)\n");
        printf("4. Exit\n");
        printf("Choose an option: ");
    } else {
        printf("\n===== 修改 CPU 名称工具 =====\n");
        printf("1. 修改 CPU 名称\n");
        printf("2. 恢复原始名称\n");
        printf("3. 切换语言 (Switch Language)\n");
        printf("4. 退出\n");
        printf("请选择操作: ");
    }
}

// 获取 CPU 名称
int getCpuName(char *buffer, DWORD size) {
    HKEY hKey;
    if (RegOpenKeyEx(HKEY_LOCAL_MACHINE, CPU_REGISTRY_PATH, 0, KEY_READ, &hKey) != ERROR_SUCCESS) {
        return 0;
    }
    if (RegQueryValueEx(hKey, VALUE_NAME, NULL, NULL, (LPBYTE)buffer, &size) != ERROR_SUCCESS) {
        RegCloseKey(hKey);
        return 0;
    }
    RegCloseKey(hKey);
    return 1;
}

// 修改 CPU 名称
int setCpuName(const char *newName) {
    HKEY hKey;
    if (RegOpenKeyEx(HKEY_LOCAL_MACHINE, CPU_REGISTRY_PATH, 0, KEY_SET_VALUE, &hKey) != ERROR_SUCCESS) {
        return 0;
    }
    if (RegSetValueEx(hKey, VALUE_NAME, 0, REG_SZ, (const BYTE*)newName, strlen(newName) + 1) != ERROR_SUCCESS) {
        RegCloseKey(hKey);
        return 0;
    }
    RegCloseKey(hKey);
    return 1;
}

// 检查是否有管理员权限
int isAdmin() {
    BOOL isAdmin = FALSE;
    SID_IDENTIFIER_AUTHORITY NtAuthority = SECURITY_NT_AUTHORITY;
    PSID AdministratorsGroup;
    if (AllocateAndInitializeSid(&NtAuthority, 2, SECURITY_BUILTIN_DOMAIN_RID, DOMAIN_ALIAS_RID_ADMINS,
                                 0, 0, 0, 0, 0, 0, &AdministratorsGroup)) {
        CheckTokenMembership(NULL, AdministratorsGroup, &isAdmin);
        FreeSid(AdministratorsGroup);
    }
    return isAdmin;
}

// 切换语言
void switchLanguage() {
    isEnglish = !isEnglish;
    printf(isEnglish ? "\nSwitched to English.\n" : "\n已切换为中文。\n");
}

int main() {
    if (!isAdmin()) {
        printf("请以管理员身份运行此程序!\n");
        system("pause");
        return 1;
    }

    char originalCpuName[256] = {0};
    char newCpuName[256] = {0};

    if (!getCpuName(originalCpuName, sizeof(originalCpuName))) {
        printf("无法获取当前 CPU 名称。\n");
        return 1;
    }

    int choice;
    while (1) {
        printMenu();
        scanf("%d", &choice);
        getchar();  // 处理回车

        switch (choice) {
            case 1:
                printf(isEnglish ? "Enter new CPU name: " : "输入新的 CPU 名称: ");
                fgets(newCpuName, sizeof(newCpuName), stdin);
                newCpuName[strcspn(newCpuName, "\n")] = 0;  // 移除换行符

                if (strlen(newCpuName) == 0) {
                    printf(isEnglish ? "Invalid input!\n" : "无效输入!\n");
                    break;
                }

                if (setCpuName(newCpuName)) {
                    printf(isEnglish ? "CPU name changed to: %s\n" : "CPU 名称已修改为: %s\n", newCpuName);
                    printf(isEnglish ? "A restart may be required.\n" : "可能需要重新启动计算机。\n");
                } else {
                    printf(isEnglish ? "Modification failed!\n" : "修改失败!\n");
                }
                break;

            case 2:
                if (setCpuName(originalCpuName)) {
                    printf(isEnglish ? "CPU name restored to: %s\n" : "CPU 名称已恢复为: %s\n", originalCpuName);
                } else {
                    printf(isEnglish ? "Restoration failed!\n" : "恢复失败!\n");
                }
                break;

            case 3:
                switchLanguage();
                break;

            case 4:
                printf(isEnglish ? "Exiting...\n" : "退出中...\n");
                return 0;

            default:
                printf(isEnglish ? "Invalid option!\n" : "无效选项!\n");
        }
    }

    return 0;
}
