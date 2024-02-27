# Hysteria2-panel
Hysteria2服务端管理面板
# 申请免费eu.org域名，并申请证书

# Hysteria2 安装
sudo mkdir /root/hysteria2
sudo cp config.yaml /root/hysteria2/
sudo cp hysteria-linux-amd64 /root/hysteria2/
sudo cp 1.crt /root/hysteria2/
sudo cp 1.key /root/hysteria2/
cd /root/hysteria2
sudo chmod +x hysteria-linux-amd64

cp  hysteria2.service /etc/systemd/system/

# 创建服务
===============================================
sudo vi /etc/systemd/system/hysteria2.service

[Unit]
Description=hysteria2 VPN Server
After=network.target

[Service]
Type=simple
ExecStart=/root/hysteria2/hysteria-linux-amd64 server -c /root/hysteria2/config.yaml
Restart=on-failure

[Install]
WantedBy=multi-user.target

===================================================

sudo systemctl daemon-reload
sudo systemctl enable hysteria2
sudo systemctl start hysteria2
sudo systemctl restart hysteria2
netstat -luntp |grep hysteria


sudo systemctl stop hysteria2
netstat -luntp |grep hysteria
# config.yaml 配置  可参考官方文档
'auth:
  type: userpass
  userpass:
    csdn: csdn
 
listen: :443
masquerade:
  proxy:
    rewriteHost: true
    url: https://www.bing.com/
  type: proxy
tls:
  cert: /root/hyst*****马赛克******eria2/csdn.crt
  key: /root/hyst*****马赛克******eria2/csdn.key'


# 启动面板 Python3 app.py 

