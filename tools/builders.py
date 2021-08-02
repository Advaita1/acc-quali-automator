import gspread
from oauth2client.service_account import ServiceAccountCredentials
from data.car_by_id import car_by_id

def build_fastest_lap(result):
    """Return a dictionary containing a driver, car, race number, and fastest lap.

    Keyword arguments:
    result -- ACC leaderBoardLine list element.
    """
    m, s = divmod(result['timing']['bestLap'] / 1000, 60)
    time = f"{int(m)}:{round(s, 3)}"
    return {
        'driver_name': result['currentDriver']['firstName'] + ' ' + result['currentDriver']['lastName'],
        'car': car_by_id[result['car']['carModel']],
        'number': result['car']['raceNumber'],
        'lap_time': time,
        'id': result['currentDriver']['playerId']
    }

def build_fastest_laps(data):
    """Return a list of dictionaries which contain a driver, car, race number, and fastest lap.
    Return None if there were no laps set in the session.

    Keyword arguments:
    data -- ACC session dictionary.
    """
    # If there are no laps in the session, return None
    if len(data['sessionResult']['leaderBoardLines']) == 0:
        return None

    laps = []
    for result in data['sessionResult']['leaderBoardLines']:
        # Skip laps longer than 3 min
        if (result['timing']['bestLap'] > 180000):
            continue
        laps.append(build_fastest_lap(result))
    return laps

def build_authenticated_sheet(sheet_name):
    """Returns a gspread worksheet class instance for sheet1 in the corresponding spreadsheet

    Keyword arguments:
    sheet_name -- A string containing the name of the spreadsheet.
    """
    # Authenticate
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    # Access spreadsheet
    return client.open(sheet_name).sheet1

def build_current_lap_dict(current_laps):
    """Return a dict containing current lap data

    Keyword arguments:
    current_laps -- List of current lap dicts returned from the get_all_records gspread method.
    """
    dict = {}
    for current_lap in current_laps:
        dict[current_lap['ID']] = {
            'lap_time': current_lap['LAP TIME'],
            'sheet_location': f"B{current_lap['#'] + 1}:F{current_lap['#'] + 1}"
        }
    return dict

def build_batch_element(new_lap, current_lap_dict=None, insertion_row=None):
    """Return a batch element intened for gspread's batch update method

    Keyword arguments:
    new_lap -- Dict containing new lap data
    current_lap_dict -- (optional) Dict containing existing lap data. Pass in None for new drivers.
    insertion_row -- (optional) Insertion row for new driver records.
    """
    values = [[
                new_lap['driver_name'],
                new_lap['car'],
                new_lap['number'],
                new_lap['lap_time'],
                new_lap['id']
            ]]
    if current_lap_dict == None:
        return {
            'range': f"B{insertion_row}:F{insertion_row}",
            'values': values
        }
    return {
        'range': f"{current_lap_dict[new_lap['id']]['sheet_location']}",
        'values': values
    }
