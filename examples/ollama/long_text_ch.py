import langextract as lx
import textwrap
import os
from collections import Counter, defaultdict
import docx

# Define comprehensive prompt and examples for complex literary text
prompt = textwrap.dedent("""\
    提取出公司、产品的名称、用途、技术参数、使用方法、特点、优势等对公司和产品进行介绍的信息。
    """)

examples = [
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            山西云晟科技有限公司成立于2015年，坐落于有太行明珠之称的山西省晋城市，并先后在武汉市、西安市、长治市、临汾市、阳泉市成立子分公司。公司注册资金1000万。
            """),
        extractions=[
            lx.data.Extraction(
                extraction_class="公司介绍",
                extraction_text=(
                    "山西云晟科技有限公司成立于2015年，坐落于有太行明珠之称的山西省晋城市，并先后在武汉市、西安市、长治市、临汾市、阳泉市成立子分公司。公司注册资金1000万。        云晟科技是国内解决工业行业实操培训的科技公司。公司致力于将AI+XR(VR、MR、APP等)高尖端技术应用于安全教育与培训领域，帮助企业和个人更高效、安全、真实的体验、学习。     "
                ),
                attributes={
                    "name": "山西云晟科技有限公司",
                    "genre": "云晟科技是国内解决工业行业实操培训的科技公司",
                    "establishment_date": "2015 年",
                    "location": "山西省晋城市",
                    "registered_capital": "1000 万",
                },
            )
        ]
    )
]

def read_docx_file(file_path):
    """读取 DOCX 文件内容"""
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        print(f"❌ 读取 DOCX 文件失败: {e}")
        return None


def normalize_quotes(text):
    """标准化引号，将中文引号转换为英文引号"""
    # 中文引号到英文引号的映射
    quote_mapping = {
        '"': '"',  # 中文双引号左 -> 英文双引号
        '"': '"',  # 中文双引号右 -> 英文双引号
        ''': "'",  # 中文单引号左 -> 英文单引号
        ''': "'",  # 中文单引号右 -> 英文单引号
    }
    
    for chinese_quote, english_quote in quote_mapping.items():
        text = text.replace(chinese_quote, english_quote)
    
    return text


def run_docx_extraction(model_id="qwen3:8b", temperature=0.3, docx_path="/app/test_data/晋控创力产品介绍文字版.docx"):
    """专门处理 DOCX 文件的提取函数"""
    print(f"📄 正在处理 DOCX 文件: {docx_path}")
    
    # 读取 DOCX 文件
    text_content = read_docx_file(docx_path)
    if text_content is None:
        raise FileNotFoundError(f"无法读取文件: {docx_path}")
    
    # 标准化引号
    text_content = normalize_quotes(text_content)
    
    print(f"📝 文件内容长度: {len(text_content)} 字符")
    print(f"📖 内容预览: {text_content[:200]}...")
    
    # 配置模型
    model_config = lx.factory.ModelConfig(
        model_id=model_id,
        provider_kwargs={
            "model_url": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            "format_type": lx.data.FormatType.JSON,
            "temperature": temperature,
        },
    )
    
    try:
        # 执行提取
        result = lx.extract(
            text_or_documents=text_content,
            prompt_description=prompt,
            examples=examples,
            config=model_config,
            use_schema_constraints=True,
            extraction_passes=2,      # 减少passes以避免JSON错误累积
            max_workers=10,           # 减少并发以避免竞争条件
            max_char_buffer=500       # 减小缓冲区以提高准确性
        )
        
        return result
        
    except Exception as e:
        print(f"⚠️  提取过程中出现错误: {e}")
        print("🔄 尝试使用更简单的配置重新提取...")
        

def run_literary_extraction(model_id="qwen3:8b", temperature=0.3, text_source="gutenberg"):
    """Run literary text extraction using Ollama."""
    
    if text_source == "gutenberg":
        # Process Romeo & Juliet directly from Project Gutenberg
        print("Downloading and processing Romeo and Juliet from Project Gutenberg...")
        text_or_documents = "https://www.gutenberg.org/files/1513/1513-0.txt"
    elif text_source == "docx":
        # Use local DOCX file
        docx_path = "/app/test_data/晋控创力产品介绍文字版.docx"
        print(f"Processing local DOCX file: {docx_path}")
        text_content = read_docx_file(docx_path)
        if text_content is None:
            raise FileNotFoundError(f"无法读取文件: {docx_path}")
        text_or_documents = text_content
    else:
        # Use sample text for testing
        text_or_documents = textwrap.dedent("""\
            晋控创力（山西晋控装备创力智能制造有限公司介绍）成立于2021年9月30日，注册地位于长治市经济技术开发区，注册资本10000万元。公司在煤矿机械领域积极探索智能化、绿色化转型，致力于推动煤机装备升级和制造模式创新。我们希望通过技术创新和工艺优化，提升煤机产品的智能化水平，同时降低能耗与排放，助力行业可持续发展。这一方向既符合国家推动制造业智能化、绿色化升级的政策要求，也是我们立足行业实际、稳步推进产业现代化的重要路径。公司以打造高端智能开采控制技术装备产品为主，研发、制造综采工作面液压支架电液控系统、智能化控制系统、集中供液系统、高端智能乳化液泵站，高端智能喷雾泵站。""")
        print("Processing sample Chinese text...")

    model_config = lx.factory.ModelConfig(
        model_id=model_id,
        provider_kwargs={
            "model_url": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            "format_type": lx.data.FormatType.JSON,
            "temperature": temperature,
        },
    )

    result = lx.extract(
        text_or_documents=text_or_documents,
        prompt_description=prompt,
        examples=examples,
        config=model_config,
        use_schema_constraints=True,
        extraction_passes=3,      # Multiple passes for improved recall
        max_workers=20,           # Parallel processing for speed
        max_char_buffer=1000      # Smaller contexts for better accuracy
    )

    return result


def save_and_visualize_results(result, model_id, temperature, text_source):
    """Save results to files and generate interactive visualization."""
    
    # Save as JSONL format for visualization
    jsonl_file = f"literary_extraction_{model_id.replace(':', '_')}.jsonl"
    lx.io.save_annotated_documents([result], output_name=jsonl_file, output_dir=".")
    print(f"📊 JSONL 文件已保存到: {jsonl_file}")
    
    # Generate the interactive visualization
    try:
        print("🎨 正在生成交互式可视化...")
        html_content = lx.visualize(jsonl_file)
        
        html_file = f"literary_visualization_{model_id.replace(':', '_')}.html"
        with open(html_file, "w", encoding='utf-8') as f:
            if hasattr(html_content, 'data'):
                f.write(html_content.data)  # For Jupyter/Colab
            else:
                f.write(html_content)
        
        print(f"🌐 交互式可视化已保存到: {html_file}")
        print(f"   请在浏览器中打开 {html_file} 查看可视化结果")
        
    except Exception as e:
        print(f"⚠️  可视化生成失败: {e}")
        print("   但 JSONL 文件已成功保存")


def print_extraction_results(result, model_id, text_source):
    """Print extraction results in a formatted way."""
    print(f"Extracted {len(result.extractions)} entities from {len(result.text):,} characters")

    if result.extractions:
        print(f"\n📝 Found {len(result.extractions)} extraction(s):\n")
        
        # Group extractions by class
        extraction_counts = Counter(extraction.extraction_class for extraction in result.extractions)
        print("📊 Extraction Summary:")
        for class_name, count in extraction_counts.most_common():
            print(f"   {class_name}: {count}")
        print()
        
        # Show first few extractions
        for i, extraction in enumerate(result.extractions[:5], 1):
            print(f"Extraction {i}:")
            print(f"  Class: {extraction.extraction_class}")
            print(f"  Text: {extraction.extraction_text[:100]}{'...' if len(extraction.extraction_text) > 100 else ''}")
            print(f"  Attributes: {extraction.attributes}")
            if extraction.char_interval:
                print(f"  Position: {extraction.char_interval.start_pos}-{extraction.char_interval.end_pos}")
            print()
        
        if len(result.extractions) > 5:
            print(f"... and {len(result.extractions) - 5} more extractions")
    else:
        print("\n⚠️  No extractions found")

    print("✅ SUCCESS! Literary extraction completed")
    print(f"   Model: {model_id}")
    print(f"   Text source: {text_source}")
    print("   JSON mode: enabled")
    print("   Schema constraints: enabled")
    print("   Parallel processing: enabled")


# 示例调用函数
def run_example():
    """示例：运行 DOCX 文件提取"""
    try:
        print("🚀 Running DOCX extraction with qwen3:8b...")
        print("📄 File: /app/test_data/晋控创力产品介绍文字版.docx")
        print("-" * 50)
        
        # 使用专门的 DOCX 处理函数
        result = run_docx_extraction(
            model_id="qwen3:8b",
            temperature=0.1,
            docx_path="/app/test_data/晋控创力产品介绍文字版.docx"
        )
        
        # 打印结果
        print_extraction_results(result, "qwen3:8b", "docx")
        
        # 保存和可视化结果
        save_and_visualize_results(result, "qwen3:8b", 0.3, "docx")
        
        return True
        
    except ConnectionError as e:
        print(f"\n❌ ConnectionError: {e}")
        print("\n💡 Make sure Ollama is running:")
        print("   ollama serve")
        return False
    except ValueError as e:
        if "Can't find Ollama" in str(e):
            print(f"\n❌ Model not found: qwen3:8b")
            print("\n💡 Install the model first:")
            print("   ollama pull qwen3:8b")
        else:
            print(f"\n❌ ValueError: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    run_example()