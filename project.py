projects = {
    "Frontend Developer": [
        {
            "name": "Responsive Portfolio Website",
            "desc": "Every front-end dev needs a personal website to showcase their skills, projects, and resume",
            "link": "https://youtu.be/0YFrGy_mzjY?si=EKsr1zvW_Rp4CSVu"
        },
        {
            "name": "Netflix Clone",
            "desc": "Built a simple netflix front-end clone with figma or any tool of your choice",
            "link": "https://youtu.be/Tgat3-prVv4?si=5BGIeaJTDT73ckPv"
        },
        {
            "name": "Interactive Weather App",
            "desc": "Built a weather app that fetches live weather data from an API and displays it beautifully",
            "link": "https://youtu.be/WZNG8UomjSI?si=k-icilv6MGYwNU5k"
        },
    ],
}

def get_projects(path):
    return projects[path]

'''a = get_projects("data_science")
for i in a:
    print(i["name"])
    print(i["desc"])
    print(i["link"])'''
