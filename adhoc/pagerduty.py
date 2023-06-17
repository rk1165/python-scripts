import requests
import sys

# Enter your pagerduty API token here
TOKEN = ''

headers = {
    'Accept': 'application/vnd.pagerduty+json;version=2',
    'Authorization': f'Token token={TOKEN}',
    'Content-Type': 'application/json'
}


# Get pagerduty incident details
def get_incident_details(incident_id):
    get_incident = f"https://api.pagerduty.com/incidents/{incident_id}"
    response = requests.get(get_incident, headers=headers)
    # print(response.json())
    return response.json()


# Lists all notes related to an incident
def list_incident_notes(incident_id):
    list_notes = f"https://api.pagerduty.com/incidents/{incident_id}/notes"
    response = requests.get(list_notes, headers=headers)
    # print(response.json())
    return response.json()


# Generates report for a specific incident
def generate_report(incident_id):
    incident_details = get_incident_details(incident_id)
    incident_notes = list_incident_notes(incident_id)

    title = incident_details['incident']['title']
    created_at = incident_details['incident']['created_at']
    status = incident_details['incident']['status']

    notes = list()
    for note in incident_notes['notes']:
        user = note['user']['summary']
        resolution_note = note['content']
        notes.append(user + " | " + resolution_note)

    report = str(incident_id) + " | " + title + " | " + created_at + " | " + status + " | " + ','.join(notes)
    return report


# Reads a list of incident ids from stdin and creates a markdown report.
# usage: python3 pagerduty.py < incidents.txt > report.md
def create_report():
    print('Incident Id  | Title  | Created At | Status | User  | Resolution Note |')
    print('------------ | ------ | ---------- | -------| ----- | ----------------|')
    for incident_id in sys.stdin:
        print(generate_report(incident_id.strip('\n')))
        print()


if __name__ == '__main__':
    # create_report()
    print(generate_report(325993))
    # get_incident_details(308060)
    # list_incident_notes(308060)
