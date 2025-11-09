"""
本地开发启动脚本
生产环境请使用 uvicorn 命令启动
"""
import sys
import uvicorn

if __name__ == '__main__':
    # 支持命令行参数：python run.py <host> <port>
    host = sys.argv[1] if len(sys.argv) > 1 else "0.0.0.0"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 80

    uvicorn.run(
        "wxcloudrun:app",
        host=host,
        port=port,
        reload=True,  # 开发环境启用热重载
        log_level="info"
    )
