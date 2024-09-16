import pandas as pd
from glob import glob

def load_subs(path):
    path = path + "/*.srt"
    subs = glob(path)
    episodes = []
    scripts = []

    for sub in subs:
        with open(sub, "r", encoding="utf-8") as f:
            lines = f.readlines()
            con = []
            for line in lines:
                line = line.strip().replace("Sync", "").replace("vNaru", "")
                if line.isnumeric() or "-->" in line:
                    continue
                else:
                    con.append(line)
        
        script = " ".join(con)
        epno = int(sub.split("-")[1].strip()[-1])
        episodes.append(epno)
        scripts.append(script)

    df = pd.DataFrame({"episode": episodes, "script": scripts})
    return df