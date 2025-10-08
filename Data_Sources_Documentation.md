# YEAP 数据分析仪表板说明书 
# YEAP Data Analysis Dashboard Guide

## 📋 项目概览 Project Overview

YEAP (Youth Employment Action Programme) 数据分析仪表板是一个基于 Streamlit 的交互式数据可视化平台，用于分析青年就业行动计划的调查数据。该仪表板包含五个主要页面，提供从概览到专项分析的全方位数据洞察。

### 页面结构 Page Structure
1. **🏠 Overview** - 调查概览页面
2. **📊 Outputs Count Statistics** - 产出统计页面
3. **📚 Knowledge Development & Dissemination** - 知识发展与传播分析
4. **🔧 Technical Assistance** - 技术援助分析
5. **🎓 Capacity Development** - 能力发展分析
6. **🤝 Advocacy & Partnerships** - 倡导与合作伙伴关系分析

## 🏠 Overview 页面 (调查概览)

### 页面功能 Page Functions
- **综合概览**: 提供调查响应和关键洞察的全面概述
- **Q2 数据展示**: 显示核心调查问题的饼图分析
- **Q3-Q5 汇总表**: 展示实施框架、政策领域和目标群体的汇总数据

### 数据文件位置 Data File Locations
- **Q2 数据**: `orignaldata/PART1_base_dataQ2-5.csv`
- **Q3-Q5 数据**: 
  - `orignaldata/PART2_base_dataQ3.csv`
  - `orignaldata/PART2_base_dataQ4.csv`
  - `orignaldata/PART2_base_dataQ5.csv`

### 显示内容 Display Content
1. **统一头部**: 蓝色背景容器，包含 ILO Logo 和年份感知标题
2. **Q2 饼图**: 基于 PART1 数据的核心问题可视化
3. **Q3-Q5 汇总表**: 三个专项分析的数据汇总表格

---

## 📊 General Survey Analysis 页面 (通用调查分析)

### 页面功能 Page Functions
- **多问题分析**: 支持 Q1-Q5 所有问题的可视化分析
- **多图表类型**: 自动选择最适合的图表类型（饼图、条形图、横向条形图）
- **交互式功能**: 提供问题选择和图表类型切换功能

### 数据文件位置 Data File Location
- **主数据文件**: `orignaldata/PART1_base_dataQ2-5.csv`
- **文件格式**: CSV 文件，包含三列：`question`(问题), `option`(选项), `count`(数量)

### 图表制作方式 Chart Creation Methods

#### 自动图表选择逻辑 Auto Chart Selection Logic
- **饼图**: 当选项 ≤ 5个时使用
- **竖条图**: 当选项 > 5个或标签文字较长时使用
- **横条图**: 当选项 > 10个或标签文字 > 20个字符时使用

#### 数据处理规则 Data Processing Rules
- **数据映射**: 
  - `question`列 → 图表标题
  - `option`列 → 图表分类标签
  - `count`列 → 图表数值
- **数据过滤**: 
  - Q4和Q5问题：过滤掉少于5%的选项和"其他"选项
  - Q2问题：显示所有选项（是/否问题不过滤）

#### 数据表格显示 Data Table Display
- **显示内容**: 选项名称、数量、百分比
- **排序方式**: 按数量从高到低排序
- **百分比计算**: 自动计算各选项占比

---

## 🔍 Specialized Analysis (Q3-Q5) 页面 (专项分析)

### 页面功能 Page Functions
- **实施框架分析**: Q3 - 分析实施框架各集群的产出分布
- **政策领域分析**: Q4 - 分析青年就业政策各支柱的产出分布
- **目标群体分析**: Q5 - 分析目标青年群体的产出分布
- **地区筛选**: 支持按组织单位/地区筛选数据

### 数据文件位置 Data File Locations
- **Q3 文件**: `orignaldata/PART2_base_dataQ3.csv`
- **Q4 文件**: `orignaldata/PART2_base_dataQ4.csv`
- **Q5 文件**: `orignaldata/PART2_base_dataQ5.csv`

### 筛选功能 Filtering Features
- **筛选字段**: `Department/Region` (部门/地区)
- **筛选方式**: 下拉菜单选择特定组织单位
- **全局年份筛选**: 支持按年份筛选数据

### 详细分析内容 Detailed Analysis Content

#### Q3 - 实施框架分类统计 Implementation Framework Distribution
- **图表标题**: "Distribution Of Outputs Across The Clusters Of The Implementation Framework"
- **统计类别**:
  - Knowledge development and dissemination (知识开发和传播)
  - Technical assistance and capacity-building of constituents (技术援助和成员能力建设)
  - Advocacy and partnerships (倡导和合作伙伴关系)
- **统计方法**: 统计每个分类中标记为'YES'的项目数量

#### Q4 - 青年就业政策分类统计 Youth Employment Policy Distribution
- **图表标题**: "Distribution Of Outputs Across The Pillars Of The Call For Action On Youth Employment"
- **统计类别**:
  - Employment and economic policies for youth employment (青年就业的就业和经济政策)
  - Employability – Education, training and skills, and the school-to-work transition (就业能力 – 教育、培训和技能，以及从学校到工作的过渡)
  - Labour market policies (劳动力市场政策)
  - Youth entrepreneurship and self-employment (青年创业和自主就业)
  - Rights for young people (青年人权利)

#### Q5 - 目标青年群体统计 Target Youth Groups Distribution
- **图表标题**: "Distribution Of Outputs Across Target Youth Groups, When Applicable"
- **统计类别**:
  - Young women (年轻女性)
  - Young people not in employment, education or training (NEET) (不在就业、教育或培训中的年轻人)
  - Young migrant workers (年轻移民工人)
  - Young refugees (年轻难民)
  - Young people - sexual orientation and gender identity (年轻人 - 性取向和性别认同)
  - Young people with disabilities (残疾年轻人)
  - Young rural workers (年轻农村工人)
  - Young indigenous people (年轻原住民)

---

## 📈 Specialized Analysis Pages (专项分析页面)

### 页面功能 Page Functions
- **独立页面标题**: 每个专项分析页面都有独立的主标题和副标题
- **产出统计对比**: 各问题类别的产出数量统计
- **主题化分析**: 按四大主题组织的详细频率分析
- **地区筛选**: 支持按组织单位筛选数据
- **多维度分析**: 资金来源、目标群体、交付方式等多角度分析

### 页面标题系统 Page Title System
每个专项分析页面都有独立的标题配置：

#### 📊 Outputs Count Statistics
- **主标题**: "📊 Outputs Count Statistics"
- **副标题**: "Overview of output counts across all analysis areas"

#### 📚 Knowledge Development & Dissemination
- **主标题**: "📚 Knowledge Development & Dissemination"
- **副标题**: "Analysis of knowledge development and dissemination outputs"

#### 🔧 Technical Assistance
- **主标题**: "🔧 Technical Assistance"
- **副标题**: "Analysis of technical assistance outputs and delivery"

#### 🎓 Capacity Development
- **主标题**: "🎓 Capacity Development"
- **副标题**: "Analysis of capacity development programs and outcomes"

#### 🤝 Advocacy & Partnerships
- **主标题**: "🤝 Advocacy & Partnerships"
- **副标题**: "Analysis of advocacy initiatives and partnership activities"

### 数据文件位置 Data File Locations
- **Q6 文件**: `orignaldata/PART3_base_dataQ6.csv` (知识发展与传播)
- **Q7 文件**: `orignaldata/PART3_base_dataQ7.csv` (技术援助)
- **Q10 文件**: `orignaldata/PART3_base_dataQ10.csv` (能力发展)
- **Q11 文件**: `orignaldata/PART3_base_dataQ11.csv` (倡导与合作伙伴关系)

### 筛选功能 Filtering Features
- **地区筛选**: `Department/Region` 字段筛选
- **年份筛选**: 全局年份筛选功能
- **实时应用**: 筛选条件实时应用到所有图表

### 页面布局结构 Page Layout Structure

#### 1. 产出统计对比 Outputs Count Comparison
- **图表标题**: "Outputs Count by Question"
- **数据来源**: 综合 Q6、Q7、Q10、Q11 四个数据文件
- **显示指标**: 
  - Number of staff reporting (报告员工数量)
  - Number of outputs delivered (交付产出数量)
- **图表类型**: 分组条形图

#### 2. 主题化频率分析 Themed Frequency Analysis

##### 主题1: Q6 - 知识发展与传播 Knowledge Development & Dissemination
- **主题颜色**: 浅蓝色背景
- **分析维度**:
  - 资金来源分析: "Funding Source Of Knowledge Development And Dissemination Outputs"
  - 目标群体分析: "Target Group Of Knowledge Development And Dissemination Outputs"
  - 产出类型分析: "Types Of Knowledge Development And Dissemination Outputs Delivered"

##### 主题2: Q7 - 技术援助 Technical Assistance
- **主题颜色**: 浅绿色背景
- **分析维度**:
  - 资金来源分析: "Funding Source Of Technical Assistance Outputs"
  - 目标群体分析: "Target Group Of Technical Assistance Outputs"
  - 地区分布分析: "Technical Assistance Outputs Across Regions" (显示前10个地区)

##### 主题3: Q10 - 能力发展 Capacity Development
- **主题颜色**: 浅黄色背景
- **分析维度**:
  - 交付方式分析: "Delivery Mode Of Capacity Development Outputs"
  - 资金来源分析: "Funding Source For Capacity Development Outputs"
  - 认证情况分析: "Capacity Development Outputs & Certification"
  - 目标群体分析: "Target Group Of Capacity Development Outputs"

##### 主题4: Q11 - 倡导与合作伙伴关系 Advocacy & Partnerships
- **主题颜色**: 浅粉色背景
- **分析维度**:
  - 资金来源分析: "Funding Source For Advocacy & Partnerships Related Outputs"
  - 目标群体分析: "Target Group For Advocacy & Partnerships Outputs"
  - 产出类型分析: "Types Of Advocacy Or Partnership Outputs"
  - 地区分布分析: "Advocacy & Partnership Outputs Across Regions" (显示前10个地区)
  - 地理重点分析: "Geographical Focus Of Advocacy And Partnerships Outputs"

### 图表样式说明 Chart Style Guidelines
- **饼图**: 显示各类别分布比例，每个扇形显示具体数量和百分比
- **条形图**: 显示各类别数量对比，适用于多类别比较
- **自动选择**: 根据数据特征自动选择最适合的图表类型

---

## 🔧 技术实现详情 Technical Implementation

### 系统架构 System Architecture
- **前端框架**: Streamlit
- **数据处理**: Pandas
- **可视化**: Plotly
- **样式管理**: 统一的 CSS 样式系统

### 统一头部设计 Unified Header Design
- **蓝色背景容器**: RGB(33, 45, 183)
- **ILO Logo**: 左侧显示国际劳工组织标志
- **年份感知标题**: 根据选择年份动态更新标题
- **响应式设计**: 适配不同屏幕尺寸

### 数据处理流程 Data Processing Workflow
1. **数据读取**: 从 CSV 文件读取原始数据
2. **数据清理**: 过滤无效和空值数据
3. **数据筛选**: 应用年份和地区筛选条件
4. **统计计算**: 计算各类别的统计数据
5. **图表生成**: 根据数据特征生成相应图表

### 性能优化 Performance Optimization
- **会话缓存**: 数据在会话中只加载一次
- **实时筛选**: 筛选条件实时应用，无需重新加载
- **智能图表**: 根据数据量自动选择最优图表类型

### 错误处理 Error Handling
- **文件检查**: 自动检测数据文件是否存在
- **数据验证**: 验证数据格式和完整性
- **友好提示**: 提供清晰的错误信息和解决建议

---

## 📊 数据质量标准 Data Quality Standards

### 数据完整性要求 Data Integrity Requirements
- 项目名称字段不能为空
- 数值字段不能是 'None'、'nan' 或空字符串
- 只统计符合标准的有效记录

### 数据筛选规则 Data Filtering Rules
- **百分比阈值**: 小于5%的选项可能被过滤（Q4、Q5）
- **地区显示**: 地区分布图只显示前10个地区
- **年份筛选**: 支持按具体年份筛选数据

---

## 🚀 使用指南 Usage Guide

### 启动应用 Starting the Application
```bash
cd streamlit
streamlit run streamlit_app.py
```

### 导航使用 Navigation Usage
1. **侧边栏导航**: 使用左侧导航菜单切换页面
2. **全局筛选**: 使用侧边栏的年份和地区筛选器
3. **交互功能**: 点击图表元素查看详细信息

### 数据筛选 Data Filtering
1. **年份筛选**: 在侧边栏选择特定年份或"All"查看所有年份
2. **地区筛选**: 在专项分析页面选择特定组织单位
3. **实时更新**: 筛选条件会立即应用到所有相关图表

### 图表交互 Chart Interaction
- **悬停信息**: 鼠标悬停查看详细数值
- **缩放功能**: 支持图表缩放和平移
- **下载功能**: 可下载图表为图片格式

---

## 📁 项目文件结构 Project File Structure

```
YEAP-10-8-2/
├── orignaldata/                    # 原始数据文件夹
│   ├── PART1_base_dataQ2-5.csv   # Q1-Q5 通用调查数据
│   ├── PART2_base_dataQ3.csv     # Q3 实施框架数据
│   ├── PART2_base_dataQ4.csv     # Q4 政策领域数据
│   ├── PART2_base_dataQ5.csv     # Q5 目标群体数据
│   ├── PART3_base_dataQ6.csv     # Q6 知识发展数据
│   ├── PART3_base_dataQ7.csv     # Q7 技术援助数据
│   ├── PART3_base_dataQ10.csv    # Q10 能力发展数据
│   ├── PART3_base_dataQ11.csv    # Q11 倡导合作数据
│   ├── logo.png                   # ILO 标志文件
│   └── question_list.csv          # 问题列表文件
├── streamlit/                      # Streamlit 应用文件夹
│   ├── streamlit_app.py           # 主应用文件
│   ├── st_landing_dashboard.py    # Overview 页面
│   ├── st_q6q7q10q11_dashboard.py # 专项分析页面 (Q6-Q11)
│   ├── st_styles.py               # 样式管理文件
│   ├── visualizer.py              # 可视化工具文件
│   └── requirements.txt           # Python 依赖文件
├── Data_Sources_Documentation.md   # 本说明文档
├── TUTORIAL.md                    # 项目教程文档
├── 独立页面标题修改说明.md         # 标题修改指南
├── start_dashboard.py             # 启动脚本
├── upload_to_github.ps1           # GitHub 上传脚本
└── README.md                      # 项目说明文件
```

---

## 🔍 故障排除 Troubleshooting

### 常见问题 Common Issues

#### 1. 数据文件未找到
**问题**: 显示"No data available"或文件路径错误
**解决方案**: 
- 检查 `orignaldata` 文件夹是否存在
- 确认 CSV 文件名称正确
- 验证文件路径和编码格式

#### 2. 图表显示异常
**问题**: 图表无法显示或显示错误
**解决方案**:
- 检查数据格式是否正确
- 确认数值字段不包含非数字字符
- 验证数据是否为空

#### 3. 筛选功能无效
**问题**: 地区或年份筛选不起作用
**解决方案**:
- 检查数据文件中是否包含相应的筛选字段
- 确认字段名称拼写正确
- 验证数据格式一致性

### 性能优化建议 Performance Optimization Tips
1. **数据预处理**: 定期清理和优化数据文件
2. **缓存使用**: 利用 Streamlit 的缓存功能
3. **分页显示**: 对大量数据使用分页显示
4. **图表优化**: 合理选择图表类型和数据点数量

---

## 📞 技术支持 Technical Support

如需技术支持或有任何问题，请参考：
1. **文档指南**: 查看本说明文档和标题修改指南
2. **代码注释**: 查看源代码中的详细注释
3. **日志信息**: 检查控制台输出的错误信息
4. **数据验证**: 使用数据质量检查工具验证数据完整性


