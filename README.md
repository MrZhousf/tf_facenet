# tf_facenet
facenet人脸检测与识别项目


### 说明
通过MTCNN人脸检测模型，从照片中提取人脸图像
把人脸图像输入到FaceNet，计算Embedding的特征向量
采用annoy进行人脸匹配，比较特征向量间的欧式距离
项目利用谷歌浏览器调用电脑摄像头进行人脸采集与识别业务

每次识别时间约240ms（MAC only cpu）。

### 依赖
1. tensorflow1.8
2. python2.7
3. flask
4. flask_sqlalchemy
5. annoy

### facenet
https://github.com/davidsandberg/facenet

### 模型下载
https://download.csdn.net/download/zsf442553199/10952495

### 项目运行步骤
1. 修改项目配置文件config_development.yml
2. 运行app.py
3. 人脸采集页面：http://127.0.0.1:8090/user/sign_in
4. 人脸识别页面：http://127.0.0.1:8090/user/sign_up

### 相关截图
以周杰伦为例，此处仅用于学习与研究，莫怪。
1. 人脸采集页面（谷歌浏览器打开）
![](https://github.com/MrZhousf/tf_facenet/blob/master/pic/1.png?raw=true)
2. 人脸识别页面（谷歌浏览器打开）
![](https://github.com/MrZhousf/tf_facenet/blob/master/pic/2.png?raw=true)