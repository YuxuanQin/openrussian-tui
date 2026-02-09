# OpenRussian TUI
这是 [Open Russian](https://openrussian.org) 的 TUI 前端。

使用本程序必须联网：因为程序发送查词请求后，必须等待网站发回包含单词信息的 `.json` 才能输出信息。

This is a tui "program" for the [Open Russian Dictionary](https://openrussian.org). You can use it to search meanings and example sentences of Russian words.

There is no magic in this program: it just throw a request to that website and receive a `.json` file, then parse it. So to use it, a decent network should be accessible.

## 下载 / Installation
```
pip install openrussian-tui
```

## 如何使用 / How to use
+ 克隆本仓库；
+ 确保本机已有 `textual` 库，如果没有，请遵[官方指导](https://textual.textualize.io/getting_started/#installation)下载；
+ 执行 `python openrussian.py`，就可以查词了！

+ Clone this repo.
+ Make sure you have installed the famous python tui library `textual` already, if not, please follow the [instruction](https://textual.textualize.io/getting_started/#installation) on their official site.
+ Just run `python openrussian.py` and start learning Russian!

## 功能 / Functions
目前可以看到俄语单词的释义和例句。

You can view the translations, exmaples sentences of a russian word.

## 这软件怎么来的 / How did I made this program
大部分代码是从 `textual` [官方仓库](https://github.com/textualize/textual/)中的 `/examples/dictionary.py` 和相应 `.tcss` 里偷的，所以如果你想添加更多网站的支持，请务必研究一下这两个文件。

The main part of these codes are stolen from `/examples/dictionary.py` and the adjoint `.tcss` file in the `textual` [repo](https://github.com/textualize/textual/), so if you want to add other online dictionary, you'd better check the official guide of `textual`.

## 协议 / License
想做什么都可以，干了坏事别找我 😆。

Do anything you want to these codes, just promise that if something bad happened because of your forks, do not charge me 😆.
