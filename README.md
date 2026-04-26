# Puzodyssey Official Site

当前项目是一个纯静态官网，主页面已经换成 PuzOdyssey 拼图板产品展示页。

## 当前包含内容

- `index.html`：当前主页面，已融入产品主图、角度调节、配件、旋转与尺寸详情图
- `index-minimal.html`：更简约的首页方案
- `styles.css`：页面视觉样式与响应式布局
- `styles-minimal.css`：简约版首页样式
- `script.js`：移动端菜单、滚动出现动画与页脚年份
- `robots.txt`：搜索引擎抓取规则，指向正式 sitemap
- `sitemap.xml`：正式站点地图，使用 `https://puzodyssey.com/` 作为 canonical 域名
- `CNAME`：自定义域名配置，当前为 `puzodyssey.com`

## 图片目录建议

- `assets/product/`：产品图片
- `assets/factory/`：工厂图片
- `assets/founder/`：创始人介绍图片

当前主页面使用的产品图片已放在 `assets/product/`，文件名为 `puzodyssey-*.jpg`。

## 当前两个首页方向

- `index.html`：当前产品展示版本
- `index-minimal.html`：旧的简约方向，暂未接入本次产品详情图

## 本地预览

直接在浏览器里打开 `index.html` 即可。

如果你希望本地起一个简单服务，也可以在当前目录运行：

```bash
python3 -m http.server 8000
```

然后访问 `http://localhost:8000`。

## 生产环境上线

当前线上站点由 Netlify 提供服务，正式域名是：

```text
https://puzodyssey.com/
```

实际发布链路是：

```text
local changes -> GitHub main branch -> Netlify automatic deploy -> puzodyssey.com
```

上线步骤：

1. 在本地完成并验证官网改动。
2. 只提交需要发布的官网文件，避免把无关临时文件带进 commit。
3. 推送到 GitHub `main` 分支。
4. 等待 Netlify 自动部署。
5. 验证以下线上地址：

```text
https://puzodyssey.com/
https://puzodyssey.com/robots.txt
https://puzodyssey.com/sitemap.xml
```

Google Search Console 通常不需要重建配置。只要域名仍然是 `puzodyssey.com`、URL 结构没有变化、canonical 仍指向 `https://puzodyssey.com/`，上线后只需要：

- 对首页执行一次 URL Inspection / Request Indexing
- 重新提交 `https://puzodyssey.com/sitemap.xml`

## 上线前建议替换

- 联系方式中的邮箱、微信、销售渠道
- 按钮中的询盘链接、表单地址或购买链接
- 后续可补充的工厂、创始人或真实使用场景图片
