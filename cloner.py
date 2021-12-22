# clone multiple course repos
# this utility included for convenience
# it was used once - not the best solution to check all course files

from git import Repo

# insert appropriate username and token below
user = "github_username"
token = "github_token"

github_root = "github.com/RedHatTraining/"

# course_list = ["AD183", "AD240", "AD248", "AD283", "AD348", "AD371", "AD373", "AD421", "AD427", "AD440", "AD465", "CL110", "CL210", "CL260", "CL310", "DO101", "DO180", "DO280", "DO288", "DO292", "DO295", "DO378", "DO380", "DO405", "DO407",
            #    "DO410", "DO417", "DO425", "DO447", "DO457", "RH124", "RH134", "RH199", "RH236", "RH294", "RH318", "RH342", "RH354", "RH358", "RH362", "RH403", "RH436", "RH442", "RH442", "CEPH125", "DO283", "DO409", "RH415", "RH259", "RH254", "DO328"]
# course_list = ["DO409", "DO280", "JB440", "DO407", "RH318", "CEPH1", "CL310", "DO380", "JB183", "DO288", "RH309", "RH311", "IH310", "DO180", "RH436", "RH254", "RH299", "RH362", "DO410", "JB283", "DO292", "RH413", "RH342", "DO405", "RH124", "RH134", "RH199", "RH403", "CL110", "RH442", "RH236", "CL220", "CL210", "RH401", "DO999", "DO457", "RH024", "JB421", "RH415", "DO285", "JB248", "DO425", "JB501", "JB325", "JB348",
            #    "JB435", "JB450", "JB465", "JB453", "JB371", "JB373", "DO290", "RH259", "JB240", "DO500", "DO388", "RH354", "RH294", "DO447", "DO417", "DO101", "DO378", "RH358", "DO328", "DO295", "CL260", "AD183", "AD240", "AD427", "AD248", "AD440", "DO400", "AD364", "DO322", "DO250", "DO477", "DO370", "DO326", "DO480", "DO401", "DO402", "AD482", "RES29", "DO100", "DO316", "DO374", "DO467", "TL112", "RH445", "RES12", "WS380", ]
course_list = ["RES294", "RES123"]
github_url = "https://" + user + ":" + token + "@" + github_root
root_dir = "../New/"

for course in course_list:
    remote = github_url + course
    local = root_dir + course
    try:
        Repo.clone_from(remote, local, depth=1)
    except:
        print(course+" not found")

