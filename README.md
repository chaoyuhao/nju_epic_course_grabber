# NJU Course Selector

## 简介

NJU Course Selector 是一个自动选课工具，基于DrissionPage框架。这个基于Python的应用程序通过自动检测并选择收藏列表中有空位的课程，简化了选课流程。

fork作者留言：传奇抢课王在`NJU Course Selector`的基础上做了简单的图形化界面，并提供了打包的release版本，提高了自动化水平以及该脚本对打开浏览器进行抢课的执念()，对非cs相关专业的同学更为友好，作者预计将维护该分支直到`25fall`。

## 主要功能

- 选课网站登录
- 自动选择收藏界面中有空余名额的课程
- 无限刷新直至选课成功

**⭐如果觉得好用的话，欢迎给个Star。**

## 安装

1. **克隆仓库**：要开始，请使用以下命令将NJU课程选择器克隆到您的本地机器：

    ```bash
    git clone https://github.com/chaoyuhao/nju_epic_course_grabber.git
    ```

2. **安装依赖项**：通过运行以下命令，安装必要的依赖项，推荐创建一个新的anaconda虚拟环境：

    ```bash
    pip install DrissionPage
    pip install requests
    pip install wxpython
    ```

## 使用

1. 运行`main.py`；
2. 等待程序进入选课部分；
3. 看到浏览器在收藏界面无限刷新时，即代表运行成功。

## 反馈

您的反馈对我们至关重要！如果您在使用NJU Course Selector时遇到任何问题，或者有任何建议或反馈，请按照以下方式与我们联系：

- **问题报告**: 如果您发现任何错误或问题，请通过GitHub的Issues功能提交问题报告。请尽可能详细地描述问题，包括如何重现该问题的步骤。
- **功能建议**: 我们欢迎任何关于新功能或改进的建议。请使用GitHub的Issues功能来提交您的建议。
- **加入开发**：如果您有更好的代码思路和功能实现，欢迎您使用GitHub的Pull Requests功能来加入程序的开发，我们感谢您的贡献。