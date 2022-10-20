def error404(render_params, data):
    render_params["body"] = data["body"]
    render_params["title"] = "MTGSTATISTICS | " + data["title"]
    return render_params
