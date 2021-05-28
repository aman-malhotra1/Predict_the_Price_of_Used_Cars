from flask import Flask, request , render_template
import numpy as np
import pandas as pd
import pickle as pkl

app = Flask(__name__)

with open('AVG_MILEAGE_AS_PER_FUEL_TYPE.pkl', 'rb') as file:
    Avg_mileage_as_per_fuel_type = pkl.load(file)
with open('AVG_NEW_PRICE_AS_PER_CARNAME_FUEL.pkl', 'rb') as file:
    Avg_new_price_as_per_car_name_fuel = pkl.load(file)
with open('cat_boost_model.pkl', 'rb') as file:
    cat_boost_model = pkl.load(file)
with open('model_columns.pkl', 'rb') as file:
    model_columns = pkl.load(file)
print(Avg_new_price_as_per_car_name_fuel)

clean_data = pd.read_csv('clean_data.csv')
car_name = clean_data['Name'].unique()
locations = clean_data['Location'].unique()
owner_type = clean_data['Owner_Type'].unique()

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        selected_car = request.form['data']
        company_name = selected_car.split()[0].upper()
        fuel_type = clean_data[clean_data['Name'] == selected_car]['Fuel_Type'].reset_index(drop=True)[0]
        transmission = clean_data[clean_data['Name'] == selected_car]['Transmission'].reset_index(drop=True)[0]
        car_manufactured_year = clean_data[clean_data['Name'] == selected_car]['Year'].unique()
        return render_template('index.html',company= company_name, fuel_type= fuel_type, transmission = transmission , year=car_manufactured_year)
    return render_template('index.html',car_name = car_name, location = locations, owner= owner_type)

@app.route('/get_engine_detail', methods = ['POST','GET'])
def get_engine_detail():
    selected_car = request.form['selected_car']
    selected_year = request.form['selected_year']
    engine = clean_data[(clean_data['Name'] == selected_car) & (clean_data['Year'] == int(selected_year))]['Engine'].reset_index(drop=True)[0]
    power = clean_data[(clean_data['Name'] == selected_car) & (clean_data['Year'] == int(selected_year))]['Power'].reset_index(drop=True)[0]
    return render_template('index.html',engine= engine, power= power)

@app.route('/get_prediction', methods = ['POST',"GET"])
def get_prediction():
    predict_df = pd.DataFrame(columns=model_columns , data=np.zeros(shape=(1,len(model_columns))))
    car_name , fuel_type = request.form['company'] , request.form['fuel_type']
    predict_df['AVG_NEW_PRICE_AS_PER_CARNAME_FUEL'] = [value for key,value in Avg_new_price_as_per_car_name_fuel.items() if key==(car_name,fuel_type)]
    predict_df['Location'] = request.form['location']
    predict_df['Kilometers_Driven'] = request.form['kilometer']
    predict_df['Fuel_Type'] = request.form['fuel_type']
    predict_df['Transmission'] = request.form['transmission']
    predict_df['Owner_Type'] = request.form['owner']
    predict_df['Owner_Type'].replace({'First':1,'Second':2,'Third':3,'Fourth & Above':4}, inplace = True)
    predict_df['Mileage'] = request.form['mileage']
    predict_df['engine'] = request.form['engine']
    predict_df['Power'] = request.form['power']
    predict_df['New_Price'] = request.form['new_price']
    predict_df['Car_Name_1'] = request.form['company']
    predict_df['Age_of_Car'] = 2020- int(request.form['year'])
    predict_df['KM_DRIVEN_PER_YEAR'] = int(predict_df['Kilometers_Driven']) /predict_df['Age_of_Car']
    predict_df['AVG_MILEAGE_AS_PER_FUEL_TYPE'] = Avg_mileage_as_per_fuel_type.get(request.form['fuel_type'])
    print(predict_df.isnull().sum())
    prediction = cat_boost_model.predict(predict_df)
    prediction = np.round(prediction*100000)
    return render_template('index.html', prediction = prediction)

if __name__ == '__main__':
    app.run(debug=True)
