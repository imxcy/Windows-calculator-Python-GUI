# 计算器

模仿 Windows 计算器的 Python GUI 程序（Windows 11 深色风格）。

点击 `=` 时不会直接计算，而是弹出确认框，选择"是"后通过 Chrome 在百度搜索该表达式。

## 功能

- 标准计算器 UI，支持键盘输入
- 运算符：`+` `−` `×` `÷` `%`
- 函数键：`1/x` `x²` `√x` `±` `⌫` `CE` `C`
- 点击 `=` → 确认后调用浏览器搜索表达式

## 运行

```bash
python calculator.py
```

**依赖：** Python 3.8+，仅需标准库（`tkinter`）。

**浏览器路径：** 默认 `C:\Program Files\Google\Chrome\Application\chrome.exe`，如路径不同请修改脚本中的 `BROWSER_PATH`。

## 截图

<img width="382" height="612" alt="acb5ce3f-2652-4893-8129-368915bbbab0" src="https://github.com/user-attachments/assets/78968931-05fd-427c-b0b4-377100160c57" />
