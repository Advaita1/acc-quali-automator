from tools.builders import build_authenticated_sheet, build_current_lap_dict, build_batch_element

def update_quali_sheet(new_laps, sheet_name):
    """Update quali sheet.

    Keyword arguments:
    new_laps -- List of new lap dicts.
    sheet_name -- String containing sheet name.
    """
    if new_laps == None:
        return
    # Get sheet
    sheet = build_authenticated_sheet(sheet_name)
    # Get current laps
    current_laps = sheet.get_all_records()
    # Build current lap dict
    current_laps_dict = build_current_lap_dict(current_laps)

    batch = []
    new_driver_insertion_row = 500
    # Iterate through new laps
    for new_lap in new_laps:
        # Check if driver has existing time
        if new_lap['driver_name'] in current_laps_dict.keys():
            # Add to batch if new time is faster
            if current_laps_dict[new_lap['driver_name']]['lap_time'] > new_lap['lap_time']:
                batch.append(build_batch_element(new_lap, current_laps_dict))
        # Add new driver to batch
        else:
            batch.append(build_batch_element(new_lap, None, new_driver_insertion_row))
            new_driver_insertion_row += 1
    # Update sheet
    sheet.batch_update(batch)
    # Sort sheet
    sheet.sort((5, 'asc'), range='B2:E550')
