# Puzodyssey Official Site

当前项目是一个纯静态单页官网，主页面已经换成 PuzOdyssey 拼图板产品展示页。

## 当前包含内容

- `index.html`：当前主页面，已融入产品主图、角度调节、配件、旋转与尺寸详情图
- `index-minimal.html`：更简约的首页方案
- `styles.css`：页面视觉样式与响应式布局
- `styles-minimal.css`：简约版首页样式
- `script.js`：移动端菜单、滚动出现动画与页脚年份

## 图片目录建议

- `assets/product/`：产品图片
- `assets/factory/`：工厂图片
- `assets/founder/`：创始人介绍图片

当前主页面使用的产品图片已放在 `assets/product/`，文件名为 `puzodyssey-*.jpg`。

## 当前两个首页方向

- `index.html`：当前产品展示版本
- `index-minimal.html`：旧的简约方向，暂未接入本次产品详情图

## 如何预览

直接在浏览器里打开 `index.html` 即可。

如果你希望本地起一个简单服务，也可以在当前目录运行：

```bash
python3 -m http.server 8000
```

然后访问 `http://localhost:8000`。

## 上线前建议替换

- 联系方式中的邮箱、微信、销售渠道
- 按钮中的询盘链接、表单地址或购买链接
- 后续可补充的工厂、创始人或真实使用场景图片
