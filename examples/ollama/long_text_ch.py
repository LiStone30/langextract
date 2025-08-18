import langextract as lx
import textwrap
import os
from collections import Counter, defaultdict
import docx

# Define comprehensive prompt and examples for complex literary text
prompt = textwrap.dedent("""\
    从给定的文本中提取公司、产品和关系信息。

    为每个实体提供有意义的属性，以增加上下文和深度。

    重要提示：
    1. 使用输入中的精确文本进行提取
    2. 按出现顺序提取实体，没有重叠的文本跨度
    3. 确保JSON格式完全正确，包含所有必要的逗号、引号和闭合括号
    4. 所有中文字符都要用英文双引号包围（使用 " 而不是 "）
    5. 每个属性值都要用英文双引号包围
    6. 确保JSON结构完整，不要截断
    7. 使用英文键名（company, product）而不是中文
    8. 特别注意：文本中的中文引号要转换为英文引号
    9. 避免引号嵌套问题，确保每个字符串都正确闭合
    """)

examples = [
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            创力（山西晋控装备创力智能制造有限公司介绍）成立于2021年9月30日，注册地位于长治市经济技术开发区，注册资本10000万元。公司在煤矿机械领域积极探索智能化、绿色化转型，致力于推动煤机装备升级和制造模式创新。我们希望通过技术创新和工艺优化，提升煤机产品的智能化水平，同时降低能耗与排放，助力行业可持续发展。这一方向既符合国家推动制造业智能化、绿色化升级的政策要求，也是我们立足行业实际、稳步推进产业现代化的重要路径。公司以打造高端智能开采控制技术装备产品为主，研发、制造综采工作面液压支架电液控系统、智能化控制系统、集中供液系统、高端智能乳化液泵站，高端智能喷雾泵站。
            FHDA1.6/31.5X电磁先导阀
            本电磁先导阀是由两组电磁铁驱动的二位三通换向阀组成的。本阀具有体积小、性能可靠、能耗低、维修方便等优点，本阀可单独使用或和电液控换向阀配套使用。
            结构:卧式
            公称压力:31.5MPa
            公称通径:1.6mm  
            额定工作电压: DC12V
            工作电流:≤120mA
            电器接头:M12(圆头)
            外形尺寸:155mm×84mm×40mm
            特点：结构简单、可靠、可维护性强， 可自动控制或手动控制。
            """),
        extractions=[
            lx.data.Extraction(
                extraction_class="company",
                extraction_text="山西晋控装备创力智能制造有限公司",
                attributes={
                    "genre": "工业行业实操培训的科技公司",
                    "establishment_date": "2021年9月30日",
                    "location": "长治市经济技术开发区",
                    "capital": "10000万元",
                    "industry": "煤矿机械",
                    "development_direction": "智能化、绿色化转型，推动煤机装备升级和制造模式创新",
                    "core_goal": "提升煤机产品的智能化水平，降低能耗与排放，助力行业可持续发展",
                    "main_business": "研发、制造综采工作面液压支架电液控系统、智能化控制系统、集中供液系统、高端智能乳化液泵站、高端智能喷雾泵站"
                }
            ),
            lx.data.Extraction(
                extraction_class="product",
                extraction_text="FHDA1.6/31.5X电磁先导阀",
                attributes={
                    "product_name": "FHDA1.6/31.5X电磁先导阀",
                    "composition": "由两组电磁铁驱动的二位三通换向阀组成",
                    "structure": "卧式",
                    "nominal_pressure": "31.5MPa",
                    "nominal_diameter": "1.6mm",
                    "rated_working_voltage": "DC12V",
                    "working_current": "≤120mA",
                    "electrical_connector": "M12(圆头)",
                    "overall_dimensions": "155mm×84mm×40mm",
                    "advantages": "体积小、性能可靠、能耗低、维修方便",
                    "features": "结构简单、可靠、可维护性强，可自动控制或手动控制",
                    "application": "可单独使用或和电液控换向阀配套使用"
                }
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="山西晋控装备创力智能制造有限公司制造FHDA1.6/31.5X电磁先导阀",
                attributes={"type": "制造", "company": "山西晋控装备创力智能制造有限公司", "product": "FHDA1.6/31.5X电磁先导阀"}
            ),
            
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
        
        # 使用更简单的配置重试
        simple_model_config = lx.factory.ModelConfig(
            model_id=model_id,
            provider_kwargs={
                "model_url": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
                "format_type": lx.data.FormatType.JSON,
                "temperature": 0.05,  # 非常低的温度
            },
        )
        
        # 简化的提示词
        simple_prompt = """从文本中提取公司信息，按以下JSON格式输出：
            {
            "extractions": [
                {
                "company": "公司名称",
                "company_attributes": {
                    "name": "公司名称",
                    "industry": "行业"
                }
                }
            ]
            }"""
        
        result = lx.extract(
            text_or_documents=text_content,
            prompt_description=simple_prompt,
            examples=examples,
            config=simple_model_config,
            use_schema_constraints=True,
            extraction_passes=1,      # 单次提取
            max_workers=5,            # 更少的并发
            max_char_buffer=300       # 更小的缓冲区
        )
        
        return result


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