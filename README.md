# PDFtoPNG

这是一个简单的 Web 应用程序，可以将上传的 PDF 文件转换为图像，并提供下载 ZIP 文件的功能。

## 功能
- 上传 PDF 文件
- 将 PDF 页面转换为 PNG 图像
- 下载所有图像的 ZIP 文件

## 技术栈
- **Python**: 后端编程语言
- **Flask**: Python Web 框架
- **PyMuPDF (fitz)**: PDF 处理库
- **HTML/CSS/JavaScript**: 前端技术
- **Git**: 版本控制系统

## 快速开始

### 克隆仓库
```bash
git clone https://github.com/yourusername/pdf-converter.git
cd pdf-converter
```

### 运行应用程序
```bash
python app.py
```
应用程序将在本地运行，你可以通过浏览器访问 http://127.0.0.1:5000/ 来查看。

## 使用说明
1. 访问首页 http://127.0.0.1:5000/
2. 选择你要上传的 PDF 文件。
3. 点击 "上传文件" 按钮。
4. 查看转换后的图像，并下载 ZIP 文件。

## 目录结构
```
pdf-converter/
├── app.py
├── templates/
├── uploads/
├── output/
├── zips/
└── README.md
```

## 贡献
欢迎贡献！如果你发现任何问题或有改进建议，请提交 issue 或 pull request。

## 许可证
本项目采用 MIT License 许可。

## 联系方式
如有任何问题或建议，请联系 xiao_maikuai@163.com。
