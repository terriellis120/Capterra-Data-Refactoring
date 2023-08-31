import os
import json
import re
from GPT import get_gpt
from urllib.parse import urlparse
import regex


def get_alt_products(jsondata):
    # print(altProds)
    
    human_message = ""

    for altprod in jsondata.get("alternativeProducts"):
        tem_hm = f"- {altprod['name']}, bearing common features such as \n"
        for sfeat in altprod["features"]:
            tem_hm += f"o {sfeat['name']}, defined as {sfeat['definition']}, with the corresponding rating {sfeat['avgRating']}\n"
        human_message += tem_hm

    prompt = f"""
As a Competitor Analysis Expert in software review, your role involves producing an informative paragraph titled 'Alternative Products' for the software {jsondata.get('name')}.


"
{human_message}
"

This response sentence must follow the following rules:
1. Must start with "<h2>Alternative Products</h2>"
1. keep your response sentence between 120-150 words in length. 130-140 words is ideal.
2. must to grasp the overall user sentiment as communicated by the numerical values, but without mentioning numerical values
3. must to show how alternative prducts concoct has common features with {jsondata.get('name')}
4. don't mention the word "review".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.



your response:
"""
    # return prompt

    try:
        return get_gpt(prompt)
    except Exception as e:
        print("alternative products")
        print(e)
        return ""


def get_pricing_value(jsondata, text_list):
    keywords = ["pric", "cost", "valu", "worth", "money"]
    search_reviews = [s for s in text_list if any(k in s for k in keywords)]
    reviews = ""
    for sr in search_reviews:
        reviews += f"o {sr}\n\n"
        
    pricingplansData = jsondata["pricingPlansData"]

    pricingplans = pricingplansData["plans"]
    planstext = ""
    for plan in pricingplans:
        planstext += f"""the plan '{plan["name"]}' \n"""
        planstext += f""" o description: '{plan["description"]}' \n"""
        planstext += f""" o starting_price: '{plan["starting_price"]}' \n"""
        planstext += f""" o pricing_model_name: '{plan["pricing_model_name"]}' \n"""
        planstext += f""" o payment_frequency_name: '{plan["payment_frequency_name"]}' \n"""
        planstext += f""" o attributes: '{[x["name"] for x in plan["attributes"]][:3]}' \n\n"""


    prompt = f"""
As a Software Value Analyst, your duty involves crafting an incisive and insightful paragraph titled 'Cost & Value for Money' for the software {jsondata.get("name")}.



""
- Your review should initially employ your expertise to depict a holistic view of the product's value, taking into account factors like {jsondata.get("pricingDetails")} and its 'value for money' rating {jsondata.get("valueForMoneyRating")}. ( for the latter grasp the overall user sentiment as communicated by the numerical value, but don't mention it ).


- Elaborate Pring Plans:
{planstext}

- If applicable. Disclose whether the product offers a Free Version = {jsondata.get("hasFreeVersion")} and/or Free Trial = {jsondata.get("hasFreeTrial")}, remembering that True means yes and False means no.

- Consider the following reviews of this product:
{reviews}
""

This response sentence must follow the following rules:
1. Must start with "<h2>Cost & Value for Money</h2>"
2. keep your response sentence between 120-150 words in length!! 130-140 words is ideal.
3. mention specific numerical cost or price value only, but don't mention numerical values about rating.
4. don't mention the word "review"
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.



    """

    try:
        return get_gpt(prompt)

    except Exception as e:
        print(e)
        return "Error occured while GPT"


def get_ease_use(jsondata, text_list):
    keywords = ["ease", "simplicit", "use", "layout", "interface", "design"]
    search_reviews = [s for s in text_list if any(k in s for k in keywords)]
    reviews = ""
    for sr in search_reviews:
        reviews += f"- {sr}\n\n"

    prompt = f"""
As a Software Usability Analyst, your task is to compose a discerning paragraph titled 'Ease of Use & Interface Design' for the software {jsondata.get('name')}.

"
This product has the ease of use rating {jsondata.get('easeOfUseRating')} and functionality {jsondata.get('functionalityRating')}.


Consider the following reviews of this product:
{reviews}
"

    
This response sentence must follow the following rules:
1. Must start with "<h2>Ease of Use & Interface Design</h2>"
2. keep your response sentence between 120-150 words in length. 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical values, but without mentioning numerical values
4. don't mention the word "review".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.
        
    """
    # return prompt
    try:
        return get_gpt(prompt)
    except Exception as e:
        print("easeUse")
        print(e)
        return ""


def get_customer_support(jsondata, text_list):
    keywords = ["custom", "client", "servic", "assist", "user", "support", "aid"]
    search_reviews = [s for s in text_list if any(k in s for k in keywords)]
    reviews = ""
    for sr in search_reviews:
        reviews += f"- {sr}\n\n"

    prompt = f"""
As a Software Support Analyst, you're assigned to craft a perceptive paragraph titled 'Customer Service & User Support' for the software {jsondata.get('name')}.

""
This product has recived Service Rating for customer: {jsondata.get('customerServiceRating')}

Consider the following reviews of this product:
{reviews}
""

This response sentence must follow the following rules:
1. Must start with "<h2Customer Service & User Support</h2>"
2. keep your response sentence between 120-150 words in length 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical values, but without mentioning numerical values.
4. don't mention the word "review".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.

    """

    try:
        return get_gpt(prompt)
    except Exception as e:
        print("customerSupport")
        print(e)
        return ""


def get_best_for(jsondata, text_list):
    keywords = ["best", "ideal"]
    search_reviews = [s for s in text_list if any(k in s for k in keywords)]
    reviews = ""
    for sr in search_reviews:
        reviews += f"- {sr}\n\n"

    prompt = f"""

As a Software Audience Analyst, you are charged with the task of composing an enlightening paragraph titled 'Best for' for the software {jsondata.get('name')}.

""
- This product is the best for {jsondata.get('bestFor')} and these demographics: {jsondata.get('targetUsers')}.

- Consider the following reviews of this product:
{reviews}

""

This response sentence must follow the following rules:
1. Must start with "<h2>Best for</h2>"
2. keep it between 120-150 words in length. 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical rating values, but without mentioning numerical values.
4. don't mention the word "review".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.

    """

    try:
        return get_gpt(prompt)
    except Exception as e:
        print(e)
        return ""
    pass


def get_description(jsondata):
    prompt = f"""
As a Software Description Analyst, your task is to craft an engaging paragraph titled 'Description' for the software {jsondata.get('name')}.

""
This product has short and long descriptions:
- {jsondata.get('longDescription')}
- {jsondata.get('shortDescription')}
""

his response sentence must follow the following rules:
1. Must start with "<h2>Description</h2>\n{jsondata.get('name')} is "
2. keep it between 120-150 words in length. 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical rating values, but without mentioning numerical values.
4. don't mention the word "review".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.
    """

    try:
        return get_gpt(prompt)
    except Exception as e:
        print(e)
        return ""
    pass
    pass


def get_innovation(jsondata, text_list):
    keywords = ["featur", "innovat", "distinct", "uniqu", "characterist"]
    search_reviews = [s for s in text_list if any(k in s for k in keywords)]
    reviews = ""
    for sr in search_reviews:
        reviews += f"- {sr}\n\n"

    features = jsondata.get("features")

    human_message = ""

    
    for feat in features:
        tem_hm = f"- {feat['categoryName']}, bearing common features such as \n"
        for sfeat in feat["categoryFeatures"]:
            tem_hm += f"o {sfeat['name']}, defined as {sfeat['definition']}, pondering its importance as indicated by {sfeat['avg_importance']}. Reflect on the frequency this feature is utilized, given by this rating {sfeat['pct_time_used']}, and its user rating by {sfeat['avg_rating']} \n"
        human_message += tem_hm

    prompt = f"""
As a Software Review Expert, you're tasked with constructing an insightful paragraph titled 'Innovation & Unique Features' for the software {jsondata.get('name')}.

""
The features of products are:
{human_message}

Consider the following reviews of this product:
{reviews}

""

This response sentence must follow the following rules:
1. Must start with "<h2>Innovation & Unique Features</h2>"
2. keep it between 120-150 words in length. 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical rating values, but without mentioning numerical values
4. don't mention the word "review".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.


"""
    

    try:
        return get_gpt(prompt)
    except Exception as e:
        print("innovation")
        print(e)
        return ""


def get_collaboration(jsondata, text_list):
    keywords = ["collabor", "teamwork", "communicat", "dialogu"]
    search_reviews = [s for s in text_list if any(k in s for k in keywords)]
    reviews = ""
    for sr in search_reviews:
        reviews += f"- {sr}\n\n"

    prompt = f"""
As a Software Collaboration Analyst, your task is to decipher and relay the fundamental aspects of the software {jsondata.get('name')}, within an enticing paragraph titled 'Collaboration & Communication'.

""

Consider the following reviews of this product:
{reviews}

""

This response sentence must follow the following rules:
1. Must start with "<h2>Collaboration & Communication</h2>"
2. keep it between 120-150 words in length. 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical rating values, but without mentioning numerical values.
4. don't mention the word "review".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.

    """

    try:
        return get_gpt(prompt)
    except Exception as e:
        print(e)
        return ""


def get_efficiency(jsondata, text_list):
    keywords = ["effici", "productiv", "flow", "control", "work", "process", "manag"]
    search_reviews = [s for s in text_list if any(k in s for k in keywords)]
    reviews = ""
    for sr in search_reviews:
        reviews += f"- {sr}\n\n"

    prompt = f"""
As a Workflow Efficiency Analyst, your role is to decode and express the essential attributes of the software {jsondata.get('name')}, within a gripping paragraph titled 'Efficiency & Workflow Management'.

""

Consider the following reviews of this product:
{reviews}

""

This response sentence must follow the following rules:
1. Must start with "<h2>Efficiency & Workflow Management</h2>"
2. keep it between 120-150 words in length. 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical rating values, but without mentioning numerical values.
4. don't mention the word "review".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.

    """

    try:
        return get_gpt(prompt)
    except Exception as e:
        print(e)
        return ""


def get_adaptability(jsondata, text_list):
    keywords = ["adapt", "flexibl", "integrat", "merg"]
    search_reviews = [s for s in text_list if any(k in s for k in keywords)]
    reviews = ""
    for sr in search_reviews:
        reviews += f"- {sr}\n\n"

    prompt = f"""
As a Software Compatibility Analyst, your responsibility is to decode and convey the core attributes of the software {jsondata.get('name')}, within an intriguing paragraph titled 'Adaptability & Integration'.

""

Consider the following reviews of this product:
{reviews}

""

This response sentence must follow the following rules:
1. Must start with "<h2>Adaptability & Integration</h2>"
2. keep it between 120-150 words in length. 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical rating values, but without mentioning numerical values.
4. don't mention the word "review".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.
    """

    try:
        return get_gpt(prompt)
    except Exception as e:
        print(e)
        return ""


def get_security_privacy(jsondata, text_list):
    keywords = ["secur", "protect", "privac", "confidenti"]
    search_reviews = [s for s in text_list if any(k in s for k in keywords)]
    reviews = ""
    for sr in search_reviews:
        reviews += f"- {sr}\n\n"

    prompt = f"""
As a Software Security Analyst, your obligation is to demystify and communicate the key aspects of the software {jsondata.get('name')}, within a compelling paragraph titled 'Security & Privacy'.

""

Consider the following reviews of this product:
{reviews}

""

This response sentence must follow the following rules:
1. Must start with "<h2>Security & Privacy</h2>"
2. keep it between 120-150 words in length. 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical rating values, but without mentioning numerical values
4. don't mention the word "review".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.
    """

    try:
        return get_gpt(prompt)
    except Exception as e:
        print(e)
        return ""


def get_scalability(jsondata, text_list):
    keywords = ["scalabl", "expand", "growth", "possibl", "potenti", "progress"]
    search_reviews = [s for s in text_list if any(k in s for k in keywords)]
    reviews = ""
    for sr in search_reviews:
        reviews += f"- {sr}\n\n"


    prompt = f"""
As a Software Scalability Analyst, your duty is to decipher and express the essence of the software {jsondata.get('name')}, in a thought-provoking paragraph titled 'Scalability & Growth Potential'.

""

Consider the following reviews of this product:
{reviews}

""

This response sentence must follow the following rules:
1. Must start with "<h2>Scalability & Growth Potential</h2>"
2. keep it between 120-150 words in length. 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical rating values, but without mentioning numerical values.
4. don't mention the word "review".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.

    """

    try:
        return get_gpt(prompt)
    except Exception as e:
        print(e)
        return ""


def get_highlights_pro(jsondata):
    prosText = [x["prosText"] for x in jsondata.get("reviews")]
    if len(prosText) > 30:
        prosText = prosText[:30]


    prompt = f"""
As a Software Review Expert, your mission is to distill and articulate the essence of software {jsondata.get('name')}, into an insightful, one-paragraph titled ""Highlights Pros"".

""

Consider the following reviews of this product:
{prosText}

""

This response sentence must follow the following rules:
1. Must start with "<h2>Highlights Pros</h2>"
2. keep it between 120-150 words in length. 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical rating values, but without mentioning numerical values.
4. don't mention the word "review".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.

    """
    try:
        return get_gpt(prompt)
    except Exception as e:
        print("highlights")
        print(e)
        return ""


def get_highlits_con(jsondata):
    consText = [x["consText"] for x in jsondata.get("reviews")]
    if len(consText) > 30:
        consText = consText[:30]

    
    prompt = f"""
As a Software Review Expert, your mission is to distill and articulate the essence of software {jsondata.get('name')}, into an insightful, one-paragraph titled ""Highlights Cons"".

""

Consider the following reviews of this product:
{consText}

""

This response sentence must follow the following rules:
1. Must start with "<h2>Highlights Cons</h2>"
2. keep it between 120-150 words in length. 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical rating values, but without mentioning numerical values.
4. Don't mention the word "review" ever, replace it with "feedback".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.
    """

    try:
        return get_gpt(prompt)
    except Exception as e:
        print("highlights")
        print(e)
        return ""

def get_overall_conclusion(jsondata):
    prosText = [x["prosText"] for x in jsondata.get("reviews")]
    if len(prosText) > 30:
        prosText = prosText[:30]

    consText = [x["consText"] for x in jsondata.get("reviews")]
    if len(consText) > 30:
        consText = prosText[:30]

    title = [x["title"] for x in jsondata.get("reviews")]
    if len(title) > 30:
        title = title[:30]

    generalComments = [x["generalComments"] for x in jsondata.get("reviews")]
    if len(generalComments) > 30:
        generalComments = generalComments[:30]

    transcriptContent = [
        re.sub(r"\s+", " ", x["transcriptContent"]).replace("rn", "\n")
        for x in jsondata.get("videoReviews", [])
    ]
    if len(transcriptContent) > 5:
        transcriptContent = transcriptContent[:5]

    text_list = prosText + consText + title + generalComments
    keywords = ["recommend"]
    search_reviews = [s for s in text_list if any(k in s for k in keywords)]
    reviews = "\n".join(search_reviews)

    genComm = "\n".join(generalComments)
    transCont = "\n".join(transcriptContent)
    transCont = re.sub("\n+", "\n", transCont)
    genComm = re.sub("\n+", "\n", genComm)

    overallRating = jsondata.get("overallRating")
    recommendationRating = jsondata.get("recommendationRating")
    prompt = f"""
As a Software Review Expert, your mission is to distill and articulate the essence of software {jsondata.get('name')}, into an insightful, one-paragraph conclusion titled 'Overall Conclusion'.

""
Draw from this collection of reviews: {genComm}, {transCont} and {reviews}, identifying their key features, strengths, and weaknesses
Capture the general sentiment as indicated by {recommendationRating} and {overallRating}.
""


This response sentence must follow the following rules:
1. Must start with "<h2>Overall Conclusion</h2>"
2. keep it between 120-150 words in length. 130-140 words is ideal.
3. must to grasp the overall user sentiment as communicated by the numerical rating values, but without mentioning numerical values.
4. Don't mention the word "review", replace it with "feedback".
5. should showcase enthusiasm and adhere to professional language norms.
6. must anonymize all human names, and replace 'Capterra', if encountered, with 'most popular platforms'.
    """

    try:
        return get_gpt(prompt)
    except Exception as e:
        print("overall")
        print(e)
        return ""

def convert_match(match):
    x = str(match.group(0))
    x = "\n"+x
    # x.replace('\\', '')
    return x

def get_information(filename):
    with open(filename, "r") as f:
        jsondata = json.load(f)

    prosText = [x["prosText"] for x in jsondata.get("reviews")]
    if len(prosText) > 30:
        prosText = prosText[:30]

    consText = [x["consText"] for x in jsondata.get("reviews")]
    if len(consText) > 30:
        consText = prosText[:30]

    title = [x["title"] for x in jsondata.get("reviews")]
    if len(title) > 30:
        title = title[:30]

    generalComments = [x["generalComments"] for x in jsondata.get("reviews")]
    if len(generalComments) > 30:
        generalComments = generalComments[:30]

    text_list = prosText + consText + title + generalComments
    pricingdetails = regex.sub(r'\n(.*?):', convert_match, jsondata.get("pricingDetails")).split("\n\n")
    data = {
        "Software name": jsondata.get("name"),
        "URL": f"{urlparse(jsondata.get('url')).scheme}://{urlparse(jsondata.get('url')).netloc}",
        "Logo": jsondata.get("logoUrl"),
        "Category": [x["categoryName"] for x in jsondata.get("features")],
        "alternativeProducts": jsondata.get("alternativeProducts"),
        "hasFreeTrial": jsondata.get("hasFreeTrial"),
        "hasFreeVersion": jsondata.get("hasFreeVersion"),
        "vendor": jsondata.get("vendor"),
        "Platforms": [(x["name"], x["enabled"]) for x in jsondata.get("platform", [])],
        "Pricing": {
            "Pricing": jsondata.get("pricing"),
            "hasFreeVersion": jsondata.get("hasFreeVersion"),
            "hasFreeTrial": jsondata.get("hasFreeTrial"),
            "valueForMoneyRating": jsondata.get("valueForMoneyRating"),
            "Fee schedule": jsondata.get("feeSchedule"),
            "Pricing Model": jsondata.get("pricingModel"),
            "Pricing amount": jsondata.get("pricingAmount"),
            "Pricing Details": pricingdetails,
        },
        "Target User": jsondata.get("targetUsers"),
        "Training": [(x["name"], x["enabled"]) for x in jsondata.get("training", [])],
        "Support": [(x["name"], x["enabled"]) for x in jsondata.get("support", [])],
        "Ratings": {
            "overallRating": jsondata.get("overallRating"),
            "easeOfUseRating": jsondata.get("easeOfUseRating"),
            "customerServiceRating": jsondata.get("customerServiceRating"),
            "functionalityRating": jsondata.get("functionalityRating"),
            "valueForMoneyRating": jsondata.get("valueForMoneyRating"),
            "recommendationRating": jsondata.get("recommendationRating"),
        },
        "Popular Comparisons": [
            (x["product_1"]["name"], x["product_2"]["name"])
            for x in jsondata.get("popularComparisons", [])
        ],
        "Recommended Product": jsondata.get("recommendedProducts"),
        "Media": jsondata.get("media"),
    }

    features = []
    for feat in jsondata.get("features"):
        temfeat = [x for x in feat["categoryFeatures"] if x["value"]==True]
        features.append({ "categoryName": feat['categoryName'], "categoryFeatures": temfeat})

    data["Features"] = features
    # data["Alternative Products"] = get_alt_products(jsondata)
    # data["Pricing & Value for Money"] = get_pricing_value(jsondata, text_list)
    # data["Ease of Use & Interface Design"] = get_ease_use(jsondata, text_list)
    # data["Customer Service & User Support"] = get_customer_support(jsondata, text_list)
    # data["Best for"] = get_best_for(jsondata, text_list)
    # data[f"What is {jsondata.get('name')}?"] = get_description(jsondata)

    
    # data["Innovation & Unique Features"] = get_innovation(jsondata, text_list)
    # data["Collaboration & Communication"] = get_collaboration(jsondata, text_list)
    # data["Efficiency & Workflow Management"] = get_efficiency(jsondata, text_list)
    # data["Adaptability & Integration"] = get_adaptability(jsondata, text_list)
    # data["Security & Privacy"] = get_security_privacy(jsondata, text_list)
    # data["Scalability & Growth Potential"] = get_scalability(jsondata, text_list)

    # data["Highlights Pro"] = get_highlights_pro(jsondata)
    # data["Highlights Cons"] = get_highlits_con(jsondata)
    # data["Overall Conclusion"] = get_overall_conclusion(jsondata)

    return data


if __name__ == "__main__":
    data = get_information("pull/HubSpot-Marketing.json")
    with open("data.json", "w") as f:
        json.dump(data, f)

    # with open("pull/Filestage.json", "r") as f:
    #     jsondata = json.load(f)
    
    # prosText = [x["prosText"] for x in jsondata.get("reviews")]
    # if len(prosText) > 30:
    #     prosText = prosText[:30]

    # consText = [x["consText"] for x in jsondata.get("reviews")]
    # if len(consText) > 30:
    #     consText = prosText[:30]

    # title = [x["title"] for x in jsondata.get("reviews")]
    # if len(title) > 30:
    #     title = title[:30]

    # generalComments = [x["generalComments"] for x in jsondata.get("reviews")]
    # if len(generalComments) > 30:
    #     generalComments = generalComments[:30]

    # text_list = prosText + consText + title + generalComments
    
    # # text = ""
    # res = get_overall_conclusion(jsondata)
    # # print(prompt)
    # # res = get_gpt(prompt)
    # print(res)
    # print(len(res.split()))