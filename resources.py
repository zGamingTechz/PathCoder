resources = {
    "Frontend Developer": ["https://youtu.be/WG5ikvJ2TKA?si=iMeAXD3-rRpOUCYQ", "https://www.youtube.com/watch?v=9He4UBLyk8Y&list=PLWKjhJtqVAbmMuZ3saqRIBimAKIMYkt0E", "https://www.geeksforgeeks.org/what-is-frontend-development/", "https://www.udemy.com/topic/Front-End-Web-Development/?utm_source=bing&utm_medium=udemyads&utm_campaign=BG-Search_DSA_GammaCatchall_NonP_la.EN_cc.India&campaigntype=Search&portfolio=Bing-India&language=EN&product=Course&test=&audience=DSA&topic=&priority=Gamma&utm_content=deal4584&utm_term=_._ag_1316117806681635_._ad__._kw_udemy_._de_c_._dm__._pl__._ti_dat-2334057027983529:loc-90_._li_156312_._pd__._&matchtype=b&msclkid=c78b3761b446129e654650f7e6e770cb"],
    "Backend Developer": []
}

def return_resources(path):
    try:
        return resources[path]
    except:
        return ["", "", "", ""]