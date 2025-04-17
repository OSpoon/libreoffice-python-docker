import os
import subprocess
import logging
from pathlib import Path


def setup_logging():
    """设置日志配置"""
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


logger = setup_logging()


class ConversionError(Exception):
    """转换错误异常类"""

    pass


def convert_to_pdf(input_file: str, output_dir: str, timeout: int = 300) -> bool:
    """转换文档到PDF"""
    # 验证输入文件
    input_path = Path(input_file).resolve()
    if not input_path.exists():
        error_msg = f"输入文件不存在: {input_path}"
        logger.error(error_msg)
        raise ConversionError(error_msg)

    # 验证输出目录
    output_path = Path(output_dir).resolve()
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        error_msg = f"创建输出目录失败: {output_path}, 错误: {str(e)}"
        logger.error(error_msg)
        raise ConversionError(error_msg)

    # 记录转换信息
    logger.info(f"开始转换文件: {input_path}")
    logger.info(f"输出目录: {output_path}")

    try:
        command = [
            os.environ.get("LIBREOFFICE_PATH"),
            "--headless",
            "--convert-to",
            "pdf:writer_pdf_Export",
            "--outdir",
            str(output_path),
            str(input_path),
        ]

        logger.info(f"执行转换命令: {' '.join(command)}")

        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=startupinfo,
        )

        try:
            stdout, stderr = process.communicate(timeout=timeout)
            stdout_str = stdout.decode(errors="ignore")
            stderr_str = stderr.decode(errors="ignore")

            # 记录进程输出
            if stdout_str:
                logger.info(f"标准输出: {stdout_str}")
            if stderr_str:
                logger.warning(f"错误输出: {stderr_str}")

            # 验证转换结果
            output_file = output_path / f"{input_path.stem}.pdf"
            if process.returncode == 0 and output_file.exists():
                logger.info(f"转换成功: {output_file}")
                return True

            error_msg = (
                f"转换失败，返回码: {process.returncode}\n"
                f"标准输出: {stdout_str}\n"
                f"错误输出: {stderr_str}"
            )
            logger.warning(error_msg)

        except subprocess.TimeoutExpired:
            process.kill()
            error_msg = f"转换超时 (>{timeout}秒)"
            logger.warning(error_msg)

    except Exception as e:
        error_msg = f"转换发生错误: {str(e)}"
        logger.error(error_msg, exc_info=True)

    raise ConversionError(error_msg)


if __name__ == "__main__":
    # 支持的文件扩展名
    SUPPORTED_EXTENSIONS = {
        ".doc",
        ".docx",  # Word文档
        ".ppt",
        ".pptx",  # PowerPoint演示文稿
        ".xls",
        ".xlsx",  # Excel表格
    }

    input_dir = Path("input")
    if not input_dir.exists():
        print("输入目录不存在，正在创建...")
        input_dir.mkdir(parents=True, exist_ok=True)

    # 获取所有支持的文件
    files = [
        str(f)
        for f in input_dir.glob("*.*")
        if f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files:
        print("未找到可转换的文件")
        exit(0)

    print(f"找到 {len(files)} 个文件待转换")

    for input_file in files:
        try:
            result = convert_to_pdf(input_file=input_file, output_dir="output")
            print(f"{input_file}: {'成功' if result else '失败'}")
        except ConversionError as e:
            print(f"{input_file}: 转换失败 - {str(e)}")
