from flask import Flask, request, jsonify
import yaml
import subprocess
import os
 
app = Flask(__name__)
CONFIG_FILE = '/root/hyst*******马赛克******eria2/config.yaml'
API_KEY = '123456789'
 
def read_config():
    with open(CONFIG_FILE, 'r') as file:
        return yaml.safe_load(file)
 
def write_config(config):
    with open(CONFIG_FILE, 'w') as file:
        yaml.safe_dump(config, file)
 
def restart_service(service_name):
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', service_name], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
 
def check_service_status(service_name):
    try:
        result = subprocess.run(['sudo', 'systemctl', 'is-active', service_name], check=True, stdout=subprocess.PIPE)
        if result.stdout.decode('utf-8').strip() == 'active':
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False
 
@app.route('/api', methods=['POST'])
def manage_user():
    # 验证API Key
    api_key = request.headers.get('Authorization')
    if api_key != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401
 
    # 解析请求数据
    data = request.json
    if not data or 'username' not in data or 'action' not in data:
        return jsonify({'error': 'Bad Request'}), 400
    
    username = data['username']
    action = data['action'].lower()
 
    # 读取配置文件
    config = read_config()
    userpass = config.get('auth', {}).get('userpass', {})
 
    service_name = 'hyst*******马赛克******eria2' # 服务名称
    need_restart = False
 
    if action == 'add':
        if 'password' not in data:
            return jsonify({'error': 'Missing password for add action'}), 400
        password = data['password']
        userpass[username] = password
        need_restart = True
    elif action == 'delete':
        if username in userpass:
            userpass.pop(username, None)
            need_restart = True
        else:
            return jsonify({'error': 'User not found'}), 404
    elif action == 'query':
        password = userpass.get(username)
        if password is not None:
            return jsonify({username: password})
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        return jsonify({'error': 'Invalid action'}), 400
 
    # 对于非查询动作，更新配置文件并重启服务
    if need_restart:
        config['auth']['userpass'] = userpass
        write_config(config)
        if restart_service(service_name):
            if check_service_status(service_name):
                return jsonify({'success': True, 'message': 'Service restarted and running'})
            else:
                return jsonify({'error': 'Service restarted but not running'}), 500
        else:
            return jsonify({'error': 'Failed to restart service'}), 500
 
    return jsonify({'success': True})
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
