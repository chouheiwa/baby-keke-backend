# 多阶段构建 Spring Boot 应用
# 二开推荐阅读[如何提高项目构建效率](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/scene/build/speed.html)

# 第一阶段：构建阶段
# 使用 Maven 官方镜像进行构建
FROM maven:3.9.6-eclipse-temurin-21-alpine AS builder

# 设置工作目录
WORKDIR /build

# 复制 pom.xml 和源代码
COPY pom.xml .
COPY src ./src

# 使用腾讯云 Maven 镜像加速依赖下载
RUN mkdir -p /root/.m2 \
    && echo '<?xml version="1.0" encoding="UTF-8"?>\n\
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"\n\
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n\
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">\n\
  <mirrors>\n\
    <mirror>\n\
      <id>aliyun-maven</id>\n\
      <mirrorOf>central</mirrorOf>\n\
      <name>Aliyun Maven</name>\n\
      <url>https://maven.aliyun.com/repository/public</url>\n\
    </mirror>\n\
  </mirrors>\n\
</settings>' > /root/.m2/settings.xml

# 打包应用（跳过测试以加快构建速度）
RUN mvn clean package -DskipTests

# 第二阶段：运行阶段
# 使用轻量级 JRE 镜像
FROM eclipse-temurin:21-jre-alpine

# 容器默认时区为UTC，设置为上海时间
RUN apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo Asia/Shanghai > /etc/timezone \
    && apk del tzdata

# 使用 HTTPS 协议访问容器云调用证书安装
RUN apk add --no-cache ca-certificates

# 创建应用目录
WORKDIR /app

# 从构建阶段复制 JAR 文件
COPY --from=builder /build/target/*.jar app.jar

# 暴露端口
# 此处端口必须与「服务设置」-「流水线」以及「手动上传代码包」部署时填写的端口一致，否则会部署失败。
EXPOSE 80

# 设置 JVM 参数和 Spring Boot 配置
ENV JAVA_OPTS="-Xms256m -Xmx512m -XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"

# 执行启动命令
# 使用 --server.port=80 确保应用监听 80 端口
CMD ["sh", "-c", "java ${JAVA_OPTS} -Djava.security.egd=file:/dev/./urandom -jar app.jar --server.port=80"]
