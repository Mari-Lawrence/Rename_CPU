import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class CPURenameTool {
    private static final String CPU_REGISTRY_PATH = "HKEY_LOCAL_MACHINE\\HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0";
    private static final String VALUE_NAME = "ProcessorNameString";

    private JFrame frame;
    private JTextField cpuNameField;
    private JLabel statusLabel;
    private String originalCpuName;
    private boolean isEnglish = false;

    public CPURenameTool() {
        // 获取原始 CPU 名称
        originalCpuName = getRegistryValue();

        // 创建窗口
        frame = new JFrame(isEnglish ? "Modify CPU Name Tool" : "修改 CPU 名称工具");
        frame.setSize(500, 250);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new GridLayout(5, 1));

        // 输入框
        JPanel inputPanel = new JPanel();
        inputPanel.add(new JLabel(isEnglish ? "Enter new CPU name:" : "输入新的 CPU 名称:"));
        cpuNameField = new JTextField(25);
        inputPanel.add(cpuNameField);
        frame.add(inputPanel);

        // 按钮
        JPanel buttonPanel = new JPanel();
        JButton modifyButton = new JButton(isEnglish ? "Modify Name" : "修改名称");
        JButton restoreButton = new JButton(isEnglish ? "Restore Original" : "恢复原始名称");
        JButton switchLangButton = new JButton(isEnglish ? "Switch to Chinese" : "切换到英文");
        JButton themeButton = new JButton(isEnglish ? "Switch Theme" : "切换主题");

        buttonPanel.add(modifyButton);
        buttonPanel.add(restoreButton);
        buttonPanel.add(switchLangButton);
        buttonPanel.add(themeButton);
        frame.add(buttonPanel);

        // 状态栏
        statusLabel = new JLabel(isEnglish ? "Current CPU Name: " + originalCpuName : "当前 CPU 名称: " + originalCpuName, JLabel.CENTER);
        frame.add(statusLabel);

        // 事件监听
        modifyButton.addActionListener(e -> modifyCpuName(cpuNameField.getText()));
        restoreButton.addActionListener(e -> restoreCpuName());
        switchLangButton.addActionListener(e -> switchLanguage());
        themeButton.addActionListener(e -> switchTheme());

        frame.setVisible(true);
    }

    /**
     * 获取注册表中的 CPU 名称
     */
    private String getRegistryValue() {
        try {
            Process process = Runtime.getRuntime().exec("reg query \"" + CPU_REGISTRY_PATH + "\" /v " + VALUE_NAME);
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.contains(VALUE_NAME)) {
                    return line.split("    ")[line.split("    ").length - 1].trim();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return "Unknown";
    }

    /**
     * 修改 CPU 名称
     */
    private void modifyCpuName(String newName) {
        if (newName.isEmpty() || !newName.matches("^[ A-Za-z0-9()-]+$")) {
            JOptionPane.showMessageDialog(frame, isEnglish ? "Invalid CPU name!" : "无效的 CPU 名称！", "Error", JOptionPane.ERROR_MESSAGE);
            return;
        }
        try {
            Process process = Runtime.getRuntime().exec("reg add \"" + CPU_REGISTRY_PATH + "\" /v " + VALUE_NAME + " /t REG_SZ /d \"" + newName + "\" /f");
            process.waitFor();
            statusLabel.setText(isEnglish ? "CPU name changed to: " + newName : "CPU 名称已修改为: " + newName);
            JOptionPane.showMessageDialog(frame, isEnglish ? "Modification successful! Restart required." : "修改成功！可能需要重启计算机。", "Success", JOptionPane.INFORMATION_MESSAGE);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(frame, isEnglish ? "Modification failed!" : "修改失败！", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    /**
     * 恢复 CPU 名称
     */
    private void restoreCpuName() {
        modifyCpuName(originalCpuName);
    }

    /**
     * 切换语言
     */
    private void switchLanguage() {
        isEnglish = !isEnglish;
        frame.setTitle(isEnglish ? "Modify CPU Name Tool" : "修改 CPU 名称工具");
        statusLabel.setText(isEnglish ? "Current CPU Name: " + originalCpuName : "当前 CPU 名称: " + originalCpuName);
        frame.getContentPane().removeAll();
        new CPURenameTool();
        frame.dispose();
    }

    /**
     * 切换主题
     */
    private void switchTheme() {
        UIManager.put("Panel.background", UIManager.getColor("Panel.background").equals(Color.DARK_GRAY) ? Color.WHITE : Color.DARK_GRAY);
        UIManager.put("Label.foreground", UIManager.getColor("Label.foreground").equals(Color.WHITE) ? Color.BLACK : Color.WHITE);
        SwingUtilities.updateComponentTreeUI(frame);
    }

    public static void main(String[] args) {
        // 检测是否以管理员运行
        if (!isRunningAsAdmin()) {
            JOptionPane.showMessageDialog(null, "请以管理员身份运行此程序！", "权限错误", JOptionPane.ERROR_MESSAGE);
            System.exit(0);
        }
        new CPURenameTool();
    }

    /**
     * 检测 Java 是否以管理员权限运行
     */
    private static boolean isRunningAsAdmin() {
        try {
            Process process = Runtime.getRuntime().exec("net session");
            process.waitFor();
            return process.exitValue() == 0;
        } catch (IOException | InterruptedException e) {
            return false;
        }
    }
}
