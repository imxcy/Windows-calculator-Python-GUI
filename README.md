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

<img width="1854" height="902" alt="image" src="https://github.com/user-attachments/assets/862cac0c-c377-4ade-8f4f-f234c9560139" />
