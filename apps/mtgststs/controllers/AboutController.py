#HOME
def top(render_params, data):
    render_params["body"] = data["body"]
    render_params["title"] = data["title"]
    return render_params