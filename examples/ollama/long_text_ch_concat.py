import langextract as lx
import textwrap
import os
from collections import Counter, defaultdict
import docx

# Define comprehensive prompt and examples for complex literary text
prompt = textwrap.dedent("""\
    提取出公司、产品的名称、用途、技术参数、使用方法、特点、优势等对公司和产品进行介绍的信息。
    提取出公司和产品的关系
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
        公司介绍
        晋控创力（山西晋控装备创力智能制造有限公司介绍）成立于2021年9月30日，注册地位于长治市经济技术开发区，注册资本10000万元。公司在煤矿机械领域积极探索智能化、绿色化转型，致力于推动煤机装备升级和制造模式创新。我们希望通过技术创新和工艺优化，提升煤机产品的智能化水平，同时降低能耗与排放，助力行业可持续发展。这一方向既符合国家推动制造业智能化、绿色化升级的政策要求，也是我们立足行业实际、稳步推进产业现代化的重要路径。公司以打造高端智能开采控制技术装备产品为主，研发、制造综采工作面液压支架电液控系统、智能化控制系统、集中供液系统、高端智能乳化液泵站，高端智能喷雾泵站。
        创新团队
        在智能化与绿色化转型的探索中，我们组建了一支由行业专家指导、中青年技术骨干为主体的研发团队。团队成员兼具专业理论知识和工程实践经验，在煤机装备升级、智能制造等领域持续开展技术创新与应用研究。这支充满活力的团队，正以务实的态度和开放的思维，稳步推进产品优化与工艺改进。在智能化升级与绿色化转型的实践中，我们的研发团队始终关注行业技术前沿，通过持续的技术积累和工程实践，在煤机装备智能化改造、节能降耗工艺优化等领域形成了特色技术优势。团队以市场需求为导向，结合行业发展趋势，为企业产品迭代和工艺改进提供技术支持，助力公司在细分领域稳步提升竞争力。我们的团队始终以技术创新为驱动，通过与高校、科研院所及行业伙伴的开放合作，持续探索煤机智能化和绿色化发展的可行路径。未来，我们将继续深耕专业领域，优化产品性能与生产工艺，为行业转型升级贡献务实解决方案。
        科研实力与成果
        在液压支架用阀、电液控系统、乳化液保障系统和矿山自动化系统领域拥有各种实用技术专利50余项，各类资质及报告证书300余项。公司已建成规模化智能液压控制系统生产基地，具备批量生产液压支架电液控系统、集中供液系统等核心产品的能力，在山西省智能矿山装备领域形成了具有竞争力的产业化规模。我们的研发制造体系覆盖智能电液控系统、集中供液系统、远程供液系统及综采自动化控制系统等产品系列，相关技术水平均达到业内领先地位。
        公司自主研发的综采工作面液压支架用阀、电液控系统、集中供液系统、远程供液系统、高端智能乳化液泵站、工作面智能化控制系统等智能开采控制技术装备，经过中国煤炭工业协会鉴定，技术水平已处于业内领先地位。
        公司致力于提高中国煤矿综采自动化水平、改善煤矿开采安全条件、提高生产效率，持续提高科技创新能力。工作面智能化控制系统等产能规模和技术创新，均居于业内前列。
        公司建有机加中心、装配中、检验中心、仓储中心、维修中心和无尘车间等现代化生产线。无尘车间设备完全按照工业级和军工级电子类产品的制造和检测标准，能够满足恒温、恒湿、防尘、防静电等高端电子产，品生产制造要求
        """),
        extractions=[
            lx.data.Extraction(
                extraction_class="company",
                extraction_text=(
                    """
                    晋控创力（山西晋控装备创力智能制造有限公司介绍）成立于2021年9月30日，注册地位于长治市经济技术开发区，注册资本10000万元。公司在煤矿机械领域积极探索智能化、绿色化转型，致力于推动煤机装备升级和制造模式创新。我们希望通过技术创新和工艺优化，提升煤机产品的智能化水平，同时降低能耗与排放，助力行业可持续发展。这一方向既符合国家推动制造业智能化、绿色化升级的政策要求，也是我们立足行业实际、稳步推进产业现代化的重要路径。公司以打造高端智能开采控制技术装备产品为主，研发、制造综采工作面液压支架电液控系统、智能化控制系统、集中供液系统、高端智能乳化液泵站，高端智能喷雾泵站。
                    创新团队
                    在智能化与绿色化转型的探索中，我们组建了一支由行业专家指导、中青年技术骨干为主体的研发团队。团队成员兼具专业理论知识和工程实践经验，在煤机装备升级、智能制造等领域持续开展技术创新与应用研究。这支充满活力的团队，正以务实的态度和开放的思维，稳步推进产品优化与工艺改进。在智能化升级与绿色化转型的实践中，我们的研发团队始终关注行业技术前沿，通过持续的技术积累和工程实践，在煤机装备智能化改造、节能降耗工艺优化等领域形成了特色技术优势。团队以市场需求为导向，结合行业发展趋势，为企业产品迭代和工艺改进提供技术支持，助力公司在细分领域稳步提升竞争力。我们的团队始终以技术创新为驱动，通过与高校、科研院所及行业伙伴的开放合作，持续探索煤机智能化和绿色化发展的可行路径。未来，我们将继续深耕专业领域，优化产品性能与生产工艺，为行业转型升级贡献务实解决方案。
                    科研实力与成果
                    在液压支架用阀、电液控系统、乳化液保障系统和矿山自动化系统领域拥有各种实用技术专利50余项，各类资质及报告证书300余项。公司已建成规模化智能液压控制系统生产基地，具备批量生产液压支架电液控系统、集中供液系统等核心产品的能力，在山西省智能矿山装备领域形成了具有竞争力的产业化规模。我们的研发制造体系覆盖智能电液控系统、集中供液系统、远程供液系统及综采自动化控制系统等产品系列，相关技术水平均达到业内领先地位。
                    公司自主研发的综采工作面液压支架用阀、电液控系统、集中供液系统、远程供液系统、高端智能乳化液泵站、工作面智能化控制系统等智能开采控制技术装备，经过中国煤炭工业协会鉴定，技术水平已处于业内领先地位。
                    公司致力于提高中国煤矿综采自动化水平、改善煤矿开采安全条件、提高生产效率，持续提高科技创新能力。工作面智能化控制系统等产能规模和技术创新，均居于业内前列。
                    公司建有机加中心、装配中、检验中心、仓储中心、维修中心和无尘车间等现代化生产线。无尘车间设备完全按照工业级和军工级电子类产品的制造和检测标准，能够满足恒温、恒湿、防尘、防静电等高端电子产，品生产制造要求
                    """
                ),
                attributes={
                    "establishment_date": "2021年9月30日",
                    "location": "长治市经济技术开发区",
                    "registered_capital": "10000万元",
                    "industry": "煤矿机械",
                    "focus": "智能化、绿色化转型",
                    "mission": "推动煤机装备升级和制造模式创新",
                    "technological_goals": "提升煤机产品的智能化水平，降低能耗与排放，助力行业可持续发展",
                    "policy_alignment": "符合国家推动制造业智能化、绿色化升级的政策要求",
                    "strategic_path": "立足行业实际、稳步推进产业现代化",
                    "core_products": "高端智能开采控制技术装备",
                    "product_list": [
                        "综采工作面液压支架电液控系统",
                        "智能化控制系统",
                        "集中供液系统",
                        "高端智能乳化液泵站",
                        "高端智能喷雾泵站"
                        ],
                    "research_team": "由行业专家指导、中青年技术骨干为主体的研发团队",
                    "team_features": "兼具专业理论知识和工程实践经验，持续开展技术创新与应用研究",
                    "team_objectives": "以市场需求为导向，结合行业发展趋势，为企业产品迭代和工艺改进提供技术支持",
                    "technological_advantages": "在煤机装备智能化改造、节能降耗工艺优化等领域形成了特色技术优势",
                    "collaboration": "与高校、科研院所及行业伙伴的开放合作",
                    "future_goals": "继续深耕专业领域，优化产品性能与生产工艺，为行业转型升级贡献务实解决方案",
                    "patents": "50余项实用技术专利",
                    "certifications": "300余项资质及报告证书",
                    "production_capacity": "规模化智能液压控制系统生产基地，具备批量生产液压支架电液控系统、集中供液系统等核心产品的能力",
                    "industrial_scale": "在山西省智能矿山装备领域形成具有竞争力的产业化规模",
                    "product_series": "智能电液控系统、集中供液系统、远程供液系统及综采自动化控制系统",
                    "technical_leadership": "相关技术水平均达到业内领先地位",
                    "self_researched_products": "综采工作面液压支架用阀、电液控系统、集中供液系统、远程供液系统、高端智能乳化液泵站、工作面智能化控制系统等智能开采控制技术装备",
                    "technical_certification": "经过中国煤炭工业协会鉴定，技术水平处于业内领先地位",
                    "company_mission": "提高中国煤矿综采自动化水平、改善煤矿开采安全条件、提高生产效率",
                    "innovation_capacity": "持续提高科技创新能力",
                    "capacity_leadership": "工作面智能化控制系统等产能规模和技术创新均居于业内前列",
                    "production_facilities": "机加中心、装配中、检验中心、仓储中心、维修中心和无尘车间等现代化生产线",
                    "clean_room_standards": "无尘车间设备按照工业级和军工级电子类产品的制造和检测标准，满足恒温、恒湿、防尘、防静电等高端电子产，品生产制造要求",
                }
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="公司以打造高端智能开采控制技术装备产品为主，研发、制造综采工作面液压支架电液控系统、智能化控制系统、集中供液系统、高端智能乳化液泵站，高端智能喷雾泵站。",
                attributes={"type": "研发与制造", "company_name": "山西晋控装备创力智能制造有限公司（简称晋控创力）", "product_name": "综采工作面液压支架电液控系统"}
            ),
            lx.data.Extraction(
                extraction_class="relationship",
                extraction_text="公司以打造高端智能开采控制技术装备产品为主，研发、制造综采工作面液压支架电液控系统、智能化控制系统、集中供液系统、高端智能乳化液泵站，高端智能喷雾泵站。",
                attributes={"type": "研发与制造", "company_name": "山西晋控装备创力智能制造有限公司（简称晋控创力）", "product_name": "智能化控制系统"}
            ),
        ]
    ),
    lx.data.ExampleData(
        text=textwrap.dedent("""\
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
            """),
        extractions=[
            lx.data.Extraction(
                extraction_class="product",
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
        ]
    ),
    lx.data.ExampleData(
        text=textwrap.dedent("""\
            XR 煤矿 十大工种技能培训系统;十大工种分别是：煤矿安全监测监控作业安全技术实际操作考试标准、煤矿采煤机操作作业安全技术实际操作考试标准、煤矿防突作业安全技术实际操作考试标准、煤矿井下爆破作业安全技术实际操作考试标准、煤矿井下电气作业安全技术实际操作考试标准、煤矿掘进机操作作业安全技术实际操作考试标准、煤矿探放水作业安全技术实际操作考试标准、煤矿提升机操作作业安全技术实际操作考试标准、煤矿瓦斯抽查作业安全技术实际操作考试标准、煤矿瓦斯检查作业安全技术实际操作考试标准	
            系统介绍：十大工种技能培训系统的教学及考核内容依据《中华人民共和国安全生产法》、《煤矿安全规程》、《特种作业人员安全技术培训考核管理规定》等法律、法规和标准制定。
            此系统通过虚拟现实技术，让学员成为教学环节的参与者，使理论学习与实际操作可同时进行。以减少教学环节，降低企业培训成本为目的，不需要传统的教学模式，多位学员可同时进行操作练习和考核。解决教师的工作负担、提高学习效率。其优点在于教学场地占用小,内容生动丰富，教学效果明显等。可为煤矿企业大幅降低培训成本,零风险培训,提高煤炭操作岗位实操教学质量,最终实现员工高素质快速入岗。
            """),
        extractions=[
            lx.data.Extraction(
                extraction_class="product",
                extraction_text=(
                    """
                    XR 煤矿 十大工种技能培训系统;
                    """
                ),
                attributes={
                    "product_name": "XR 煤矿 十大工种 技能培训系统",
                    "product_content": "十大工种分别是：煤矿安全监测监控作业安全技术实际操作考试标准、煤矿采煤机操作作业安全技术实际操作考试标准、煤矿防突作业安全技术实际操作考试标准、煤矿井下爆破作业安全技术实际操作考试标准、煤矿井下电气作业安全技术实际操作考试标准、煤矿掘进机操作作业安全技术实际操作考试标准、煤矿探放水作业安全技术实际操作考试标准、煤矿提升机操作作业安全技术实际操作考试标准、煤矿瓦斯抽查作业安全技术实际操作考试标准、煤矿瓦斯检查作业安全技术实际操作考试标准",
                    "reference_standards": "《中华人民共和国安全生产法》、《煤矿安全规程》、《特种作业人员安全技术培训考核管理规定》等法律、法规和标准",
                    "product_features": "学员参与教学环节，理论学习与实际操作可同时进行；多位学员可同时进行操作练习和考核，无需传统教学模式",
                    "product_advantages": "减少教学环节，降低企业培训成本；减轻教师工作负担，提高学习效率；教学场地占用小，内容生动丰富，教学效果明显；实现晋控创力产品介绍文字版零风险培训，提高煤炭操作岗位实操教学质量，助力员工高素质快速入岗"
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
        save_and_visualize_results(result, "qwen3:8b", 0.3, "docx", "/app/test_data/晋控创力产品介绍文字版.docx")
        
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