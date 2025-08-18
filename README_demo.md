git clone https://github.com/google/langextract.git
cd langextract

docker build -t langextract .
# 长期运行容器用于 VSCode 调试
 <!-- 或者使用绝对路径 (Windows): -->
docker run -d --name langextract-dev  -e LANGEXTRACT_API_KEY="your-api-key"  -v D:\LiRan\VsPro\langextract:/workspace  -w /workspace  -p 22:22  langextract  tail -f /dev/null

 <!-- 或者使用交互式终端运行 -->
 或者使用绝对路径 (Windows):
 docker run -it --name langextract-interactive \
   -e LANGEXTRACT_API_KEY="your-api-key" \
   -v D:\LiRan\VsPro\langextract:/workspace \
   -w /workspace \
   langextract \
   /bin/bash



# 命令行进入一个已经运行的容器（如 langextract-dev）
docker exec -it ollama-ollama-1 /bin/bash
# 在 Linux 系统的命令行中，使用以下命令将 gemma2:2b 模型下载到 /root/.ollama 文件夹下（Ollama 会自动下载到该目录，无需手动指定）：
ollama pull gemma2:2b
# 启动本地 gemma2:2b 模型服务（Ollama 会自动拉取并加载模型）
ollama serve & ollama run gemma2:2b

# 创建名为 qwen3-no-thoughts.modelfile 的文件并写入内容
cat > qwen3-no-thoughts.modelfile << 'EOF'
FROM qwen3:8b
SYSTEM "你是一个高效的中文助手，直接输出最终答案，无需展示思考过程。"
EOF

# 创建模型并保存到默认路径
ollama create qwen3:8b-no-thoughts -f ~/models/qwen3-no-thoughts.modelfile