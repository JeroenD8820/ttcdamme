import requests
import json
import xml.etree.ElementTree as ET
import sys

# TabT API Configuration
WSDL_URL = "https://api.vttl.be/"
NAMESPACE = "{http://api.frenoy.net/TabTAPI}"
CLUB_ID = "WVL158"
SEASON_ID = 26 # 2025-2026

def make_soap_request(method, payload):
    soap_header = '<?xml version="1.0" encoding="utf-8"?>'
    soap_body = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tab="http://api.frenoy.net/TabTAPI">
       <soapenv:Header/>
       <soapenv:Body>
          <tab:{method}>
             {payload}
          </tab:{method}>
       </soapenv:Body>
    </soapenv:Envelope>
    """
    
    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": f"http://api.frenoy.net/TabTAPI#{method}"
    }
    
    try:
        response = requests.post(WSDL_URL, data=soap_body, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error calling {method}: {e}")
        return None

def parse_members(xml_text):
    root = ET.fromstring(xml_text)
    members = []
    # Find Members in the response
    for member_node in root.findall(f".//{NAMESPACE}MemberEntries"):
        member = {
            "firstname": member_node.findtext(f"{NAMESPACE}FirstName"),
            "lastname": member_node.findtext(f"{NAMESPACE}LastName"),
            "ranking": member_node.findtext(f"{NAMESPACE}Ranking"),
            "elo": member_node.findtext(f"{NAMESPACE}RankingPoints"),
            "position": member_node.findtext(f"{NAMESPACE}Position"), # For relative points?
        }
        members.append(member)
    return members

def parse_teams(xml_text):
    root = ET.fromstring(xml_text)
    teams = []
    for team_node in root.findall(f".//{NAMESPACE}TeamEntries"):
        team = {
            "team": team_node.findtext(f"{NAMESPACE}Team"),
            "divisionId": team_node.findtext(f"{NAMESPACE}DivisionId"),
            "divisionName": team_node.findtext(f"{NAMESPACE}DivisionName"),
        }
        teams.append(team)
    return teams

def parse_matches(xml_text):
    root = ET.fromstring(xml_text)
    matches = []
    for match_node in root.findall(f".//{NAMESPACE}TeamMatchEntries"):
        matches.append({
            "date": match_node.findtext(f"{NAMESPACE}Date"),
            "home": match_node.findtext(f"{NAMESPACE}HomeTeam"),
            "away": match_node.findtext(f"{NAMESPACE}AwayTeam"),
            "score": match_node.findtext(f"{NAMESPACE}Score"),
            "isMatchFree": match_node.findtext(f"{NAMESPACE}IsMatchFree")
        })
    return matches

def main():
    data = {}
    
    # Get Members
    print("Fetching members...")
    members_payload = f"<tab:Club>{CLUB_ID}</tab:Club>"
    members_xml = make_soap_request("GetMembers", members_payload)
    if members_xml:
        data["members"] = parse_members(members_xml)
    
    # Get Teams
    print("Fetching teams...")
    teams_payload = f"<tab:Club>{CLUB_ID}</tab:Club>"
    teams_xml = make_soap_request("GetClubTeams", teams_payload)
    if teams_xml:
        data["teams"] = parse_teams(teams_xml)
        
    # Get Results (Last 10 matches)
    print("Fetching matches...")
    matches_payload = f"<tab:Club>{CLUB_ID}</tab:Club><tab:ShowAll>1</tab:ShowAll>"
    matches_xml = make_soap_request("GetMatches", matches_payload)
    if matches_xml:
        data["matches"] = parse_matches(matches_xml)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print("Data saved to data.json")

if __name__ == "__main__":
    main()
