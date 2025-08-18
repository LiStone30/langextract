#!/usr/bin/env python3
# Copyright 2025 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Quick-start example for using Ollama with langextract."""

import argparse
import os
import sys
import json

import langextract as lx


def run_extraction(model_id="qwen3:8b", temperature=0.3):
  """Run a simple extraction example using Ollama."""
  # input_text = "Isaac Asimov was a prolific science fiction writer."
  input_text = "晋控创力（山西晋控装备创力智能制造有限公司介绍）成立于2021年9月30日，注册地位于长治市经济技术开发区，注册资本10000万元。公司在煤矿机械领域积极探索智能化、绿色化转型，致力于推动煤机装备升级和制造模式创新。我们希望通过技术创新和工艺优化，提升煤机产品的智能化水平，同时降低能耗与排放，助力行业可持续发展。这一方向既符合国家推动制造业智能化、绿色化升级的政策要求，也是我们立足行业实际、稳步推进产业现代化的重要路径。公司以打造高端智能开采控制技术装备产品为主，研发、制造综采工作面液压支架电液控系统、智能化控制系统、集中供液系统、高端智能乳化液泵站，高端智能喷雾泵站。"
  

  # prompt = "Extract the author's full name and their primary literary genre."
  prompt = "提取出公司、产品的名称、用途、技术参数、使用方法、特点、优势等对公司和产品进行介绍的信息。"
  

  examples = [
      lx.data.ExampleData(
          text=(
              "山西云晟科技有限公司成立于2015年，坐落于有太行明珠之称的山西省晋城市，并先后在武汉市、西安市、长治市、临汾市、阳泉市成立子分公司。公司注册资金1000万。        云晟科技是国内解决工业行业实操培训的科技公司。公司致力于将AI+XR(VR、MR、APP等)高尖端技术应用于安全教育与培训领域，帮助企业和个人更高效、安全、真实的体验、学习。     "
          ),
          extractions=[
              lx.data.Extraction(
                  extraction_class="公司介绍",
                  extraction_text=(
                      "山西云晟科技有限公司成立于2015年，坐落于有太行明珠之称的山西省晋城市，并先后在武汉市、西安市、长治市、临汾市、阳泉市成立子分公司。公司注册资金1000万。        云晟科技是国内解决工业行业实操培训的科技公司。公司致力于将AI+XR(VR、MR、APP等)高尖端技术应用于安全教育与培训领域，帮助企业和个人更高效、安全、真实的体验、学习。     "
                  ),
                  attributes={
                      "name": "山西云晟科技有限公司",
                      "genre": "云晟科技是国内解决工业行业实操培训的科技公司",
                  },
              )
          ],
      )
  ]

  model_config = lx.factory.ModelConfig(
      model_id=model_id,
      provider_kwargs={
          "model_url": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
          "format_type": lx.data.FormatType.JSON,
          "temperature": temperature,
      },
  )

  result = lx.extract(
      text_or_documents=input_text,
      prompt_description=prompt,
      examples=examples,
      config=model_config,
      use_schema_constraints=True,
  )

  # Option 2: Pass model_id directly (simpler)
  # result = lx.extract(
  #     text_or_documents=input_text,
  #     prompt_description=prompt,
  #     examples=examples,
  #     model_id=model_id,
  #     model_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
  #     format_type=lx.data.FormatType.JSON,
  #     temperature=temperature,
  #     use_schema_constraints=True,
  # )

  return result


def save_and_visualize_results(result, model_id, temperature):
  """Save results to files and generate interactive visualization."""
  
  # 保存 JSON 结果到文件
  output_data = {
    "model_id": model_id,
    "temperature": temperature,
    "input_text": "Isaac Asimov was a prolific science fiction writer.",
    "extractions": []
  }
  
  for extraction in result.extractions:
    output_data["extractions"].append({
      "class": extraction.extraction_class,
      "text": extraction.extraction_text,
      "attributes": extraction.attributes,
      "char_interval": {
        "start": extraction.char_interval.start_pos if extraction.char_interval else None,
        "end": extraction.char_interval.end_pos if extraction.char_interval else None
      } if extraction.char_interval else None
    })
  
  # 保存到 JSON 文件
  output_file = f"extraction_result_{model_id.replace(':', '_')}.json"
  with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)
  
  print(f"💾 JSON 结果已保存到: {output_file}")
  
  # 保存为 JSONL 格式用于可视化
  jsonl_file = f"extraction_result_{model_id.replace(':', '_')}.jsonl"
  lx.io.save_annotated_documents([result], output_name=jsonl_file, output_dir=".")
  print(f"📊 JSONL 文件已保存到: {jsonl_file}")
  
  # 生成交互式可视化
  try:
    print("🎨 正在生成交互式可视化...")
    html_content = lx.visualize(jsonl_file)
    
    html_file = f"extraction_visualization_{model_id.replace(':', '_')}.html"
    with open(html_file, "w", encoding='utf-8') as f:
      if hasattr(html_content, 'data'):
        f.write(html_content.data)  # For Jupyter/Colab
      else:
        f.write(html_content)
    
    print(f"🌐 交互式可视化已保存到: {html_file}")
    print(f"   请在浏览器中打开 {html_file} 查看可视化结果")
    
  except Exception as e:
    print(f"⚠️  可视化生成失败: {e}")
    print("   但 JSON 和 JSONL 文件已成功保存")


def main():
  """Main function to run the quick-start example."""
  parser = argparse.ArgumentParser(
      description="Run Ollama extraction example",
      epilog=(
          "Supported models: qwen3:8b, gemma2:2b, llama3.2:1b, mistral:7b, qwen2.5:0.5b,"
          " etc."
      ),
  )
  parser.add_argument(
      "--model-id",
      default=os.getenv("MODEL_ID", "qwen3:8b"),
      help="Ollama model ID (default: qwen3:8b or MODEL_ID env var)",
  )
  parser.add_argument(
      "--temperature",
      type=float,
      default=float(os.getenv("TEMPERATURE", "0.3")),
      help="Model temperature (default: 0.3 or TEMPERATURE env var)",
  )
  parser.add_argument(
      "--visualize",
      action="store_true",
      help="Generate interactive HTML visualization",
  )
  args = parser.parse_args()

  print(f"🚀 Running Ollama quick-start example with {args.model_id}...")
  print("-" * 50)

  try:
    result = run_extraction(
        model_id=args.model_id, temperature=args.temperature
    )

    if result.extractions:
      print(f"\n📝 Found {len(result.extractions)} extraction(s):\n")
      for extraction in result.extractions:
        print(f"Class: {extraction.extraction_class}")
        print(f"Text: {extraction.extraction_text}")
        print(f"Attributes: {extraction.attributes}")
        print()
      
      # 保存结果并生成可视化
      if args.visualize:
        save_and_visualize_results(result, args.model_id, args.temperature)
      else:
        # 只保存 JSON 文件
        output_data = {
          "model_id": args.model_id,
          "temperature": args.temperature,
          "input_text": "Isaac Asimov was a prolific science fiction writer.",
          "extractions": []
        }
        
        for extraction in result.extractions:
          output_data["extractions"].append({
            "class": extraction.extraction_class,
            "text": extraction.extraction_text,
            "attributes": extraction.attributes,
            "char_interval": {
              "start": extraction.char_interval.start_pos if extraction.char_interval else None,
              "end": extraction.char_interval.end_pos if extraction.char_interval else None
            } if extraction.char_interval else None
          })
        
        output_file = f"extraction_result_{args.model_id.replace(':', '_')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
          json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 JSON 结果已保存到: {output_file}")
        print("💡 使用 --visualize 参数可以生成交互式 HTML 可视化")
      
    else:
      print("\n⚠️  No extractions found")

    print("✅ SUCCESS! Ollama is working with langextract")
    print(f"   Model: {args.model_id}")
    print("   JSON mode: enabled")
    print("   Schema constraints: enabled")
    return True

  except ConnectionError as e:
    print(f"\n❌ ConnectionError: {e}")
    print("\n💡 Make sure Ollama is running:")
    print("   ollama serve")
    return False
  except ValueError as e:
    if "Can't find Ollama" in str(e):
      print(f"\n❌ Model not found: {args.model_id}")
      print("\n💡 Install the model first:")
      print(f"   ollama pull {args.model_id}")
    else:
      print(f"\n❌ ValueError: {e}")
    return False
  except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    return False


if __name__ == "__main__":
  SUCCESS = main()
  sys.exit(0 if SUCCESS else 1)
