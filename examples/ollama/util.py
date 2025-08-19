import json
import os

def split_jsonl_to_json_files(jsonl_path, output_dir):
    """
    将一个jsonl文件拆分为多个json文件，每一行一个json文件。
    :param jsonl_path: 输入的jsonl文件路径
    :param output_dir: 输出json文件的文件夹
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"第{idx}行不是合法的JSON格式，跳过。错误信息: {e}")
                continue
            output_path = os.path.join(output_dir, f"{idx}.json")
            with open(output_path, 'w', encoding='utf-8') as out_f:
                json.dump(data, out_f, ensure_ascii=False, indent=2)
    print(f"已将 {jsonl_path} 拆分为 {idx} 个json文件，保存在 {output_dir} 目录下。")


if __name__ == "__main__":
    split_jsonl_to_json_files("/app/晋控创力产品介绍文字版_qwen3_8b.jsonl", "temp_out_json")