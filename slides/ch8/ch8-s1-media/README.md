# 8.1 自旋动画素材

`gyro-both.mp4` 是经典陀螺同时沿轨道运动并自转的 8 秒视频。它用于说明两种角动量的区别，不是电子结构模型。

课件第 7 页已嵌入循环 GIF，下载 PPTX 后不需要额外下载视频。

从仓库根目录重新生成 GIF：

```sh
python -m pip install imageio imageio-ffmpeg Pillow
python slides/ch8/ch8-s1.make_gif.py
```

生成文件为此目录下的 `gyro-both.gif`，脚本不会自动修改 PPTX。

在线查看器第 7 页使用整页 MP4，保留幻灯片的正文与动画位置。安装 Pillow 和 FFmpeg 后，从仓库根目录重建：

```sh
python tools/render_animated_slide.py slides/ch8/ch8-s1.pptx 7 docs/viewer/slides/ch8/ch8-s1/page-7.png
```

该脚本从 PPTX 提取实际嵌入的 GIF 及位置，覆盖到新版页面截图上，不依赖此目录的源视频。普通页使用 PNG；动画页由 `docs/viewer/manifest.json` 中的 `_media` 配置指定，缩略图仍使用 PNG。
