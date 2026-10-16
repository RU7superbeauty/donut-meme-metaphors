# donut-meme-metaphors

为 **Donut / D0** 生成「World 式」隐喻 meme 的创意库 + prompt 生成器。

参考对象：[World (@world_xyz)](https://x.com/world_xyz) 的视觉打法 ——  
**经典源典（名画 / 电影 / 金融史 / 体育史）+ 只改一处品牌物 + 极短文案。**

本仓库不直接吐出侵权原图，也不承诺 1:1 复刻受版权保护的作品。  
它产出的是：**可解码的创意 brief + 可丢进图像模型的 prompt**，让人一眼认出源典母题，再半秒发现被 Donut「劫持」。

---

## 配方（硬规则）

```
经典源典（可指名）
  + 只插入 1 个 Donut 品牌物（糖霜环 / Glazy / 品牌渐变环）
  + ≤ 4 个词的英文或中文短句（可选日期）
  = Donut metaphor meme
```

| 做 | 不做 |
|---|---|
| 一图一事，源典可点名 | 堆 UI / 功能列表 / 产品截图 |
| 品牌物独占彩色 | 紫粉渐变铺满、赛博霓虹墙 |
| 隐喻对齐真实产品能力 | 稳赚 / 翻倍 / 躺赚 / 颠覆全球 |
| 文案像黑话或谜语 | 长 headline 压画面 |

详细品牌插入规范见 [`brand/INSERT.md`](brand/INSERT.md)，红线见 [`brand/RULES.md`](brand/RULES.md)。

---

## 快速开始

```bash
# 需要 Python 3.10+
cd tools
python generate_prompt.py list
python generate_prompt.py show mona-lisa
python generate_prompt.py build mona-lisa --metaphor just-say-it --lang en
python generate_prompt.py build ali-liston --metaphor conviction --lang zh
python generate_prompt.py random --count 5
python generate_prompt.py export recipes/batch.json --all
```

输出是一段 **Creative Brief + Image Prompt**，可直接贴进 Midjourney / Flux / Higgsfield / nano-banana 等。

---

## 仓库结构

```
brand/           品牌插入物 + 红线
catalog/         源典库 + Donut 隐喻映射（JSON）
prompts/         prompt 模板
examples/        World 解码笔记 + Donut brief 样例
recipes/         可直接跑的批次配方
tools/           CLI 生成器
```

---

## 隐喻轴（Donut 版）

| 产品能力 | 视觉隐喻 | 示例源典 |
|---|---|---|
| 一句话下单 / just say it | 话语成真、打字即法术 | 《创世纪》手势、打字机、神谕 |
| Agent 代劳 | 管家 / 自动驾驶 / 替身出手 | 管家肖像、自动驾驶公路片 |
| Whale alert | 巨鲸现身 | 飞鲸超现实、Ali 碾压图 |
| Smart money / conviction | 胜出、信念 | Ali vs Liston、拳台定格 |
| 多市场 / 全球盘口 | Around the world | Daft Punk 母题、护照、地球仪→甜甜圈环 |
| 预测 / 概率 | 水晶球、环即盘口 | 蒙娜丽莎托环、流水线造环 |
| 投机与狂欢 | 华尔街 excess | 《华尔街之狼》构图母题 |
| 稀缺与 hype | 文化资本 | Supreme 式角标（DONUT / D0）|

完整映射：[`catalog/metaphors.json`](catalog/metaphors.json)  
源典库：[`catalog/sources.json`](catalog/sources.json)

---

## 和 World 的差异（刻意）

| | World | Donut |
|---|---|---|
| 品牌物 | 虹彩网格球 | **糖霜甜甜圈环** / Glazy / 品牌渐变环 |
| 色 | 青粉金油膜 | `#9997FF → #C25C9A → #DD8B57` 渐变，其余灰阶或低饱和 |
| 产品 | 预测市场本身 | **Telegram 上的交易 agent（D0）** |
| 文案 | conviction / rumors / watching | just say it / type it / whale / placed |

World 解码笔记：[`examples/world_xyz_method.md`](examples/world_xyz_method.md)

---

## 合规

- 源典只作 **风格 / 构图 / 母题** 参考，生成时用描述性语言，避免要求「exact reproduction of [受版权作品]」。
- 名人肖像、商标（Supreme 等）只作文化母题说明；对外发布前请法务 / 设计复核。
- 禁止收益承诺文案（见 `brand/RULES.md`）。

---

## License

MIT（代码与 JSON 配方）。源典原作版权归原作者所有。
