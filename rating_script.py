import pandas as pd
from jinja2 import Environment, FileSystemLoader

df = pd.read_csv('./Rating_Table.csv')

# Cleaning prices from string and leaving only numbers and NaN.
for column in df.columns[df.columns.get_loc('Receiving call cost per min'):]:
    df[column] = pd.to_numeric(df[column], errors='coerce')

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('RATING_XML.xml')


def write_content_to_xml(index, row):
    filename = f"RATING_XML_{row['Company code']}.xml"
    content = template.render({
        'region': row['Region'],
        'country': row['Country'],
        'company_name': row['Company name'],
        'company_number': row['Company number'],
        'company_code': row['Company code'],
        'company_features': row['Company features'],
        'receiving_call_cost_per_min': round(float(row['Receiving call cost per min']), 2),
        'local_call_cost_per_min': round(float(row['Local call cost per min']), 2),
        'calling_to_me_cost_per_min': round(float(row['Calling to ME cost per min']), 2),
        'calling_to_other_destinations_cost_per_min': round(float(row['Calling to other destinations cost per min']), 2),
        'sms_mo_cost_per_sms': round(float(row['SMS  MO cost per sms']), 2),
        'sms_mt_cost_per_sms': round(float(row['SMS MT cost per sms']), 2),
        'data_cost_per_mb': round(float(row['Data cost per MB']), 2),
        'hpmn': 'HPMN',
        'effective_date': '2024',
        'submission_dt': 'SubmissionDT',
        'iot_identifier': 'IOTIdentifier',
        'correction_sequence': 'CorrectionSequence',
        'iot_currency': 'USD'})
    # creating xml file.
    with open(filename, mode='w', encoding='utf-8') as new_xml:
        new_xml.write(content)
        print(f'{index}... wrote {filename}')


# Iterating over rows.
for index, row in df.iterrows():
    # checking for rows with no NaN values in df.
    if not row.isnull().values.any():
        write_content_to_xml(index, row)
    # rows with no NaN values in df
    else:
        # checking for rows with NaN values but Company code & Company number exist.
        if not pd.isna(df.at[index, 'Company code']) and not pd.isna(df.at[index, 'Company number']):
            # fill NaN with 0
            row.fillna(0, inplace=True)
            write_content_to_xml(index, row)
        else:
            # Company code & Company number are NaN drop entire row.
            row.dropna(inplace=True)
            print(f'{index}... It\'s not a valid row.')
