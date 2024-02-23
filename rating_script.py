import pandas as pd
from jinja2 import Environment, FileSystemLoader


def clean_data():
    df = pd.read_csv('./Rating_Table.csv')

    # Cleaning prices from string and leaving only numbers
    for column in df.columns[df.columns.get_loc('Receiving call cost per min'):]:
        df[column] = pd.to_numeric(
            df[column], errors='coerce', downcast='float')

    # dealing with NaNs
    for index, row in df.iterrows():
        if not pd.isna(row['Company code']) and not pd.isna(row['Company number']):
            # fill NaN with 0
            df.fillna(0, inplace=True)
        else:
            # if Company code & Company number are NaN drop entire row
            new_df = df.drop(index)
    return new_df


def load_template_and_get_variables(row, round_decimal):
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template('RATING_XML.xml')
    content = {
        'region': row['Region'],
        'country': row['Country'],
        'company_name': row['Company name'],
        'company_number': row['Company number'],
        'company_code': row['Company code'],
        'company_features': row['Company features'],
        'receiving_call_cost_per_min': round(row['Receiving call cost per min'], round_decimal),
        'local_call_cost_per_min': round(row['Local call cost per min'], round_decimal),
        'calling_to_me_cost_per_min': round(row['Calling to ME cost per min'], round_decimal),
        'calling_to_other_destinations_cost_per_min': round(row['Calling to other destinations cost per min'],
                                                            round_decimal),
        'sms_mo_cost_per_sms': round(row['SMS  MO cost per sms'], round_decimal),
        'sms_mt_cost_per_sms': round(row['SMS MT cost per sms'], round_decimal),
        'data_cost_per_mb': round(row['Data cost per MB'], round_decimal),
        'hpmn': 'HPMN',
        'effective_date': '2024',
        'submission_dt': 'SubmissionDT',
        'iot_identifier': 'IOTIdentifier',
        'correction_sequence': 'CorrectionSequence',
        'iot_currency': 'USD'}
    return template, content


def write_content_to_xml(row):
    filename = f"RATING_XML_{row['Company code']}.xml"
    template, content = load_template_and_get_variables(
        row=row, round_decimal=2)
    content = template.render(content)
    # creating xml file
    with open(filename, mode='w', encoding='utf-8') as new_xml:
        new_xml.write(content)
        print(f'... wrote {filename}')


def rating_app():
    for index, row in clean_data().iterrows():
        write_content_to_xml(row)


if __name__ == '__main__':
    rating_app()
