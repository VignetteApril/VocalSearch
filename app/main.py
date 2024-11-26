import os
from elasticsearch import Elasticsearch
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import gradio as gr
from gradio_pdf import PDF

# 固定存放文档的文件夹路径
DOCUMENT_FOLDER = "/app/documents"  # 请替换为实际主机上存放文档的路径

# 初始化 SenseVoice 模型
model_dir = "iic/SenseVoiceSmall"  # 替换为实际模型路径
model = AutoModel(
    model=model_dir,
    vad_model="fsmn-vad",
    vad_kwargs={"max_single_segment_time": 30000},
    device="cuda:0"  # 如果没有 GPU，可改为 "cpu"
)

# 初始化 Elasticsearch 客户端
es = Elasticsearch(hosts=["http://elasticsearch:9200"])  # 连接 Docker 中的 Elasticsearch 容器

# 索引文件夹中文件名
def index_files(folder_path=DOCUMENT_FOLDER, index_name="file_index"):
    """将指定文件夹及其子文件夹内的文件索引到 Elasticsearch"""
    if not os.path.exists(folder_path):
        gr.Warning("文档文件夹不存在，请检查！")
        raise gr.Error("索引失败：文档文件夹不存在！")

    # 创建索引（如果尚不存在）
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)

    # 遍历文件夹及其子文件夹
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                # 将文件的相对路径或绝对路径索引到 Elasticsearch
                doc = {
                    "file_name": file_name,
                    "file_path": file_path,
                    "relative_path": os.path.relpath(file_path, folder_path)  # 相对于根目录的路径
                }
                es.index(index=index_name, document=doc)
    gr.Info("文件及子文件夹索引成功！")

# 查询文件
def search_file(keyword, index_name="file_index"):
    """通过关键词在 Elasticsearch 中查询文件"""
    query = {
        "query": {
            "match": {
                "file_name": keyword
            }
        }
    }
    response = es.search(index=index_name, body=query, size=100)  # 最大返回 100 条
    hits = response['hits']['hits']

    # 提取文件路径并按 score 排序
    sorted_hits = sorted(hits, key=lambda x: x['_score'], reverse=True)  # 按得分从高到低排序
    unique_file_paths = []
    seen_paths = set()  # 用于去重

    for hit in sorted_hits:
        file_path = hit['_source']['file_path']
        if file_path not in seen_paths:
            unique_file_paths.append(file_path)
            seen_paths.add(file_path)

    return unique_file_paths if unique_file_paths else []


# 使用 SenseVoice 进行语音转文字
def audio_to_text(audio_file):
    """使用 SenseVoice 模型处理音频文件并转文字"""
    res = model.generate(
        input=audio_file,
        cache={},
        language="auto",  # 自动检测语言，可根据需求指定 "zh", "en", 等
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,
        merge_length_s=15
    )
    text = rich_transcription_postprocess(res[0]["text"])
    return text if text else "无法识别语音"

# 处理流程：语音转文字 -> 文件名检索
def process_audio_and_search(audio_file):
    """处理上传的语音文件，转文字后检索文件名"""
    # 语音转文字
    text = audio_to_text(audio_file)
    if text:
        gr.Info(f"语音转写：{text}")
        # 使用转文字结果进行文件检索
        file_paths = search_file(text)
        if file_paths:
            # 去重后取前 5 个文件路径
            unique_file_paths = file_paths[:5]
            gr.Info(f"成功找到 {len(file_paths)} 个匹配文件，展示前 5 个")
            # 如果少于 5 个，填充空字符串
            output_files = unique_file_paths + [""] * (5 - len(unique_file_paths))
        else:
            gr.Warning("未找到匹配文件，请检查关键词！")
            output_files = [""] * 5  # 全部为空
    else:
        gr.Error("语音识别失败，请检查语音文件！")
        output_files = [""] * 5  # 全部为空
    return output_files

# Gradio 界面
def main():
    with gr.Blocks() as demo:
        gr.Markdown("### 非实时语音转文字并检索文件名系统")

        with gr.Row():
            audio_input = gr.Audio(label="上传语音文件", type="filepath")  # 上传语音文件

        with gr.Row():
            # 固定展示 5 个文件输出框
            output_files = [gr.File(label=f"匹配文件 {i+1}") for i in range(5)]

        with gr.Row():
            btn_index = gr.Button("索引文件夹")
            btn_process = gr.Button("语音转文字并检索")

        # 绑定按钮事件
        btn_index.click(index_files)  # 索引固定文件夹
        btn_process.click(
            process_audio_and_search,
            inputs=[audio_input],
            outputs=output_files  # 绑定固定的 5 个文件组件
        )

        demo.launch(server_name="0.0.0.0", server_port=7860)  # 在 Docker 中运行需要设置 0.0.0.0 监听所有 IP

if __name__ == "__main__":
    main()

