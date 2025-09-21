# 数据分析仪表板说明书 Data Analysis Dashboard Guide

## 1. 基础调查分析 General Survey Analysis

### 数据文件位置 Data File Location
- **文件名 File**: `orignaldata/PART1_base_dataQ2-5.csv`
- **文件类型 Format**: Excel表格文件，包含三列：`question`(问题), `option`(选项), `count`(数量)

### 图表制作方式 Chart Creation Methods

#### 1.1 问题回答分布图 Question Response Distribution Charts
- **数据来源 Data Source**: 从PART1_base_dataQ2-5.csv文件读取所有问题
- **数据对应关系 Data Mapping**:
  - `question`列 → 图表的标题
  - `option`列 → 图表中的分类标签
  - `count`列 → 图表中显示的数字
- **计算方式 Calculation Method**: 直接使用表格中已有的统计数字
- **图表样式选择 Chart Type Selection**: 系统自动选择最合适的图表：
  - 饼图：当选项≤5个时使用
  - 竖条图：当选项>5个或标签文字较长时使用
  - 横条图：当选项>10个或标签文字>20个字符时使用

#### 1.1 问题选择和图表显示 Question Selection and Chart Display
- **问题范围 Question Range**: 只显示Q2-Q5的问题
- **选择方式 Selection Method**: 下拉菜单选择要分析的问题
- **图表类型 Chart Types**: 
  - 条形图 Bar Chart
  - 饼图 Pie Chart  
  - 横条图 Horizontal Bar Chart
- **自动选择逻辑 Auto Selection Logic**:
  - 饼图：当选项≤5个时使用
  - 竖条图：当选项>5个或标签文字较长时使用
  - 横条图：当选项>10个或标签文字>20个字符时使用

#### 1.2 数据表格显示 Data Table Display
- **显示内容 Display Content**: 选项名称、数量、百分比
- **排序方式 Sorting**: 按数量从高到低排序
- **数据过滤 Data Filtering**: 
  - Q4和Q5问题：过滤掉少于5%的选项和"其他"选项
  - Q2问题：显示所有选项（是/否问题不过滤）

---

## 2. Q3-Q5专题分析 Specialized Analysis (Q3-Q5)

### 数据文件位置 Data File Locations
- **Q3文件 Q3 File**: `orignaldata/PART2_base_dataQ3.csv`
- **Q4文件 Q4 File**: `orignaldata/PART2_base_dataQ4.csv`
- **Q5文件 Q5 File**: `orignaldata/PART2_base_dataQ5.csv`

### 数据筛选功能 Data Filtering
- **筛选字段 Filter Column**: `Department/Region` (部门/地区)
- **筛选方式 Filter Method**: 可以选择特定的组织单位来查看对应数据


#### 2.1 Q3 - 实施框架分类统计 Implementation Framework Distribution
- **数据文件 Data File**: PART2_base_dataQ3.csv
- **图表标题 Chart Title**: "Distribution Of Outputs Across The Clusters Of The Implementation Framework" (实施框架各集群的产出分布)
- **统计内容 What We Count**:
  - `Knowledge development and dissemination. ` → "知识开发和传播"
  - `Technical assistance and capacity-building of constituents. ` → "技术援助和成员能力建设"
  - `Advocacy and partnerships. ` → "倡导和合作伙伴关系"
- **统计方法 How We Count**: 数一数每个分类中标记为'YES'的项目有多少个
- **图表样式 Chart Style**: 少于5个分类用饼图，5个或以上用条形图

#### 2.2 Q4 - 青年就业政策分类统计 Youth Employment Policy Distribution
- **数据文件 Data File**: PART2_base_dataQ4.csv
- **图表标题 Chart Title**: "Distribution Of Outputs Across The Pillars Of The Call For Action On Youth Employment" (青年就业行动呼吁各支柱的产出分布)
- **统计内容 What We Count**:
  - `Employment and economic policies for youth employment. ` → "青年就业的就业和经济政策"
  - `Employability – Education, training and skills, and the school-to-work transition. ` → "就业能力 – 教育、培训和技能，以及从学校到工作的过渡"
  - `Labour market policies. ` → "劳动力市场政策"
  - `Youth entrepreneurship and self-employment. ` → "青年创业和自主就业"
  - `Rights for young people. ` → "青年人权利"
- **统计方法 How We Count**: 数一数每个政策分类中标记为'YES'的项目有多少个
- **图表样式 Chart Style**: 因为有5个分类，所以用条形图

#### 2.3 Q5 - 目标青年群体统计 Target Youth Groups Distribution
- **数据文件 Data File**: PART2_base_dataQ5.csv
- **图表标题 Chart Title**: "Distribution Of Outputs Across Target Youth Groups, When Applicable" (目标青年群体的产出分布，如适用)
- **统计内容 What We Count**:
  - `Young women` → "年轻女性"
  - `Young people not in employment, education or training (NEET) ` → "不在就业、教育或培训中的年轻人(NEET)"
  - `Young migrant workers ` → "年轻移民工人"
  - `Young refugees ` → "年轻难民"
  - `Young people - sexual orientation and gender identity ` → "年轻人 - 性取向和性别认同"
  - `Young people with disabilities ` → "残疾年轻人"
  - `Young rural workers  ` → "年轻农村工人"
  - `Young indigenous people ` → "年轻原住民"
- **统计方法 How We Count**: 数一数每个目标群体中标记为'YES'的项目有多少个
- **图表样式 Chart Style**: 因为有8个分类，所以用条形图

---

## 3. Q6-Q11专题分析 Specialized Analysis (Q6-Q11)

### 数据文件路径 Data File Paths
- **Q6文件 Q6 File**: `orignaldata/PART3_base_dataQ6.csv`
- **Q7文件 Q7 File**: `orignaldata/PART3_base_dataQ7.csv`
- **Q10文件 Q10 File**: `orignaldata/PART3_base_dataQ10.csv`
- **Q11文件 Q11 File**: `orignaldata/PART3_base_dataQ11.csv`

### 数据筛选功能 Data Filtering
- **筛选字段 Filter Column**: `Department/Region` (部门/地区)
- **筛选方式 Filter Method**: 可以选择特定的组织单位来查看对应数据

### 页面显示内容 Page Display Content

#### 3.1 各问题作品数量对比图 Outputs Count Comparison Chart

##### 图表1：各问题产出数量统计总览
- **图表标题 Chart Title**: "Outputs Count by Question" (各问题产出数量统计)
- **数据来源 Data Source**: 综合Q6、Q7、Q10、Q11四个数据文件的统计结果
  - Q6: PART3_base_dataQ6.csv (Knowledge development & dissemination)
  - Q7: PART3_base_dataQ7.csv (Technical assistance)
  - Q10: PART3_base_dataQ10.csv (Capacity building)
  - Q11: PART3_base_dataQ11.csv (Advocacy & partnerships)
- **统计方式 How We Count**: 统计每个问题类别下的独特用户数（即去重后的不同员工数量）和有效作品总数（即该类别下所有产出的数量）
- **图表样式 Chart Style**: 分组条形图，显示"Number of staff reporting"(报告员工数量)和"Number of outputs delivered"(交付产出数量)两个指标
- **显示内容 Display Content**: 
  - X轴：四个问题类别的标签（支持换行显示）
  - Y轴：数量统计
  - 两个数据系列：员工报告数量（蓝色）和产出交付数量（橙色）

#### 3.2 详细分类统计 Detailed Category Statistics

**图表样式说明 Chart Style Guide**:
- **饼图**: 显示各类别的分布比例，每个扇形显示具体数量和百分比
- **条形图**: 显示各类别的数量对比，X轴显示类别名称，Y轴显示数量

##### 3.2.1 Q6 - 知识发展与传播项目分析 Knowledge Development & Dissemination

##### 图表2：Q6知识发展产出的资金来源分析
- **数据文件 Data File**: PART3_base_dataQ6.csv
- **图表标题 Chart Title**: "Funding Source Of Knowledge Development And Dissemination Outputs In 2024" (2024年知识发展与传播产出的资金来源)
- **分析字段 Analysis Field**: `Funding source (Options: regular budget or extrabudgetary)`
- **统计方式 How We Count**: 统计该字段中不同选项的出现次数

##### 图表3：Q6知识发展产出的目标群体分析
- **数据文件 Data File**: PART3_base_dataQ6.csv
- **图表标题 Chart Title**: "Target Group Of Knowledge Development And Dissemination Outputs In 2024" (2024年知识发展与传播产出的目标群体)
- **分析字段 Analysis Field**: `Focus (Options: Youth only or Youth is one of the target groups)`
- **统计方式 How We Count**: 统计该字段中不同选项的出现次数

##### 图表4：Q6知识发展产出的类型分析
- **数据文件 Data File**: PART3_base_dataQ6.csv
- **图表标题 Chart Title**: "Types Of Knowledge Development And Dissemination Outputs Delivered In 2024" (2024年交付的知识发展与传播产出类型)
- **分析字段 Analysis Field**: `Type of publication (Options: Evaluation, or Guidance/tools, or Technical Report, or Working paper, or Data/Database)`
- **统计方式 How We Count**: 统计该字段中不同出版物类型的出现次数

##### 3.2.2 Q7 - 技术援助项目分析 Technical Assistance

##### 图表5：Q7技术援助产出的资金来源分析
- **数据文件 Data File**: PART3_base_dataQ7.csv
- **图表标题 Chart Title**: "Funding Source Of Technical Assistance Outputs In 2024" (2024年技术援助产出的资金来源)
- **分析字段 Analysis Field**: `Funding source (Options: regular budget or extrabudgetary)`
- **统计方式 How We Count**: 统计该字段中不同选项的出现次数

##### 图表6：Q7技术援助产出的目标群体分析
- **数据文件 Data File**: PART3_base_dataQ7.csv
- **图表标题 Chart Title**: "Target Group Of Technical Assistance Outputs In 2024" (2024年技术援助产出的目标群体)
- **分析字段 Analysis Field**: `Focus (Options: Youth only or Youth is one of the target groups)`
- **统计方式 How We Count**: 统计该字段中不同选项的出现次数

##### 图表7：Q7技术援助产出的地区分布分析
- **数据文件 Data File**: PART3_base_dataQ7.csv
- **图表标题 Chart Title**: "Technical Assistance Outputs Across Regions" (各地区技术援助产出分布)
- **分析字段 Analysis Field**: `Country or Region`
- **统计方式 How We Count**: 统计该字段中不同国家/地区的出现次数，显示前10个地区
- **图表样式 Chart Style**: 条形图显示各地区产出数量对比
- **显示内容 Display Content**: 
  - 前10个地区的技术援助产出数量对比
  - X轴显示地区名称，Y轴显示产出数量

##### 3.2.3 Q10 - 能力培训项目分析 Capacity Development

##### 图表8：Q10能力发展产出的交付方式分析
- **数据文件 Data File**: PART3_base_dataQ10.csv
- **图表标题 Chart Title**: "Delivery Mode Of Capacity Development Outputs In 2024" (2024年能力发展产出的交付方式)
- **分析字段 Analysis Field**: `In person or online or both`
- **统计方式 How We Count**: 统计该字段中不同交付方式的出现次数

##### 图表9：Q10能力发展产出的资金来源分析
- **数据文件 Data File**: PART3_base_dataQ10.csv
- **图表标题 Chart Title**: "Funding Source For Capacity Development Outputs In 2024" (2024年能力发展产出的资金来源)
- **分析字段 Analysis Field**: `Funding source (Options: regular budget or extrabudgetary)`
- **统计方式 How We Count**: 统计该字段中不同选项的出现次数

##### 图表10：Q10能力发展产出的认证情况分析
- **数据文件 Data File**: PART3_base_dataQ10.csv
- **图表标题 Chart Title**: "Capacity Development Outputs & Certification" (能力发展产出与认证)
- **分析字段 Analysis Field**: `With certification (Yes or No)`
- **统计方式 How We Count**: 统计该字段中是否提供认证的出现次数

##### 图表11：Q10能力发展产出的目标群体分析
- **数据文件 Data File**: PART3_base_dataQ10.csv
- **图表标题 Chart Title**: "Target Group Of Capacity Development Outputs In 2024" (2024年能力发展产出的目标群体)
- **分析字段 Analysis Field**: `Focus (Options: Youth only or Youth is one of the target groups)`
- **统计方式 How We Count**: 统计该字段中不同选项的出现次数
- **图表样式 Chart Style**: 饼图显示目标群体分布比例
- **显示内容 Display Content**: 
  - 仅青年 (Youth only) 和青年是目标群体之一 (Youth is one of the target groups) 的分布比例
  - 每个扇形显示具体数量和百分比

##### 3.2.4 Q11 - 倡导合作项目分析 Advocacy & Partnerships

##### 图表12：Q11倡导合作产出的资金来源分析
- **数据文件 Data File**: PART3_base_dataQ11.csv
- **图表标题 Chart Title**: "Funding Source For Advocacy & Partnerships Related Outputs In 2024" (2024年倡导与合作伙伴关系相关产出的资金来源)
- **分析字段 Analysis Field**: `Funding source (Options: regular budget or extrabudgetary)`
- **统计方式 How We Count**: 统计该字段中不同选项的出现次数

##### 图表13：Q11倡导合作产出的目标群体分析
- **数据文件 Data File**: PART3_base_dataQ11.csv
- **图表标题 Chart Title**: "Target Group For Advocacy & Partnerships Outputs In 2024" (2024年倡导与合作伙伴关系产出的目标群体)
- **分析字段 Analysis Field**: `Focus (Options: Youth only or Youth is one of the target groups)`
- **统计方式 How We Count**: 统计该字段中不同选项的出现次数
- **图表样式 Chart Style**: 饼图显示目标群体分布比例
- **显示内容 Display Content**: 
  - 仅青年 (Youth only) 和青年是目标群体之一 (Youth is one of the target groups) 的分布比例
  - 每个扇形显示具体数量和百分比

##### 图表14：Q11倡导合作产出的类型分析
- **数据文件 Data File**: PART3_base_dataQ11.csv
- **图表标题 Chart Title**: "Types Of Advocacy Or Partnership Outputs In 2024" (2024年倡导与合作伙伴关系产出类型)
- **分析字段 Analysis Field**: `Type of advocacy or partnership outputs in 2024`
- **统计方式 How We Count**: 统计该字段中不同类型的出现次数
- **图表样式 Chart Style**: 饼图显示类型分布比例
- **显示内容 Display Content**: 
  - 不同倡导合作产出类型的分布比例
  - 每个扇形显示具体数量和百分比

##### 图表15：Q11倡导合作产出的地区分布分析
- **数据文件 Data File**: PART3_base_dataQ11.csv
- **图表标题 Chart Title**: "Advocacy & Partnership Outputs Across Regions" (各地区倡导与合作伙伴关系产出分布)
- **分析字段 Analysis Field**: `Specify name of the Region/country`
- **统计方式 How We Count**: 统计该字段中不同地区的出现次数，显示前10个地区
- **图表样式 Chart Style**: 条形图显示各地区产出数量对比
- **显示内容 Display Content**: 
  - 前10个地区的倡导合作产出数量对比
  - X轴显示地区名称，Y轴显示产出数量

##### 图表16：Q11倡导合作产出的地理重点分析
- **数据文件 Data File**: PART3_base_dataQ11.csv
- **图表标题 Chart Title**: "Geographical Focus Of Advocacy And Partnerships Outputs" (倡导与合作伙伴关系产出的地理重点)
- **分析字段 Analysis Field**: `Geographical focus (Global, Regional or National/local)`
- **统计方式 How We Count**: 统计该字段中不同地理重点的出现次数
- **图表样式 Chart Style**: 饼图显示地理重点分布比例
- **显示内容 Display Content**: 
  - 全球 (Global)、地区 (Regional)、国家/地方 (National/local) 的分布比例
  - 每个扇形显示具体数量和百分比

#### 3.3 详细数据表格 Data Table Display
- **数据来源 Data Source**: 把所有Q6、Q7、Q10、Q11文件的数据合并在一起
- **筛选条件 Filter Condition**: 只显示有项目名称的记录 (不显示空白行)
- **表格显示内容 Table Columns**:
  - 基本信息: `Question` (问题编号), `UserId` (用户ID), `Department/Region` (部门/地区)
  - 项目名称: 每个问题对应的项目名称字段
  - 其他信息: 每个数据文件中的其他相关字段

---

## 4. 技术说明 Technical Notes

### 数据处理流程 Data Processing
1. 读取CSV文件 → 数据清理 → 筛选过滤 → 统计计算 → 生成图表

### 图表选择规则 Chart Selection
- **饼图**：≤5个分类时使用
- **条形图**：>5个分类或标签较长时使用
- **横向条形图**：>10个分类或标签>20字符时使用

### 数据质量标准 Data Quality
- 项目名称字段不能为空
- 数值不能是'None'、'nan'或空字符串
- 只统计符合标准的有效记录

---

## 5. 技术实现详情 Implementation Details

### 数据文件位置 File Locations
所有数据文件都放在项目根目录下的orignaldata文件夹中 All data files are in the orignaldata folder under project root:
```
orignaldata/
├── PART1_base_dataQ2-5.csv
├── PART2_base_dataQ3.csv
├── PART2_base_dataQ4.csv
├── PART2_base_dataQ5.csv
├── PART3_base_dataQ6.csv
├── PART3_base_dataQ7.csv
├── PART3_base_dataQ10.csv
└── PART3_base_dataQ11.csv
```

### 错误处理 Error Handling
- 找不到文件时会显示错误提示 Missing files trigger error messages
- 没有数据时显示"无可用数据"提示 Empty datasets show "No data available" messages
- 处理过程中会自动过滤掉无效数据 Invalid data is automatically filtered out during processing

### 性能说明 Performance Notes
- 数据在每次会话中只加载一次 Data is loaded once per session
- 地区筛选功能实时应用 Regional filtering is applied in real-time
- 图表根据用户选择动态生成 Charts are generated dynamically based on user selections
