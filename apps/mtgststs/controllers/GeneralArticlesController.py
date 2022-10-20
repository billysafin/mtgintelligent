#General News
import services.MtgReadingAllService as ReadingAll
import services.MtgReadingJpService as ReadingJp
import services.MtgReadingEnService as ReadingEn
import services.SitesService as Sites
import services.CountryService as Country
from Main import utils
from flask import request

#最新一覧
def top(render_params, data):
    #全言語記事
    news = []
    latest_all = ReadingAll.latest(16, 0)
    for u in latest_all:
        news.append({
            "prefix"        :u.flag_prefix,
            "published"     :u.published,
            "title"         :u.title,
            "link"          :u.link,
            "date"          :u.date,
            "source_from"   :u.site_name,
            "image"         :u.image
        })

    #日本語
    news_jp = []
    latest_jp = ReadingJp.latest(16)
    for u in latest_jp:
        news_jp.append({
            "prefix"        :u.flag_prefix,
            "published"     :u.published,
            "title"         :u.title,
            "link"          :u.link,
            "date"          :u.date,
            "source_from"   :u.site_name,
            "image"         :u.image
        })

    #英語
    news_en = []
    latest_en = ReadingEn.latest(16)
    for u in latest_en:
        news_en.append({
            "prefix"        :u.flag_prefix,
            "published"     :u.published,
            "title"         :u.title,
            "link"          :u.link,
            "date"          :u.date,
            "source_from"   :u.site_name,
            "image"         :u.image
        })

    if request.args.get('lang'):
        render_params["active_tab"] = request.args.get('lang')
    else:
        render_params["active_tab"] = "all"


    render_params["news"]        = news
    render_params["news_jp"]     = news_jp
    render_params["news_en"]     = news_en
    render_params["body"]        = data["body"]
    render_params["title"]       = data["title"]
    render_params["include_css"] = [
        {"css": "general-articles.css"}
    ]
    return render_params

#過去記事
def past_list(render_params, data):
    offset = 0

    if request.form.get("view_per_page_selected"):
        per_page = int(request.form.get("view_per_page_selected"))
    else:
        per_page = 25

    if request.args.get("page"):
        if int(request.args.get("page")) > 1:
            offset = per_page * int(request.args.get("page"))

    #検索用 サイト
    sites = []
    sites_result = Sites.all_sites()
    for u in sites_result:
        sites.append({
            "id"            : u.id,
            "name"          : u.site_name,
            "country_id"    : u.country_id
        })
    #検索用 言語
    langs = []
    langs_result = Country.all_country()
    for u in langs_result:
        langs.append({
            "id"    : u.id,
            "name"  : u.name_en
        })

    #検索分岐
    news = []
    if request.args.get("sub"):
        #言語
        lang_query = []
        lang_str = ''
        if request.form.getlist("lang"):
            lang_query = request.form.getlist("lang")
            lang_str = "&la=" + ",".join(map(str, lang_query))
        elif request.args.get("la"):
            lang_query = request.args.get("la").split(',')
            lang_str = "&la=" + request.args.get("la")
            
        #date
        date_query = {}
        f = ''
        t = ''
        if request.form.get("date_from"):
            date_query["date_from"] = request.form.get("date_from")
            f = "&f=" + request.form.get("date_from")
        elif request.args.get("f"):
            date_query["date_from"] = request.args.get("f")
            f = "&f=" + request.args.get("f")
        if request.form.get("date_to"):
            date_query["date_to"] = request.form.get("date_to")
            t = "&t=" + request.form.get("date_to")
        elif request.args.get("t"):
            date_query["date_to"] = request.args.get("t")
            t = "&t=" + request.args.get("t")

        #site
        sites_query = []
        sites_str = ''
        
        if request.form.getlist("sites"):
            sites_query = request.form.getlist("sites")
            sites_str = "&si=" + ",".join(map(str, sites_query))
        elif request.args.get("si"):
            sites_query = request.args.get("si").split(',')
            sites_str = "&si=" + request.args.get("si")
        
        result = ReadingAll.search(lang_query, date_query, sites_query, per_page, offset)
        
        search_result = result['result']
        total = result['count']
        href = "?act=past_list&sub=seach" + f + t + lang_str + sites_str + "&page={0}"
    else:
        #全言語
        search_result = ReadingAll.latest(per_page, offset)
        #検索結果合計
        total = ReadingAll.all_aticles()
        href = "?act=past_list&page={0}"
    
    pagination = utils.pagination(total - 1, "MTG記事", href, per_page)

    for u in search_result:
        news.append({
            "prefix"        : u.flag_prefix,
            "published"     : u.published,
            "title"         : u.title,
            "link"          : u.link,
            "date"          : u.date,
            "source_from"   : u.site_name,
            "image"         :u.image
        })

    render_params["langs"]              = langs
    render_params["sites"]              = sites
    render_params["total_articles"]     = total
    render_params["news"]               = news
    render_params["per_page_skip"]      = offset
    render_params["pagination"]         = pagination
    render_params["pagination_items"]   = news
    render_params["body"]               = data["body"]
    render_params["title"]              = data["title"]
    render_params["include_css"]        = [
        {'css': "pagination.css"},
        {'css': "jquery-ui.theme.min.css"},
        {'css': "general-articles-past.css"}
    ]
    render_params["include_js"] = [
        {'js': "date-picker.js"},
        {'js': "lang-sites-search.js"},
        {'js': "general-article-past.js"}
    ]
    return render_params