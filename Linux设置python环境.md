设置Python环境

1. 更新系统

   ```bash
   sudo apt update -y
   ```

2. 安装Python3

   ```bash
   sudo apt install -y python3
   ```

3. 安装pip和虚拟环境

   ```bash
   sudo apt install -y python3-pip python3-venv
   ```

4. 设置软连接

   ```bash
   mkdir -p ~/.local/bin
   ln -sf `which python3` ~/.local/bin/python
   ln -sf `which pip3` ~/.local/bin/pip
   ```

5. 设置环境变量

   ```bash
   echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
   source ~/.bashrc
   ```

6. 验证

   1. 检查Python版本是否是Python3：`python --version`
   2. 检查pip使用的是否是Python3：``  head -1 `which pip`  ``

7. 安装ipython：`pip install ipython`

8. 安装后面课程需要的各种包

   ```bash
   # 数据库阶段
   pip install pymysql redis pymongo
   # Web阶段
   pip install tornado flask flask-sqlalchemy celery
   # Djngo
   pip install django==1.11.24 djangorestframework markdown django-filter
   # 爬虫阶段
   pip install requests lxml selenium bs4 scrapy
   ```

   