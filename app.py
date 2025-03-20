from flask import Flask, render_template, send_file
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    table1_df = pd.read_csv("Table 1.csv", index_col=0)
    
    print("Table 1 DataFrame:\n", table1_df)

    required_indices = ['A5', 'A7', 'A12', 'A13', 'A15', 'A20']
    missing_indices = [idx for idx in required_indices if idx not in table1_df.index]

    if missing_indices:
        return f"Error: Missing indices in the CSV file: {', '.join(missing_indices)}"

    table2_data = {
        "Category": ["Alpha", "Beta", "Charlie"],
        "Value": [
            table1_df.loc['A5'].values[0] + table1_df.loc['A20'].values[0],  
            table1_df.loc['A15'].values[0] / table1_df.loc['A7'].values[0],  
            table1_df.loc['A13'].values[0] * table1_df.loc['A12'].values[0]   
        ]
    }
    table2_df = pd.DataFrame(table2_data)

    return render_template('index.html', table1=table1_df.to_html(classes='table table-striped', index=True), table2=table2_df.to_html(classes='table table-striped', index=False))

@app.route('/download')
def download_file():
    return send_file("Table 1.csv", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
