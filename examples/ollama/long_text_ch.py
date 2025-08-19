import langextract as lx
import textwrap
import os
from collections import Counter, defaultdict
import docx

# Define comprehensive prompt and examples for complex literary text
prompt = textwrap.dedent("""\
    提取出公司、产品的名称、用途、技术参数、使用方法、特点、优势等对公司和产品进行介绍的信息。
    从原文中为每个实体提供有意义的属性，以增加上下文和深度。
    同类实体由于其描述文本的不同，属性类可以不完全相同，一些属性只有某个类有，提取属性需要基于原文本。同类实体中，意义相似的属性类，需要同名规范化。
    """)
    # 重要要求：
    # 1. 必须包含 "extractions" 键，且必须是数组
    # 2. 所有字符串值必须用英文双引号包围
    # 3. 确保JSON结构完整，不要截断
    # 4. 避免在字符串中使用中文引号，统一使用英文双引号
    # 5. 每个属性值都要正确闭合引号
    # 6. 确保JSON格式完全正确，包含所有必要的逗号、引号和闭合括号


examples = [
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            晋控创力（山西晋控装备创力智能制造有限公司介绍）成立于2021年9月30日，注册地位于长治市经济技术开发区，注册资本10000万元。
            FHJ12矿用本安型键盘为矿用本安型，适用于煤矿  井下，通过按键输入指令并发送给控制器执行相应功能 ,能让工作人员在安全区域控制和操作控制器。
            工作电压： DC12V
            工作电流： ≤50mA
            传输方式： RS485
            传输速率： 115.2Kbps
            接口数量： 1路
            最大传输距离： 10m
            防爆标志：Exib I Mb
            外形尺寸： 185mmX82mmX30mm
            特点：防护等级IP68，适用于放顶煤 支架，方便放煤的操作
            XR 煤矿 十大工种技能培训系统;十大工种分别是：煤矿安全监测监控作业安全技术实际操作考试标准、煤矿采煤机操作作业安全技术实际操作考试标准、煤矿防突作业安全技术实际操作考试标准、煤矿井下爆破作业安全技术实际操作考试标准、煤矿井下电气作业安全技术实际操作考试标准、煤矿掘进机操作作业安全技术实际操作考试标准、煤矿探放水作业安全技术实际操作考试标准、煤矿提升机操作作业安全技术实际操作考试标准、煤矿瓦斯抽查作业安全技术实际操作考试标准、煤矿瓦斯检查作业安全技术实际操作考试标准	
            系统介绍：十大工种技能培训系统的教学及考核内容依据《中华人民共和国安全生产法》、《煤矿安全规程》、《特种作业人员安全技术培训考核管理规定》等法律、法规和标准制定。
            此系统通过虚拟现实技术，让学员成为教学环节的参与者，使理论学习与实际操作可同时进行。以减少教学环节，降低企业培训成本为目的，不需要传统的教学模式，多位学员可同时进行操作练习和考核。解决教师的工作负担、提高学习效率。其优点在于教学场地占用小,内容生动丰富，教学效果明显等。可为煤矿企业大幅降低培训成本,零风险培训,提高煤炭操作岗位实操教学质量,最终实现员工高素质快速入岗。
            """),
        extractions=[
            # lx.data.Extraction(
            #       extraction_class="公司介绍",
            #       extraction_text=(
            #           "山西云晟科技有限公司成立于2015年，坐落于有太行明珠之称的山西省晋城市，并先后在武汉市、西安市、长治市、临汾市、阳泉市成立子分公司。公司注册资金1000万。        云晟科技是国内解决工业行业实操培训的科技公司。公司致力于将AI+XR(VR、MR、APP等)高尖端技术应用于安全教育与培训领域，帮助企业和个人更高效、安全、真实的体验、学习。     "
            #       ),
            #       attributes={
            #           "name": "山西云晟科技有限公司",
            #           "genre": "云晟科技是国内解决工业行业实操培训的科技公司",
            #       },
            # ),
            lx.data.Extraction(
                extraction_class="产品",
                extraction_text=(
                    """
                    FHJ12矿用本安型键盘为矿用本安型，适用于煤矿  井下，通过按键输入指令并发送给控制器执行相应功能 ,能让工作人员在安全区域控制和操作控制器。
                    工作电压： DC12V
                    工作电流： ≤50mA
                    传输方式： RS485
                    传输速率： 115.2Kbps
                    接口数量： 1路
                    最大传输距离： 10m
                    防爆标志：Exib I Mb
                    外形尺寸： 185mmX82mmX30mm
                    特点：防护等级IP68，适用于放顶煤 支架，方便放煤的操作
                    """
                ),
                attributes={
                    "product_name": "FHJ12矿用本安型键盘",
                    "type": "矿用本安型",
                    "usage": "通过按键输入指令并发送给控制器执行相应功能，能让工作人员在安全区域控制和操作控制器",
                    "working_voltage": "DC12V",
                    "working_current": "≤50mA",
                    "transmission_method": "RS485",
                    "transmission_rate": "115.2Kbps",
                    "interface_count": "1路",
                    "max_transmission_distance": "10m",
                    "explosion_proof_mark": "Exib I Mb",
                    "dimensions": "185mmX82mmX30mm",
                    "features": "防护等级IP68，适用于放顶煤支架，方便放煤的操作"
                },
            ),
            lx.data.Extraction(
                extraction_class="公司",
                extraction_text=(
                    """
                    晋控创力（山西晋控装备创力智能制造有限公司介绍）成立于2021年9月30日，注册地位于长治市经济技术开发区，注册资本10000万元。
                    """
                ),
                attributes={
                    "establishment_date": "2021年9月30日",
                    "location": "长治市经济技术开发区",
                    "registered_capital": "10000万元",
                }
            ),
            lx.data.Extraction(
                extraction_class="产品",
                extraction_text=(
                    """
                    XR 煤矿 十大工种技能培训系统;十大工种分别是：煤矿安全监测监控作业安全技术实际操作考试标准、煤矿采煤机操作作业安全技术实际操作考试标准、煤矿防突作业安全技术实际操作考试标准、煤矿井下爆破作业安全技术实际操作考试标准、煤矿井下电气作业安全技术实际操作考试标准、煤矿掘进机操作作业安全技术实际操作考试标准、煤矿探放水作业安全技术实际操作考试标准、煤矿提升机操作作业安全技术实际操作考试标准、煤矿瓦斯抽查作业安全技术实际操作考试标准、煤矿瓦斯检查作业安全技术实际操作考试标准	
                    系统介绍：十大工种技能培训系统的教学及考核内容依据《中华人民共和国安全生产法》、《煤矿安全规程》、《特种作业人员安全技术培训考核管理规定》等法律、法规和标准制定。
                    此系统通过虚拟现实技术，让学员成为教学环节的参与者，使理论学习与实际操作可同时进行。以减少教学环节，降低企业培训成本为目的，不需要传统的教学模式，多位学员可同时进行操作练习和考核。解决教师的工作负担、提高学习效率。其优点在于教学场地占用小,内容生动丰富，教学效果明显等。可为煤矿企业大幅降低培训成本,零风险培训,提高煤炭操作岗位实操教学质量,最终实现员工高素质快速入岗。
                    """
                ),
                attributes={
                    "product_name": "XR 煤矿 十大工种 技能培训系统",
                    "product_content": "十大工种分别是：煤矿安全监测监控作业安全技术实际操作考试标准、煤矿采煤机操作作业安全技术实际操作考试标准、煤矿防突作业安全技术实际操作考试标准、煤矿井下爆破作业安全技术实际操作考试标准、煤矿井下电气作业安全技术实际操作考试标准、煤矿掘进机操作作业安全技术实际操作考试标准、煤矿探放水作业安全技术实际操作考试标准、煤矿提升机操作作业安全技术实际操作考试标准、煤矿瓦斯抽查作业安全技术实际操作考试标准、煤矿瓦斯检查作业安全技术实际操作考试标准",
                    "reference_standards": "《中华人民共和国安全生产法》、《煤矿安全规程》、《特种作业人员安全技术培训考核管理规定》等法律、法规和标准",
                    "product_features": "学员参与教学环节，理论学习与实际操作可同时进行；多位学员可同时进行操作练习和考核，无需传统教学模式",
                    "product_advantages": "减少教学环节，降低企业培训成本；减轻教师工作负担，提高学习效率；教学场地占用小，内容生动丰富，教学效果明显；实现AI数字人零风险培训，提高煤炭操作岗位实操教学质量，助力员工高素质快速入岗"
                },
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
    """标准化引号，将所有双引号替换为下划线"""
    # 将所有类型的双引号替换为下划线
    quote_mapping = {
        '"': '_',  # 中文双引号左 -> 下划线
        '"': '_',  # 中文双引号右 -> 下划线
        '"': '_',  # 英文双引号 -> 下划线
        ''': '_',  # 中文单引号左 -> 下划线
        ''': '_',  # 中文单引号右 -> 下划线
        "'": '_',  # 英文单引号 -> 下划线
    }
    
    for quote, underscore in quote_mapping.items():
        text = text.replace(quote, underscore)
    
    return text


def run_docx_extraction(model_id="qwen3:8b", temperature=0.3, docx_path="/app/test_data/AI数字人.docx"):
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
        docx_path = "/app/test_data/AI数字人.docx"
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


def save_and_visualize_results(result, model_id, temperature, text_source, docx_path=None):
    """Save results to files and generate interactive visualization."""
    
    # 从文档路径中提取文档名称
    if docx_path and os.path.exists(docx_path):
        # 从完整路径中提取文件名（不含扩展名）
        doc_name = os.path.splitext(os.path.basename(docx_path))[0]
    else:
        # 如果没有文档路径，使用text_source作为文档名称
        doc_name = text_source
    
    # 清理文档名称，移除特殊字符
    doc_name = doc_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    
    # 清理模型ID，移除冒号
    clean_model_id = model_id.replace(':', '_')
    
    # 生成文件名：{文档名称}_{模型ID}
    base_filename = f"{doc_name}_{clean_model_id}"
    
    # Save as JSONL format for visualization
    jsonl_file = f"{base_filename}.jsonl"
    lx.io.save_annotated_documents([result], output_name=jsonl_file, output_dir=".")
    print(f"📊 JSONL 文件已保存到: {jsonl_file}")
    
    # Generate the interactive visualization
    try:
        print("🎨 正在生成交互式可视化...")
        html_content = lx.visualize(jsonl_file)
        
        html_file = f"{base_filename}_visualization.html"
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
        print("📄 File: /app/test_data/AI数字人.docx")
        print("-" * 50)
        
        # 使用专门的 DOCX 处理函数
        result = run_docx_extraction(
            model_id="qwen3:8b",
            temperature=0.1,
            docx_path="/app/test_data/AI数字人.docx"
        )
        
        # 打印结果
        print_extraction_results(result, "qwen3:8b", "docx")
        
        # 保存和可视化结果
        save_and_visualize_results(result, "qwen3:8b", 0.3, "docx", "/app/test_data/AI数字人.docx")
        
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