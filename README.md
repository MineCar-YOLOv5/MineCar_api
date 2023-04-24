# MineCar_api
环形矿场矿车目标检测后端 
##### 关于数据库：
项目database文件夹下有sql文件，导入数据库，修改settings.py 中的配置，无需迁移即可使用。

##### 直接运行版
1. linux 环境下
项目路径下：
```shell
# 安装python依赖
pip instll -r requirements.txt

# 制作项目的.spec文件
pyi-makespec -D manage.py

#打包
pyinstaller manage.spec 

cd dist/manage

#执行
nohup  ./manage runserver 0.0.0.0:8000 --noreload
```
2. windows环境下(建议使用anaconda集成环境)：
```shell
#创建集成环境
conda create -n MineCar python=3.6
#进入集成环境
conda activate MineCar
#cd至项目根目录下
cd MineCar_api
# 安装依赖
conda install -r requirements.txt
#运行项目
python manage.py runserver 
```
##### docker部署版（还存在bug，不建议使用）

```shell
docker build -t minecar_api:v1 . #打包镜像
```