# medanalytics
为流行病学调查设计的无代码机器学习系统。本代码只包含后段Python处理数据的核心部分

## installation
1. FastAPI
2. Uvicorn等ASGI服务器
3. Gunicorn（备选）
4. Pandas, Numpy, Scipy, Scikit-learn等Python机器学习库
5. glmnet，用于lasso-logistic回归

## 运行
可以用Uvicorn直接运行，或是用Gunicorn启用多个进程，每一个进程挂在一个Uvicorn的ASGI服务。具体参见相关文档。
