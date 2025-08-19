# Ollama Examples

This directory contains examples for using LangExtract with Ollama for local LLM inference.

For setup instructions and documentation, see the [main README's Ollama section](../../README.md#using-local-llms-with-ollama).

## Quick Reference

**Local setup:**
```bash
ollama pull gemma2:2b
python quickstart.py
```

**Docker setup:**
```bash
docker-compose up
```

## Files

- `quickstart.py` - Basic extraction example with configurable model
- `docker-compose.yml` - Production-ready Docker setup with health checks
- `Dockerfile` - Container definition for LangExtract

## Configuration Options

### Timeout Settings

For slower models or large prompts, you may need to increase the timeout (default: 120 seconds):

```python
import langextract as lx

result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="llama3.1:70b",  # Larger model may need more time
    timeout=300,  # 5 minutes
    model_url="http://localhost:11434",
)
```

Or using ModelConfig:

```python
config = lx.factory.ModelConfig(
    model_id="llama3.1:70b",
    provider_kwargs={
        "model_url": "http://localhost:11434",
        "timeout": 300,  # 5 minutes
    }
)
```

## Model License

Ollama models come with their own licenses. For example:
- Gemma models: [Gemma Terms of Use](https://ai.google.dev/gemma/terms)
- Llama models: [Meta Llama License](https://llama.meta.com/llama-downloads/)

Please review the license for any model you use.


## 如何查看 Ollama 正在运行的模型（Linux）

你可以使用如下命令来查看 Ollama 当前正在运行的模型进程：
ps aux | grep ollama

在 Linux 系统中，如果你想停止 Ollama 正在运行的某个模型，可以通过以下几种方式实现：

### 1. 直接停止 Ollama 服务（会停止所有模型）

kill 24104 

# 环境配置 适配docx文件
pip install python-docx



DEBUG:absl:Initialized Annotator with prompt:
提取出公司、产品的名称、用途、技术参数、使用方法、特点、优势等对公司和产品进行介绍的信息。

Examples
Q: 山西云晟科技有限公司成立于2015年，坐落于有太行明珠之称的山西省晋城市，并先后在武汉市、西安市、长治市、临汾市、阳泉市成立子分公司。公司注册资金1000万。        云晟科技是国内解决工业行业实操培训的科技公司。公司致力于将AI+XR(VR、MR、APP等)高尖端技术应用于安全教育与培训领域，帮助企业和个人更高效、安全、真实的体验、学习。     
A: {
  "extractions": [
    {
      "公司介绍": "山西云晟科技有限公司成立于2015年，坐落于有太行明珠之称的山西省晋城市，并先后在武汉市、西安市、长治市、临汾市、阳泉市成立子分公司。公司注册资金1000万。        云晟科技是国内解决工业行业实操培训的科技公司。公司致力于将AI+XR(VR、MR、APP等)高尖端技术应用于安全教育与培训领域，帮助企业和个人更高效、安全、真实的体验、学习。     ",
      "公司介绍_attributes": {
        "name": "山西云晟科技有限公司",
        "genre": "云晟科技是国内解决工业行业实操培训的科技公司"
      }
    }
  ]
}

Q: 
A: 

