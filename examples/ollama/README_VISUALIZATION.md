# Langextract 可视化功能使用指南

## 概述

本项目提供了两个版本的 quickstart 示例，支持将 langextract 的提取结果保存为 JSON 文件并生成交互式 HTML 可视化。

## 文件说明

### 1. `quickstart.py` - 基础版本
- 简单的作者信息提取示例
- 支持 JSON 结果保存
- 可选的可视化功能

### 2. `long_text.py` - 文学文本处理版本
- 专门处理文学文本（莎士比亚戏剧）
- 支持 Project Gutenberg 在线文本
- 保留并发处理功能
- 完整的可视化功能

## 使用方法

### 基础版本

```bash
# 基本运行（只保存 JSON）
python quickstart.py

# 生成可视化
python quickstart.py --visualize

# 使用不同模型
python quickstart.py --model-id llama3.2:1b --visualize

# 调整温度参数
python quickstart.py --temperature 0.5 --visualize
```

### 文学文本版本

```bash
# 直接运行示例（使用示例文本）
python long_text.py

# 在代码中调用函数
from long_text import run_literary_extraction, save_and_visualize_results

# 处理示例文本
result = run_literary_extraction(
    model_id="gemma2:2b",
    temperature=0.3,
    text_source="sample"
)

# 处理 Project Gutenberg 文本
result = run_literary_extraction(
    model_id="llama3.2:1b",
    temperature=0.5,
    text_source="gutenberg"
)

# 保存和可视化结果
save_and_visualize_results(result, "gemma2:2b", 0.3, "sample")
```

## 输出文件

### JSON 文件
- `extraction_result_{model_id}.json` - 基础版本
- `literary_extraction_{model_id}.jsonl` - 文学文本版本

包含：
- 模型配置信息
- 输入文本和提示词
- 提取结果和属性
- 字符位置信息

### JSONL 文件
- `extraction_result_{model_id}.jsonl` - 基础版本（用于可视化）
- `literary_extraction_{model_id}.jsonl` - 文学文本版本（用于可视化）

### HTML 可视化文件
- `extraction_visualization_{model_id}.html` - 基础版本
- `literary_visualization_{model_id}.html` - 文学文本版本

## 可视化功能

### 交互式特性
- **文本高亮**：提取的实体在原文中高亮显示
- **属性展示**：点击实体查看详细属性
- **分类筛选**：按提取类别筛选显示
- **位置导航**：快速跳转到实体位置

### 支持的数据类型
1. **简单文本**：作者信息提取（quickstart.py）
2. **文学文本**：角色、情感、关系提取（long_text.py）
   - 支持 Project Gutenberg 在线文本
   - 支持示例文本快速测试
   - 保留并发处理功能

## 示例输出

### 简单文本示例
```json
{
  "model_id": "gemma2:2b",
  "temperature": 0.3,
  "input_text": "Isaac Asimov was a prolific science fiction writer.",
  "extractions": [
    {
      "class": "author_details",
      "text": "Isaac Asimov was a prolific science fiction writer.",
      "attributes": {
        "name": "Isaac Asimov",
        "genre": "science fiction"
      },
      "char_interval": {
        "start": 0,
        "end": 51
      }
    }
  ]
}
```

### 文学文本示例
```json
{
  "extractions": [
    {
      "class": "character",
      "text": "ROMEO",
      "attributes": {
        "emotional_state": "wonder"
      }
    },
    {
      "class": "emotion",
      "text": "But soft!",
      "attributes": {
        "feeling": "gentle awe",
        "character": "Romeo"
      }
    },
    {
      "class": "relationship",
      "text": "Juliet is the sun",
      "attributes": {
        "type": "metaphor",
        "character_1": "Romeo",
        "character_2": "Juliet"
      }
    }
  ]
}
```

## 故障排除

### 常见问题

1. **可视化生成失败**
   - 确保 langextract 版本支持 `lx.visualize()` 功能
   - 检查 JSONL 文件是否正确生成

2. **模型连接失败**
   ```bash
   # 确保 Ollama 正在运行
   ollama serve
   
   # 检查模型是否已安装
   ollama list
   
   # 安装缺失的模型
   ollama pull gemma2:2b
   ```

3. **文件权限问题**
   ```bash
   # 确保有写入权限
   chmod 755 .
   ```

### 调试模式

```bash
# 启用详细日志
export LANGEXTRACT_DEBUG=1
python quickstart.py --visualize
python long_text.py
```

## 高级用法

### 自定义文本处理

可以修改代码中的 `input_text` 和 `examples` 来处理自定义文本：

```python
# 在 run_enhanced_extraction 函数中添加新的文本类型
elif text_type == "custom":
    input_text = "你的自定义文本"
    prompt = "你的自定义提示词"
    examples = [
        # 你的自定义示例
    ]
```

### 批量处理

```python
# 处理多个文件
texts = ["文本1", "文本2", "文本3"]
results = []

for text in texts:
    result = lx.extract(
        text_or_documents=text,
        prompt_description=prompt,
        examples=examples,
        model_id=model_id
    )
    results.append(result)

# 保存所有结果
lx.io.save_annotated_documents(results, output_name="batch_results.jsonl")
```

## 性能优化

### 模型选择
- **快速处理**：`gemma2:2b`, `llama3.2:1b`
- **高质量**：`mistral:7b`, `qwen2.5:7b`
- **平衡**：`llama3.2:3b`

### 参数调优
- **temperature**: 0.1-0.3 用于精确提取，0.5-0.8 用于创造性提取
- **max_workers**: 增加并行处理数量
- **max_char_buffer**: 调整文本块大小

## 扩展功能

### 集成其他模型
```python
# 使用 OpenAI
model_config = lx.factory.ModelConfig(
    model_id="gpt-4",
    provider_kwargs={
        "api_key": "your-api-key",
        "format_type": lx.data.FormatType.JSON,
    },
)
```

### 自定义可视化
```python
# 生成自定义 HTML 报告
def generate_custom_report(result, output_file):
    html_content = f"""
    <html>
    <head><title>Custom Report</title></head>
    <body>
        <h1>Extraction Results</h1>
        {generate_results_html(result)}
    </body>
    </html>
    """
    with open(output_file, 'w') as f:
        f.write(html_content)
```

## 许可证

本项目遵循 Apache License 2.0 许可证。 