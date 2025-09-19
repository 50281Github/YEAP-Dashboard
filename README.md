# YEAP Dashboard - Youth Employment Analysis Platform

## 📊 项目简介

YEAP Dashboard 是一个基于 Streamlit 的青年就业分析平台，用于分析和可视化 2024 年青年就业相关数据。

## 🚀 功能特性

- **Q3-Q5 分析**: 输出在实施框架集群中的分布分析
- **Q6-Q11 分析**: 青年就业输出的深度分析，包括频率分析和统计数据
- **Q8-Q9 分析**: 相关问题的专项分析
- **交互式可视化**: 支持多种图表类型（饼图、柱状图、水平柱状图）
- **区域过滤**: 按组织单位筛选数据
- **响应式设计**: 适配不同屏幕尺寸

## 🛠️ 技术栈

- **前端框架**: Streamlit
- **数据处理**: Pandas
- **数据可视化**: Plotly
- **语言**: Python 3.13+

## 📁 项目结构

```
YEAP-9-19/
├── streamlit/                 # Streamlit 应用文件
│   ├── streamlit_app.py      # 主应用入口
│   ├── st_q345_dashboard.py  # Q3-Q5 仪表盘
│   ├── st_q6q7q10q11_dashboard.py # Q6-Q11 仪表盘
│   ├── st_q8q9_dashboard.py  # Q8-Q9 仪表盘
│   └── requirements.txt      # 依赖包列表
├── orignaldata/              # 原始数据文件
├── result/                   # 分析结果文件
└── README.md                 # 项目说明
```

## 🚀 本地运行

1. 克隆仓库
```bash
git clone [仓库URL]
cd YEAP-9-19
```

2. 安装依赖
```bash
pip install -r streamlit/requirements.txt
```

3. 运行应用
```bash
streamlit run streamlit/streamlit_app.py
```

4. 在浏览器中访问 `http://localhost:8501`

## 🌐 在线访问

应用已部署到 Streamlit Community Cloud，可通过以下链接访问：
[部署链接将在部署完成后更新]

## 📈 数据说明

- 数据来源：2024年青年就业调研
- 数据格式：CSV文件
- 数据更新：根据调研进度定期更新

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。

## 📄 许可证

本项目采用 MIT 许可证。

---

**开发团队**: YEAP 项目组  
**最后更新**: 2024年12月