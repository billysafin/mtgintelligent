import services.MtgReadingAllService as ReadingAll
import services.MtgTournamentsService as Tour
import services.MtgDecklistService as Decklist

#HOME
def top(render_params, data):
    #全言語記事
    news = []
    latest_all = ReadingAll.latest(10, 0)
    for u in latest_all:
        news.append({
            "flag_prefix":u.flag_prefix,
            "published":u.published,
            "title":u.title,
            "link":u.link,
            "date":u.date,
            "source_from":u.site_name
        })
       
    #トーナメント
    tours_values = []
    tours = Tour.getLatestTours(10)
    for u in tours:
        if u.format_name == 'Limited' or u.format_name == 'Pauper' or u.format_name == 'Block' or u.format_name == 'Other':
            class_label = 'label label-danger'
            format = 'other'
        elif u.format_name == 'Standard':
            class_label = 'label label-default'
            format = 'standard'
        elif u.format_name == 'Modern':
            class_label = 'label label-primary'
            format = 'modern'
        elif u.format_name == 'Legacy':
            class_label = 'label label-success'
            format = 'legacy'
        elif u.format_name == 'Vintage':
            class_label = 'label label-info'
            format = 'vintage'
        elif u.format_name == 'Commander':
            class_label = 'label label-warning'
            format = 'commander'
        else:
            class_label = 'label label-danger'
            format = 'other'
            
        tours_values.append({
            "id"           : u.id,
            "name"         : u.name,
            "date"         : u.start,
            "class_label"  : class_label,
            "format"       : format
        })    
    
    #decklists
    decklists = Decklist.getPopularDecks(10, True, True)
    popular_decklists = []
    for u in decklists:
        if u.format_name == 'Limited' or u.format_name == 'Pauper' or u.format_name == 'Block' or u.format_name == 'Other':
            class_label = 'label label-danger'
            format = 'other'
        elif u.format_name == 'Standard':
            class_label = 'label label-default'
            format = 'standard'
        elif u.format_name == 'Modern':
            class_label = 'label label-primary'
            format = 'modern'
        elif u.format_name == 'Legacy':
            class_label = 'label label-success'
            format = 'legacy'
        elif u.format_name == 'Vintage':
            class_label = 'label label-info'
            format = 'vintage'
        elif u.format_name == 'Commander':
            class_label = 'label label-warning'
            format = 'commander'
        else:
            class_label = 'label label-danger'
            format = 'other'
        
        popular_decklists.append({
            "id"            : u.id,
            "name"          : u.name,
            "count"         : u.count,
            "format"        : format,
            "class_label"   : class_label
        })
    
    render_params['popular_decklists'] = popular_decklists
    render_params["tours"] = tours_values
    render_params["news"] = news
    render_params["body"] = data["body"]
    render_params["title"] = data["title"]
    render_params["include_js"] = [{'js': "tab.js"}]
    return render_params