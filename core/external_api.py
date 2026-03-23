def send_context_to_external(context):
    """
    预留：未来给 OpenClaw / 云端模型 / 其他外部系统用
    现在先只返回上下文，不做真正调用
    """
    return {
        "ok": True,
        "message": "外部接口已预留，暂未接入真实实现",
        "context": context,
    }
