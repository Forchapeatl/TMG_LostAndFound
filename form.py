from taipy.gui import Markdown




form_md =  Markdown("""
<|toggle|theme|>
<|{input_name}|input|label=Your Name|>
<|{input_item_type}|input|label=What did you loose or find|>
<|{input_where}|input|label=Where you lost item|>
lost/found: <|{input_lost_or_found}|input|>
<|{input_circle_account}|input|label=Your contact|>
<|{input_how}|input|multiline|label=How you lost item|>


<|{path}|file_selector|label=Upload Image of item|on_action=upload_image|extensions=.jpg,.png|drop_message=Drop Message|>
<|{input_date}|date|label=Date you lost item|>


<|submit|button|on_action=submit_scenario|>


""")


def run(state):
    print("form_md")
