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


### Keywords (Company)
- Company name: 山西晋控装备创力智能制造有限公司
- Establishment date: 2021年9月30日
- Registered address: 长治市经济技术开发区
- Registered capital: 10000万元
- Industry: 煤矿机械
- Development direction: 智能化、绿色化转型，推动煤机装备升级和制造模式创新
- Core goal: 提升煤机产品的智能化水平，降低能耗与排放，助力行业可持续发展
- Main business: 研发、制造综采工作面液压支架电液控系统、智能化控制系统、集中供液系统、高端智能乳化液泵站、高端智能喷雾泵站


### Keywords (Product)
- Product name: FHDA1.6/31.5X电磁先导阀
- Composition: 由两组电磁铁驱动的二位三通换向阀组成
- Structure: 卧式
- Nominal pressure: 31.5MPa
- Nominal diameter: 1.6mm
- Rated working voltage: DC12V
- Working current: ≤120mA
- Electrical connector: M12(圆头)
- Overall dimensions: 155mm×84mm×40mm
- Advantages: 体积小、性能可靠、能耗低、维修方便
- Features: 结构简单、可靠、可维护性强，可自动控制或手动控制
- Application: 可单独使用或和电液控换向阀配套使用