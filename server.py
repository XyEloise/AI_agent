from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/agent-response', methods=['POST'])
def agent_response():
    # 处理 agent 的请求
    data = request.get_json()  # 假设代理发送的是 JSON 数据
    response = {
        "status": "success",
        "data": f"Received the request: {data}"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # 使用临时的 HTTPS 证书
