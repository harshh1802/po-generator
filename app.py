import streamlit as st
from jinja2 import Template
import pandas as pd
import sys
from path import Path
import webbrowser

dir = Path(__file__).abspath()
print(dir)
sys.path.append(dir.parent.parent)
print(dir)

st.header("Enychip PO Generator")

date = st.date_input('Date')
po_number = st.text_input("PO No")

sup_name = st.text_input('sup_name')
sup_add = st.text_input('sup add')
sup_mail = st.text_input('Sup mail')
sales_tax = st.number_input('Sales Tax')


df = st.experimental_data_editor({'sr':[1],'part':["ADS123"],'desc':["ADS123"],'qty':[1],'unit_price':[12.25]},num_rows="dynamic")


if st.button('Generate'):

    with open("./PO_template.html","r") as f:
        temp_str = f.read()
        template = Template(temp_str)

        df = pd.DataFrame(df)
        df['qty'] = pd.to_numeric(df['qty'])
        df['unit_price'] = pd.to_numeric(df['unit_price'])
        df['line_total'] = df['qty'] * df['unit_price']
        df2 = df.to_dict(orient='records')
        subtotal = pd.to_numeric(df['line_total']).sum()
        total = subtotal * ((100+ sales_tax)/100)
        

        po_html = template.render(
            date = date,
            po_no = po_number,
            sup_name = sup_name,
            sup_add = sup_add,
            sup_mail = sup_mail,
            df = df2,
            subtotal = subtotal,
            sales_tax = sales_tax,
            total = total
        )

        with open(f'./pages/{po_number}.html', 'w') as f:
            f.write(po_html)

        file_url = f"./pages/{po_number}.html"

        st.markdown(f'<a href="{file_url}" target="_blank">Open HTML in New Tab</a>', unsafe_allow_html=True)

        webbrowser.open_new_tab(file_url)
        # converter.convert(f'eny123.html',f'{po_number}.pdf')



