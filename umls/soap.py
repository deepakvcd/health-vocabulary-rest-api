import requests
import json
def callmetamap(conversation, params):
    metamapurl = "https://sgm5quwy9l.execute-api.us-east-1.amazonaws.com/umls/umls/"
    payload = {"input": conversation,
                       "args": ["-R " + ",".join(params["sources"]), "-J " + ",".join(params["sems"])]}
    resp = requests.post(metamapurl, json=payload)
    jsoon_resp = resp.json()
    print(resp)
    return jsoon_resp

def getSourceIds(json_resp):
    health_url = "http://127.0.0.1:8000/concepts_bulk"
    soap_resp = []
    cuis = []
    print("metamap resp")
    print(json.dumps(json_resp))
    for phrases in json_resp:
        for phrase in phrases["phrases"]:
            each_obj  = {}
            for candidate in phrase["highestMapping"]["candidates"]:
                each_obj["str"] = candidate["candidatePreferred"]
                each_obj["cui"] = candidate["candidateCUI"]
                cuis.append(each_obj["cui"])
            soap_resp.append(each_obj)

    cuis_tuple = tuple(cuis)
    tupleresp = requests.get(health_url, {"terms" : ",".join(cuis_tuple)})
    #print(tupleresp.json())
    return tupleresp.json()
def getMetamapResponse(patient_conv, doc_conv):

    umlsUrl = "http://ec2-34-229-177-121.compute-1.amazonaws.com/concepts/"
    symptom_params = {"sources" : ["SNOMEDCT_US","ICD10CM"], "sems":["fndg", "sosy","phsf", "dsyn", "tmco","blor", "bpoc", "bdsu", "qlco", "qnco", "anst", "phsu", "clnd", "antb", "bhvr"
        , "biof", "horm", "humn", "hcpp", "inbe", "inpo", "medd", "menp", "ortf", "virs", "vita"] }


    assessment_params ={"sources":["ICD10CM"],"sems": ["dsyn", "tmco", "virs", "vita"]}
    plan_params = {"sources" : ["SNOMEDCT_US","RXNORM"],"sems": ["clnd", "phsu", "antb", "lbpr", "lbtr", "diap", "topp"]}

    # patient_conv = raw_input()
    # doc_conv = raw_input()

    patient_symp_json = callmetamap(patient_conv, symptom_params)
    soap_resp = {"symptoms":getSourceIds(patient_symp_json)}

    assesment_json = callmetamap(patient_conv, assessment_params)
    soap_resp["assessment"] = getSourceIds(assesment_json)


    doc_plan_json = callmetamap(doc_conv, plan_params)
    soap_resp["plan"] = getSourceIds(doc_plan_json)
    print(json.dumps(soap_resp))
    return soap_resp

    #print(json.dumps(doc_resp.json()))
# if __name__ == '__main__':
#     while True:
#         getMetamapResponse()