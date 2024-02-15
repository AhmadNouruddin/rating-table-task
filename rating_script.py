import pandas as pd
from jinja2 import Environment, FileSystemLoader

df = pd.read_csv('./Rating_Table.csv')

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('RATING_XML.xml')

for index, row in df.iterrows():
    if not row.isnull().values.any():
        filename = f"RATING_XML_{row['Company code']}.xml"

        content = template.render({
         'region': row['Region'],
         'country': row['Country'],
         'company_name': row['Company name'],
         'company_number': row['Company number'],
         'company_code': row['Company code'],
         'company_features': row['Company features'],
         'receiving_call_cost_per_min': row['Receiving call cost per min'],
         'local_call_cost_per_min': row['Local call cost per min'],
         'calling_to_me_cost_per_min': row['Calling to ME cost per min'],
         'calling_to_other_destinations_cost_per_min': row['Calling to other destinations cost per min'],
         'sms_mo_cost_per_sms': row['SMS  MO cost per sms'],
         'sms_mt_cost_per_sms': row['SMS MT cost per sms'],
         'data_cost_per_mb': row['Data cost per MB']})

        with open(filename, mode='w', encoding='utf-8') as new_xml:
            new_xml.write(content)
            print(f'... wrote {filename}')
    else:
        print('It\'s not a valid row.')
